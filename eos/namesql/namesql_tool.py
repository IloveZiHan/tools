#!/usr/bin/python

import re

SYS_NAME = 'Ciss'
MODULE_NAME = 'Material'

def getSelectSql():
	selectSqlFile = open("sql.txt", "r")
	sqlText = selectSqlFile.read()
	selectSqlFile.close()

	return sqlText.upper()

def getPrimaryTableName(sql):
	match = re.search(r'\s*FROM\s+([\w_$\.]*)\s*', sql)
	if match:
		return removeAlias(match.group(1))
	else:
		raise("没有找到主查询表") 

def getFields(sql):
	match = re.search(r'SELECT\s+([\s\S]*)\s+FROM', sql)
	if match:
		fields = match.group(1)
		fieldList = fields.split(',')

		i = 0;
		while i < len(fieldList):
			fieldList[i] = removeAlias(fieldList[i])
			fieldList[i] = fieldList[i].strip()
			i += 1

		return fieldList
	else:
		raise("字段识别有误")

def removeAlias(field):
	aliasIdx = field.find('.');
	if aliasIdx != -1:
		field = field[aliasIdx + 1:len(field)]

	return field

def translateFields(fieldList):
	i = 0
	while i < len(fieldList):
		fieldList[i] = translateNaming(fieldList[i])
		i += 1

	return ",".join(fieldList)

def translateNaming(field):
	field = field.lower()
	wordList = field.split('_')
	i = 1
	while i < len(wordList):
		wordList[i] = upperFisrtLetter(wordList[i])
		i += 1

	return "".join(wordList)

def upperFisrtLetter(str):
	return str[0].upper() + str[1:len(str)]

def generateNewSql():
	sql = getSelectSql()
	fields = getFields(sql)
	
	i = 0
	while i < len(fields):
		sql = sql.replace(fields[i], fields[i] + ' AS ' + translateNaming(fields[i]), 1)
		i += 1

	return sql

def getParamsInName(sql):
	return getBaseName(sql) + 'In';

def getParamsOutName(sql):
	return getBaseName(sql) + 'Out';

def getBaseName(sql):
	return SYS_NAME + MODULE_NAME + 'Q' + translateNaming(getPrimaryTableName(sql))

outputFile = open('output.txt', 'w')
outputFile.write(getParamsInName(getSelectSql()) + "\n")
outputFile.write(getParamsOutName(getSelectSql()) + "\n")
outputFile.write("---namingSql---\n")
wCountSql = outputFile.write(generateNewSql())
outputFile.write("\n\n\n---originalSql---\n")
wCountSqlOriginal = outputFile.write(getSelectSql())
print("一共写入:", wCountSql + wCountSqlOriginal)

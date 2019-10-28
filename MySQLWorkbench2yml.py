# -*- coding: utf-8 -*-

from wb import *
from os.path import expanduser
import grt
import sys
import os

txt = ""

def itsPrimary(table, column):
    global txt
    for index in table.indices:
        if index.indexType == "PRIMARY":
            for col in index.columns:
                if col.referencedColumn.name == column.name:
                    txt += "      primary: true\n"
    return 0

def tipoDato(column):
    global txt
    lstTipo = {}
    lstTipo["VARCHAR"]  = "string"
    lstTipo["CHAR"]     = "char"
    lstTipo["CHARACTER"]    = "dhar"
    lstTipo["INT1"]         = "tinyint"
    lstTipo["TINYINT"]      = "tinyint" 
    lstTipo["INT2"]         = "smallint"
    lstTipo["SMALLINT"]     = "smallint"
    lstTipo["INT3"]         = "mediumint"
    lstTipo["MEDIUMINT"]    = "mediuminteger"
    lstTipo["INT4"]         = "integer"
    lstTipo["INT"]          = "integer"
    lstTipo["INTEGER"]      = "integer"
    lstTipo["INT8"]         = "bigin"
    lstTipo["BIGINT"]       = "bigint"
    lstTipo["DEC"]          = "decimal"
    lstTipo["DECIMAL"]      = "decimal"
    lstTipo["NUMERIC"]      = "decimal"
    lstTipo["FLOAT"]        = "float"
    lstTipo["DOUBLE"]       = "double"
    lstTipo["DATE"]         = "date"
    lstTipo["TIME"]         = "time"
    lstTipo["DATETIME"]     = "datetime"
    lstTipo["TIMESTAMP"]    = "timestamp"
    lstTipo["YEAR"]         = "year"
    lstTipo["BOOL"]         = "boolean"
    lstTipo["BOOLEAN"]      = "boolean"
    lstTipo["BINARY"]       = "binary"
    lstTipo["VARBINARY"]    = "varbinary"
    lstTipo["TINYTEXT"]     = "tinytext"
    lstTipo["TEXT"]         = "text"
    lstTipo["MEDIUMTEXT"]   = "mediumtext"
    lstTipo["LONG"]         = "long"
    lstTipo["LONG VARCHAR"] = "longvarchar"
    lstTipo["LONGTEXT"]     = "longtext"
    lstTipo["TINYBLOB"]     = "blob(255)"
    lstTipo["BLOB"]         = "blob(65535)"
    lstTipo["MEDIUMBLOB"]   = "blob(16777215)"
    lstTipo["LONGBLOB"]     = "blob"
    lstTipo["ENUM"]         = "enum"
    tipo = ""
    if column.simpleType:
        tipo = lstTipo[column.simpleType.name]
    else:
        tipo = lstTipo[column.formattedRawType]
    if column.length != -1:
        tipo+="("+str(column.length)+")"
    if column.precision == 1 and tipo == "tinyint":
        tipo = "boolean"
    txt += "      type: "+tipo+"\n"

def imprimirRelaciones(table):
    global txt
    if table.foreignKeys:
        txt +=  "  relations:\n"
        for key in table.foreignKeys:
            txt += "    "+key.referencedTable.name+":\n"
            if key.many:
                txt += "      foreignType: many\n"
            txt += "      foreignAlias: "+key.owner.name+"s\n"
            for col in key.columns:
                txt += "      local: "+col.name+"\n"
            for rcon in key.referencedColumns:
                txt += "      foreign: "+rcon.name+"\n"
                txt += "      class: "+rcon.owner.name+"\n"
            txt += "      owningSide: true\n"
            txt += "      onDelete: "+key.deleteRule+"\n"
            txt += "      onUpdate: "+key.updateRule+"\n"
    return 0

def exportarSchema(catalog):
    global txt
    txt += "---\n"
    schema = grt.root.wb.doc.physicalModels[0].catalog.schemata[0]
    for table in schema.tables:
        txt += table.name+":\n"
        txt += "  columns:\n"
        for column in table.columns:
            txt += "    "+column.name+":\n"
            tipoDato(column)
            if column.simpleType:
                if column.simpleType.name == "CHAR":
                    txt += "      fixed: true\n"
            if len(column.flags) > 0:
                txt += "      unsigned: true\n"
            itsPrimary(table, column)
            if column.isNotNull:
                txt += "      notnull: true\n"
        imprimirRelaciones(table)
        txt += "\n"
    currentschemafile = grt.root.wb.docPath
    path = os.path.dirname(currentschemafile)
    fh = open(path+"/schema.yml", 'w')  
    fh.write(txt)  
    fh.close()  

exportarSchema("")

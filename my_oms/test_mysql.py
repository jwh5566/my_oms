#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
__title__ = ''
__author__ = 'JWH5566'
__mtime__ = '2016/4/5'
import MySQLdb
from my_oms import settings

def mysql_command(conn,sql_cmd):
    try:
        ret = []
        conn=MySQLdb.connect(host=conn["host"],user=conn["user"],passwd=conn["password"],db=conn["database"],port=conn["port"],charset="utf8")
        cursor = conn.cursor()
        n = cursor.execute(sql_cmd)
        for row in cursor.fetchall():
            for i in row:
                ret.append(i)
    except MySQLdb.Error,e:
        ret.append(e)

    return ret

print mysql_command(settings.OMS_MYSQL, 'select ip from asset_hostlist')

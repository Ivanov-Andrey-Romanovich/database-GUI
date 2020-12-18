#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pymysql as sql
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pymysql.cursors import DictCursor
def create_database():
    conn = psycopg2.connect(port=5432,
              host="localhost",
              user="postgres",
              dbname="postgres",
              password = "1512")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur=conn.cursor()
    cur.execute("DROP DATABASE IF EXISTS sc")
    cur.execute("CREATE DATABASE sc")
    cur.close()
    conn.close()

def delete_database():
    conn = psycopg2.connect(port=5432,
              host="localhost",
              user="postgres",
              dbname="postgres",
              password = "1512")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("DROP DATABASE IF EXISTS sc")
    cur.close()
    conn.close()

    
try:
    create_database()
except psycopg2.errors.DuplicateDatabase:
    print('db already exists')
else:
    from functions import *
    new_start()


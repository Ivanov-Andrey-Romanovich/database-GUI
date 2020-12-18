#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from functions import *

db_connect = {'port': 5432,
              'host': 'localhost',
              'user': "postgres",
              'dbname': 'sc',
             'password':"1512"}



def insert_building_call(b_name, m_cost, g_cost, race ,win):
    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()
    cur.callproc('insert_building', [b_name, m_cost, g_cost,race])
    cur.close()
    conn.commit()
    win.destroy()

def get_buildings_call():
    conn = psycopg2.connect(**db_connect)
    cur=conn.cursor()
    cur.callproc('get_buildings', ())
    return cur.fetchall()

def search_building_call(name):
    conn = psycopg2.connect(**db_connect)
    cur=conn.cursor()
    cur.callproc('search_building', (name))
    return cur.fetchall()

def search_unit_call(name):
    conn = psycopg2.connect(**db_connect)
    cur=conn.cursor()
    cur.callproc('search_unit', (name))
    return cur.fetchall()


def insert_unit_call(name, m_cost,g_cost,b_id,race, win):
    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()
    cur.callproc('insert_unit', [name, m_cost,g_cost,b_id,race])
    cur.close()
    conn.commit()
    win.destroy()


def delete_unit_call(name,win):
    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()
    cur.callproc('delete_unit', [name])
    cur.close()
    conn.commit()
    win.destroy()


def delete_building_call(name, win):
    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()
    cur.callproc('delete_building', [name])
    cur.close()
    conn.commit()
    win.destroy()

def clear_all_call():
    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()
    cur.callproc('clear_all')
    cur.close()
    conn.commit()

def clear_table_call(t_name, win):
    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()
    cur.callproc('clear_table', [t_name])
    cur.close()
    conn.commit()
    win.destroy()


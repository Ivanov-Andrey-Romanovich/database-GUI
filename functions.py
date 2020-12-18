#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import psycopg2

db_conn    = {'port': 5432,
              'host': "localhost",
              'user': "postgres",
              'dbname': "sc",
              'password':"1512"}

def create_all_tables_func():
    conn = psycopg2.connect(**db_conn)
    cur = conn.cursor()
    cur.execute(
        "CREATE OR REPLACE PROCEDURE create_all_tables() AS $$ "
        "BEGIN "
        "CREATE TABLE if not exists units (units_id SERIAL PRIMARY KEY , name varchar(20),"
        "mineral_cost integer,gas_cost integer,building_id integer, race varchar(10));"
        "CREATE TABLE if not exists buildings (building_id SERIAL PRIMARY KEY, name varchar(30), "
        "mineral_cost integer,gas_cost integer, race varchar(10)); "
        "CREATE TABLE if not exists queue (q_id SERIAL PRIMARY KEY, unit_id integer, building_name varchar(30), count integer, "
        "total_mineral_cost integer, total_gas_cost integer);"
        "END;"
        "$$ LANGUAGE plpgsql;")

    cur.close()
    conn.commit()


def insert_unit_func():
    conn = psycopg2.connect(**db_conn)
    cur = conn.cursor()

    cur.execute(
        "CREATE OR REPLACE FUNCTION insert_unit(unit_name varchar(20), "
        "mincost integer,gascost integer, buildingid integer, urace varchar(10)) "
        "RETURNS VOID AS $$ "
        "BEGIN "
            "INSERT INTO units(name, mineral_cost, gas_cost, building_id,race)"
        "VALUES (unit_name, mincost, gascost, buildingid ,urace);"
        "END;"
        "$$ LANGUAGE plpgsql;",
        )

    cur.close()
    conn.commit()

def insert_building_func():
    conn = psycopg2.connect(**db_conn)
    cur = conn.cursor()

    cur.execute(
        "CREATE OR REPLACE FUNCTION insert_building(bname varchar(30), mincost integer,gascost integer, brace varchar(10))"
        "RETURNS VOID AS $$  "
        "BEGIN "
            "INSERT INTO buildings(name, mineral_cost,gas_cost, race)"
        " VALUES (bname, mincost,gascost, brace);"
        "END;"
        "$$ LANGUAGE plpgsql;",
        )

    cur.close()
    conn.commit()

    
def insert_into_queue_func():
    conn = psycopg2.connect(**db_conn)
    cur = conn.cursor()

    cur.execute(
        "CREATE OR REPLACE FUNCTION insert_into_queue(unit_name varchar(20), unit_count integer) "
        "RETURNS VOID AS $$ "
        "BEGIN "
            " INSERT INTO queue(unit_id, building_name , count) "
                "VALUES ((SELECT units_id from units where name=unit_name),"
                        "(SELECT buildings.name from units inner join buildings on units.building_id = buildings.building_id where  units.name=unit_name), "
                        "unit_count); "
        "UPDATE queue SET total_mineral_cost = count * mineral_cost FROM units where units.units_id = queue.unit_id;"
        "UPDATE queue SET total_gas_cost = count * gas_cost FROM units where units.units_id = queue.unit_id;"
        "END;"
        "$$ LANGUAGE plpgsql;",
        )

    cur.close()
    conn.commit()
    
    
def view_units_func():
    conn = psycopg2.connect(**db_conn)
    cur = conn.cursor()

    cur.execute(
        "CREATE OR REPLACE FUNCTION veiw_units() "
        "RETURNS VOID AS $$ "
        "BEGIN "
            "SELECT units_id,name,mineral_cost,gas_cost, building_id, race FROM units; "
        "END;"
        "$$ LANGUAGE plpgsql;",
        )

    cur.close()
    conn.commit()

def get_buildings_func():
    conn = psycopg2.connect(**db_conn)
    cur = conn.cursor()

    cur.execute(
        "CREATE OR REPLACE FUNCTION get_buildings()"
        " RETURNS TABLE (building_name varchar(20)) AS $$ "
        "BEGIN "
            "RETURN QUERY "
                "SELECT name FROM buildings; "
        "END; "
        "$$ LANGUAGE plpgsql;",
        )
    cur.close()
    conn.commit()

def get_queue_func():
    conn = psycopg2.connect(**db_conn)
    cur = conn.cursor()

    cur.execute(
        "CREATE OR REPLACE FUNCTION get_queue()"
        " RETURNS TABLE (id integer, unit_n varchar(20), build_n varchar(20), c integer,"
        "total_mincost integer, total_gascost integer, qrace varchar(10)) AS $$ "
        "BEGIN "
            "RETURN QUERY "
                "SELECT q_id, units.name, queue.building_name, count, total_mineral_cost, total_gas_cost, units.race"
                " FROM queue inner join units on queue.unit_id=units.units_id "
                "inner join buildings on units.building_id=buildings.building_id; "
        "END; "
        "$$ LANGUAGE plpgsql;",
        )
    cur.close()
    conn.commit()

def search_unit_func():
    conn = psycopg2.connect(**db_conn)
    cur = conn.cursor()

    cur.execute(
        "CREATE OR REPLACE FUNCTION search_unit(unit_name varchar(20))"
        " RETURNS TABLE (unit_id integer, un_name varchar(20), search_mincost integer,search_gascost integer, build_id integer,race varchar(10)) AS $$ "
        "BEGIN "
            "RETURN QUERY "
                "SELECT units_id, name,mineral_cost,gas_cost,building_id,race FROM units WHERE name=unit_name; "
        "END; "
        "$$ LANGUAGE plpgsql;",
        )
    cur.close()
    conn.commit()




def search_building_func():
    conn = psycopg2.connect(**db_conn)
    cur = conn.cursor()

    cur.execute(
        "CREATE OR REPLACE FUNCTION search_building(build_name varchar(20))"
        " RETURNS TABLE (b_id integer, b_name varchar(20), mincost integer,gascost integer, race varchar(10)) AS $$ "
        "BEGIN "
            "RETURN QUERY "
                "SELECT building_id,name,mineral_cost,gas_cost,race FROM buildings WHERE name=build_name; "
        "END; "
        "$$ LANGUAGE plpgsql;",
        )
    cur.close()
    conn.commit()

def delete_unit_func():
    conn = psycopg2.connect(**db_conn)
    cur = conn.cursor()

    cur.execute(
        "CREATE OR REPLACE FUNCTION delete_unit(u_name varchar(50)) "
        "RETURNS VOID AS $$ "
        "BEGIN "
            "DELETE FROM units where name=u_name; "
        "END;"
        "$$ LANGUAGE plpgsql;"
    )
    cur.close()
    conn.commit()

def delete_building_func():
    conn = psycopg2.connect(**db_conn)
    cur = conn.cursor()
    cur.execute(
        "CREATE OR REPLACE FUNCTION  delete_building(b_name varchar(50)) "
        "RETURNS VOID AS $$ "
        "BEGIN "
            "DELETE FROM buildings where name=b_name; "
        "END;"
        "$$ LANGUAGE plpgsql;"
    )
    cur.close()
    conn.commit()

def clear_all_func():
    conn = psycopg2.connect(**db_conn)
    cur = conn.cursor()

    cur.execute(
        "CREATE OR REPLACE FUNCTION clear_all() "
        "RETURNS VOID AS $$ "
        "BEGIN "
        "DELETE FROM units; "
        "DELETE FROM buildings; "
        "DELETE FROM queue; "
        "END;"
        "$$ LANGUAGE plpgsql;"
    )
    cur.close()
    conn.commit()

def clear_table_func():
    conn = psycopg2.connect(**db_conn)
    cur = conn.cursor()

    cur.execute(
        "CREATE OR REPLACE FUNCTION clear_table(t_name varchar(10)) "
        "RETURNS VOID AS $$ "
        "BEGIN "
        "IF (t_name = 'units') THEN "
        "DELETE FROM units; "
        "END IF;"
        "IF (t_name = 'buildings') THEN "
        "DELETE FROM buildings; "
        "END IF;"
        "IF (t_name = 'queue') THEN "
        "DELETE FROM queue; "
        "END IF;"
        "END;"
        "$$ LANGUAGE plpgsql;"
    )
    cur.close()
    conn.commit()

def insert():
    conn = psycopg2.connect(**db_conn)
    cur = conn.cursor()
    cur.execute("CALL create_all_tables();")
    cur.close()
    conn.commit()

def new_start():
    create_all_tables_func()
    insert_building_func()
    insert_unit_func()
    view_units_func()
    insert_into_queue_func()
    search_unit_func()
    get_buildings_func()
    get_queue_func()
    search_building_func()
    delete_unit_func()
    delete_building_func()
    clear_all_func()
    clear_table_func()
    insert()
    


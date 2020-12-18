#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tkinter import *
from db_creation import *
import tkinter.ttk as ttk
import tkinter as tk
from func_calls import *
from functions import *

objects=[]

db_connect = {'port': 5432,
              'host': 'localhost',
              'user': "postgres",
              'dbname': 'sc',
              'password':"1512"}



counter = 0

def get_queue_call():
    conn = psycopg2.connect(**db_connect)
    cur=conn.cursor()
    cur.callproc('get_queue', ())
    return view(tree, cur.fetchall())

def add_queue():
    list_enters=[e1, e2]
    values = tuple([e.get() for e in list_enters])
    if not all([True if value!='' else False for value in values]):
        new_window = Toplevel(window)
        label = Label(new_window, text='Please, enter the data')
        label.grid(row=0, column=0)
        return

    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()
    cur.callproc('insert_into_queue', values)
    cur.close()
    conn.commit()
    get_queue_call()
    for enter in list_enters:
        enter.delete(0, END)


def view(tree, records):
    tree.delete(*tree.get_children())
    for record in records:
        output_text = []
        for item in record:
            output_text.append(str(item))
        tree.insert('', 'end', text=output_text[0],
                    values=tuple(output_text[1:]))


def all_units_view():
    new_window = Toplevel(window)
    tree = ttk.Treeview(new_window,
                        columns=('ID', 'Unnit name',
                                 'Minerals', 'Vespen','Building number', 'Race'))
    tree.heading('#0', text='ID')
    tree.heading('#1', text='Name')
    tree.heading('#2', text='Mineral cost')
    tree.heading('#3', text='Vespen cost')
    tree.heading('#4', text='Building ID')
    tree.heading('#5', text='race')

    tree.column('#0', stretch=YES, width=30)
    tree.column('#1', stretch=YES, width=150)
    tree.column('#2', stretch=YES, width=50)
    tree.column('#3', stretch=YES, width=50)
    tree.column('#4', stretch=YES, width=30)
    tree.column('#5', stretch=YES, width=150)
    tree.grid(row=2, columnspan=6, sticky='nsew')

    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()
    cur.execute("SELECT * FROM units")
    records = cur.fetchall()
    conn.close()
    view(tree, records)

def all_buildings_view():
    new_window = Toplevel(window)
    tree = ttk.Treeview(new_window,
                        columns=('ID', 'Building name',
                                 'Minerals', 'Vespen', 'Race'))
    tree.heading('#0', text='ID')
    tree.heading('#1', text='Name')
    tree.heading('#2', text='Minerals')
    tree.heading('#3', text='Gas')
    tree.heading('#4', text='race')

    tree.column('#0', stretch=YES, width=30)
    tree.column('#1', stretch=YES, width=150)
    tree.column('#2', stretch=YES, width=50)
    tree.column('#3', stretch=YES, width=50)
    tree.column('#4', stretch=YES, width=150)
    tree.grid(row=2, columnspan=5, sticky='nsew')

    conn = psycopg2.connect(**db_connect)

    cur = conn.cursor()
    cur.execute("SELECT * FROM buildings")
    records = cur.fetchall()
    conn.close()
    view(tree, records)

def new_building_window():
    new_window = Toplevel(window)
    display = Label(new_window, text="Please, add a new building")
    display.grid(row=0)
    l1 = Label(new_window, text='Name')
    l1.grid(row=1, column=0)
    l2 = Label(new_window, text='Minerals')
    l2.grid(row=1, column=2)
    l3 = Label(new_window, text='Gas')
    l3.grid(row=3, column=0)
    l4 = Label(new_window, text='Race')
    l4.grid(row=3, column=2)

    name = StringVar()
    e1 = Entry(new_window, textvariable=name)
    e1.grid(row=1, column=1)
    minerals = StringVar()
    e2 = Entry(new_window, textvariable=minerals)
    e2.grid(row=1, column=3)
    gas = StringVar()
    e3 = Entry(new_window, textvariable=gas)
    e3.grid(row=3, column=1)
    race = StringVar()
    e4 = Entry(new_window, textvariable=race)
    e4.grid(row=3, column=3)

    add_building_to_datebase = Button(new_window, text='Add', width=12,
                                    command=lambda: insert_building_call(e1.get(), e2.get(), e3.get(),e4.get(), new_window))
    add_building_to_datebase.grid(row=4, column=3)
    new_window.mainloop()

def new_unit_window():
    new_window = Toplevel(window)
    display = Label(new_window, text="Please, add a new unit")
    display.grid(row=0)
    l1 = Label(new_window, text='Name')
    l1.grid(row=1, column=0)
    l2 = Label(new_window, text='Minerals')
    l2.grid(row=1, column=2)
    l3 = Label(new_window, text='Gas')
    l3.grid(row=2, column=0)
    l4 = Label(new_window, text='Building ID')
    l4.grid(row=2, column=2)
    l5 = Label(new_window, text='Race')
    l5.grid(row=3, column=0)
    
    name = StringVar()
    e1 = Entry(new_window, textvariable=name)
    e1.grid(row=1, column=1)
    minerals = StringVar()
    e2 = Entry(new_window, textvariable=minerals)
    e2.grid(row=1, column=3)
    gas = StringVar()
    e3 = Entry(new_window, textvariable=gas)
    e3.grid(row=2, column=1)
    building_id = StringVar()
    e4 = Entry(new_window, textvariable=building_id)
    e4.grid(row=2, column=3)
    race = StringVar()
    e5 = Entry(new_window, textvariable=race)
    e5.grid(row=3, column=1)

    add_unit_to_datebase = Button(new_window, text='Add unit', width=12,
                                     command=lambda: insert_unit_call(e1.get(), e2.get(), e3.get(),e4.get(), e5.get(), new_window))
    add_unit_to_datebase.grid(row=3, column=3)
    new_window.mainloop()
    
    
def delete_unit_window():
    new_window = Toplevel(window)
    display = Label(new_window, text="Please, delete a unit")
    display.grid(row=0)
    l1 = Label(new_window, text='Name')
    l1.grid(row=1, column=0)

    e1 = Entry(new_window, textvariable=StringVar())
    e1.grid(row=1, column=1)

    del_unit_from_datebase = Button(new_window, text='Delete', width=12,
                                    command=lambda: delete_unit_call(e1.get(), new_window))
    del_unit_from_datebase.grid(row=4, column=3)
    new_window.mainloop()


def delete_building_window():
    new_window = Toplevel(window)
    display = Label(new_window, text="Please, delete a building")
    display.grid(row=0)
    l1 = Label(new_window, text='Name')
    l1.grid(row=1, column=0)

    e1 = Entry(new_window, textvariable=StringVar())
    e1.grid(row=1, column=1)

    del_building_from_datebase = Button(new_window, text='Delete', width=12,
                                    command=lambda: delete_building_call(e1.get(), new_window))
    del_building_from_datebase.grid(row=4, column=3)
    new_window.mainloop()




def clear_table_window():
    new_window = Toplevel(window)
    display = Label(new_window, text="Please, enter title of the table")
    display.grid(row=0)
    l1 = Label(new_window, text='Table')
    l1.grid(row=1, column=0)

    title = StringVar()
    e1 = Entry(new_window, textvariable=title)
    e1.grid(row=1, column=1)


    clear_this = Button(new_window, text='Clear the table', width=12,
                                     command=lambda: clear_table_call(e1.get(), new_window))
    clear_this.grid(row=2, column=3)
    new_window.mainloop()


def delete():
    curItem = tree.focus()
    conn = psycopg2.connect(
        port=5432,
        host='localhost',
        user="postgres",
        dbname='sc',
        password = "1512",
    )
    cur = conn.cursor()
    cur.execute("DELETE FROM book WHERE name=? OR "
                "mineral_cost=? OR gas_cost=? OR building_id=? OR race=?;", (e1.get(), e2.get(), e3.get(), e4.get(), e5.get()))
    records = cur.fetchall()
    conn.close()


def delete_all():
    global counter
    counter = 0
    tree.delete(*tree.get_children())
    conn = psycopg2.connect(**db_connect)

    cur = conn.cursor()
    cur.execute("DELETE FROM book;")
    conn.commit()
    conn.close()

def delete_db2():
    delete_database()
    window.destroy()

def delete_db1():
    new_window = Toplevel(window)
    del_button = Button(new_window, text='Delete the database?', height=4,
                                     command=delete_db2)
    del_button.grid(row=1, column=1)
    new_window.mainloop()



window = Tk()

l1 = Label(window, text='Unit')
l1.grid(row=0, column=0)
objects.append(l1)

l2 = Label(window, text='Count')
l2.grid(row=0, column=2)
objects.append(l2)



e1 = Entry(window, textvariable=StringVar())
e1.grid(row=0, column=1)
objects.append(e1)

e2 = Entry(window, textvariable=StringVar())
e2.grid(row=0, column=3)
objects.append(e2)




submit_button = Button(window, text='Add unit', width=12, command=new_unit_window)
submit_button.grid(row=2, column=2)
objects.append(submit_button)

view_units_button = Button(window, text='View units', width=12, command=all_units_view)
view_units_button.grid(row=4, column=2)
objects.append(view_units_button)

add_building_button = Button(window, text='Add Building', width=12, command=new_building_window)
add_building_button.grid(row=3, column=2)
objects.append(add_building_button)

view_buildings_button = Button(window, text='View buildings', width=12, command=all_buildings_view)
view_buildings_button.grid(row=5, column=2)
objects.append(view_buildings_button)

add_toqueue = Button(window, text='Add to queue', width=12, command=add_queue)
add_toqueue.grid(row=0, column=5)
objects.append(add_toqueue)

show_queue = Button(window, text='Refresh queue', width=12, command=get_queue_call)
show_queue.grid(row=2, column=1)
objects.append(show_queue)

delete_unit_button = Button(window, text='Del unit', width=12, command=delete_unit_window)
delete_unit_button.grid(row=2, column=3)
objects.append(delete_unit_button)

delete_building_button = Button(window, text='Del building', width=12, command=delete_building_window)
delete_building_button.grid(row=3, column=3)
objects.append(delete_building_button)

delete_database_button = Button(window, text='Del database', width=12, command=delete_db1)
delete_database_button.grid(row=4, column=3)
objects.append(delete_database_button)

clear_all_button = Button(window, text='Clear all', width=12, command=clear_all_call)
clear_all_button.grid(row=3, column=1)

clear_table_button = Button(window, text='Clear table', width=12, command=clear_table_window)
clear_table_button.grid(row=4, column=1)

tree = ttk.Treeview(window,
                    columns=('id', 'Unit',
                             'Building', 'Count', 'Total Minerals','Total gas', 'race' ))
tree.heading('#0', text='id')
tree.heading('#1', text='Unit')
tree.heading('#2', text='Building')
tree.heading('#3', text='Count')
tree.heading('#4', text='Tot minerals')
tree.heading('#5', text='Tot gas')
tree.heading('#6', text='Race')



tree.column('#0', stretch=YES, width=30)
tree.column('#1', stretch=YES, width=150)
tree.column('#2', stretch=YES, width=150)
tree.column('#3', stretch=YES, width=50)
tree.column('#4', stretch=YES, width=50)
tree.column('#5', stretch=YES, width=50)
tree.column('#6', stretch=YES, width=150)



tree.grid(row=8, columnspan=10)
treeview = tree



entry_list = [children for children in window.children.values() if 'entry' in str(children)]
window.mainloop()


# In[ ]:





# In[ ]:





# In[ ]:





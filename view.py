#this code is part of the Final Degree Project in UNIR by Gonzalo Castro

from connection_database import connection_db

#import package (“Tk interface”) is the standard Python interface to the Tcl/Tk GUI toolkit. 
import tkinter as tk
from tkinter import ttk, messagebox

#module that makes accessing ODBC databases simple
import pyodbc

#this module is used to locate and run Python modules without importing them first.
import runpy

font_1B = ("Arial",14,"bold")
connection_string=connection_db()

def load_data():
    """
    load data to connect to database
    and execute a SELECT to get all Regular Expressions
    Returns:
    An array with values: RE_Name, RE_Expression, Editable
    """
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("SELECT RE_Name, RE_Expression, Editable FROM Reg_Exp order by RE_Name")
    datos = cursor.fetchall()
    conn.close()
    return datos

def load_and_display_data():
    """
    load all data and show the values in a grid
    """
    
    for row in tree.get_children():
        tree.delete(row)

    datos = load_data()
    for row in datos:
        tree.insert('', tk.END, values=(row.RE_Name,row.RE_Expression,row.Editable))

def back_user():
    """
    return to principal window
    """
    root.destroy()
    runpy.run_path("users.py")
    
    return


root = tk.Tk()
frame = tk.Frame(root)
tree = ttk.Treeview(frame)
root.title("Regular Expressions Management")
root.configure(bg='#151547')

frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
tree = ttk.Treeview(frame, columns=('RE_Name', 'RE_Expression', 'Editable'), show='headings')
tree.heading('RE_Name', text='Name')
tree.heading('RE_Expression', text='Regular Expression')
tree.heading('Editable', text='Editable')

tree.column('RE_Name', width=150, anchor=tk.W)
tree.column('RE_Expression', width=400, anchor=tk.W)
tree.column('Editable', width=80, anchor=tk.W)
tree.pack(fill=tk.BOTH, expand=True)

boton_back = tk.Button(root, text="Back to User Panel", command=back_user,font=font_1B)
boton_back.pack(side=tk.LEFT,padx=5,pady=5)

load_and_display_data()

root.mainloop()

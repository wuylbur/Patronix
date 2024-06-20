#this code is part of the Final Degree Project in UNIR by Gonzalo Castro

from connection_database import connection_db

#import package (“Tk interface”) is the standard Python interface to the Tcl/Tk GUI toolkit. 
import tkinter as tk
from tkinter import ttk, messagebox

#module that makes accessing ODBC databases simple
import pyodbc

#this module is used to locate and run Python modules without importing them first.
import runpy


#fonts types
font_1 = ("Arial",14)
font_1B = ("Arial",14,"bold")

connection_string=connection_db()

def load_data():
    #load data from Regular Expressions
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("SELECT RE_Name, RE_Expression, Editable FROM Reg_Exp order by RE_Name")
    data= cursor.fetchall()
    conn.close()
    return data

def update_data(re_name, new_expression):
    #update information about Regular expressions in the database
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("UPDATE Reg_Exp SET RE_Expression = ? WHERE RE_Name = ?", (new_expression, re_name))
    conn.commit()
    conn.close()

def edit_row():
    #select a row to edit, but only with Editable = TRUE
    choice = tree.selection()
    if not choice:
        messagebox.showwarning("Select row", "Please select a row to edit")
        return

    item = tree.item(choice[0])
    values = item['values']

    if values[2] != 'True':
        messagebox.showwarning("Not editable", "The selected item is not editable")
        return
    #draw the window
    main_Window = tk.Toplevel(root)
    main_Window.title("Edit Regular Expression")
    main_Window.configure(bg='#151547')

    tk.Label(main_Window, text="Name:",font=font_1,bg='#151547',fg="white").grid(row=0, column=0, padx=10, pady=10)
    tk.Label(main_Window, text=values[0],font=font_1,bg='#151547',fg="white").grid(row=0, column=1, padx=10, pady=10)

    tk.Label(main_Window, text="Expression:",font=font_1,bg='#151547',fg="white").grid(row=1, column=0, padx=10, pady=10)
    entry_expresion = tk.Entry(main_Window, width=50,font=font_1)
    entry_expresion.grid(row=1, column=1, padx=10, pady=10)
    entry_expresion.insert(0, values[1])

    def Save_Changes(): #save changes
        new_expression = entry_expresion.get()
        update_data(values[0], new_expression)
        main_Window.destroy()
        load_and_display_data()

    save_button = tk.Button(main_Window, text="Save", command=Save_Changes,font=font_1B)
    save_button.grid(row=2, column=0, columnspan=2, pady=10)

def load_and_display_data(): #load the infomration from databe ans draw the main window
    for row in tree.get_children():
        tree.delete(row)

    datos = load_data()
    for row in datos:
        tree.insert('', tk.END, values=(row.RE_Name,row.RE_Expression,row.Editable))

def back_user(): #return to main window 
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

edit_button = tk.Button(root, text="Edit Selection", command=edit_row,font=font_1B)
edit_button.pack(side=tk.LEFT,padx=20,pady=5)
back_button = tk.Button(root, text="Back to User Panel", command=back_user,font=font_1B)
back_button.pack(side=tk.LEFT,padx=160,pady=5)

load_and_display_data()

root.mainloop()

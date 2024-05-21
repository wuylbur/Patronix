from connection_database import connection_db
import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
import runpy

font_1B = ("Arial",14,"bold")
cadena_conexion=connection_db()

def cargar_datos():
    conn = pyodbc.connect(cadena_conexion)
    cursor = conn.cursor()
    cursor.execute("SELECT RE_Name, RE_Expression, Editable FROM Reg_Exp order by RE_Name")
    datos = cursor.fetchall()
    conn.close()
    return datos

def cargar_y_mostrar_datos():
    for row in tree.get_children():
        tree.delete(row)

    datos = cargar_datos()
    for row in datos:
        tree.insert('', tk.END, values=(row.RE_Name,row.RE_Expression,row.Editable))

def back_user():
    root.destroy()
    runpy.run_path("TFG_TKINTER\\users.py")
    
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

cargar_y_mostrar_datos()

root.mainloop()

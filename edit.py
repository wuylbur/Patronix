from connection_database import connection_db
import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
import runpy

font_1 = ("Arial",14)
font_1B = ("Arial",14,"bold")

cadena_conexion=connection_db()

def cargar_datos():
    conn = pyodbc.connect(cadena_conexion)
    cursor = conn.cursor()
    cursor.execute("SELECT RE_Name, RE_Expression, Editable FROM Reg_Exp order by RE_Name")
    datos = cursor.fetchall()
    conn.close()
    return datos

def actualizar_datos(re_name, nueva_expresion):
    conn = pyodbc.connect(cadena_conexion)
    cursor = conn.cursor()
    cursor.execute("UPDATE Reg_Exp SET RE_Expression = ? WHERE RE_Name = ?", (nueva_expresion, re_name))
    conn.commit()
    conn.close()

def editar_fila():
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Select row", "Please select a row to edit")
        return

    item = tree.item(seleccion[0])
    values = item['values']

    if values[2] != 'True':
        messagebox.showwarning("Not editable", "The selected item is not editable")
        return

    ventana_edicion = tk.Toplevel(root)
    ventana_edicion.title("Edit Regular Expresión")
    ventana_edicion.configure(bg='#151547')

    tk.Label(ventana_edicion, text="Name:",font=font_1,bg='#151547',fg="white").grid(row=0, column=0, padx=10, pady=10)
    tk.Label(ventana_edicion, text=values[0],font=font_1,bg='#151547',fg="white").grid(row=0, column=1, padx=10, pady=10)

    tk.Label(ventana_edicion, text="Expression:",font=font_1,bg='#151547',fg="white").grid(row=1, column=0, padx=10, pady=10)
    entry_expresion = tk.Entry(ventana_edicion, width=50,font=font_1)
    entry_expresion.grid(row=1, column=1, padx=10, pady=10)
    entry_expresion.insert(0, values[1])

    def guardar_cambios():
        nueva_expresion = entry_expresion.get()
        actualizar_datos(values[0], nueva_expresion)
        ventana_edicion.destroy()
        cargar_y_mostrar_datos()

    boton_guardar = tk.Button(ventana_edicion, text="Save", command=guardar_cambios,font=font_1B)
    boton_guardar.grid(row=2, column=0, columnspan=2, pady=10)

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

boton_editar = tk.Button(root, text="Edit Selection", command=editar_fila,font=font_1B)
boton_editar.pack(side=tk.LEFT,padx=20,pady=5)
boton_back = tk.Button(root, text="Back to User Panel", command=back_user,font=font_1B)
boton_back.pack(side=tk.LEFT,padx=160,pady=5)

cargar_y_mostrar_datos()

root.mainloop()

#this code is part of the Final Degree Project in UNIR by Gonzalo Castro

from connection_database import connection_db

#import package (“Tk interface”) is the standard Python interface to the Tcl/Tk GUI toolkit. 
import tkinter as tka
import tkinter.messagebox as messagebox

#module that makes accessing ODBC databases simple
import pyodbc

#this module is used to locate and run Python modules without importing them first.
import runpy

connection_string=connection_db()


#Fonts Type
font_0= ("Arial",9)
font_1 = ("Arial",14)
font_1B = ("Arial",14,"bold")
font_2B = ("Arial",16, "bold")

#Main window

win_add = tka.Tk()
win_add.title("Patronix - Add new Regular Expression")
win_add.geometry("730x250")
win_add.configure(bg='#151547')
win_add.resizable(False,False)

name_text = tka.StringVar()
expression_text = tka.StringVar()



def add_data():
    """
    To add a new regular expression, we check that we have written in the text boxes,
    and that neither the name nor the regular expression is repeated
    """
    name = name_text.get()
    expression = expression_text.get()
    
    if name and expression:
        #check that there are no duplicates in the name fileds, because we cannot create two with the same name
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("SELECT RE_Name, RE_Expression FROM Reg_Exp WHERE [RE_Name] = ?",(name))
        data_name = cursor.fetchall()
        conn.commit()
        conn.close()
        
        #if repeats, came back
        if data_name:
            messagebox.showerror("ERROR", "Name already registered. Choose another, please.")
            return
        
        #check that there are no duplicates in the expression fileds, because we cannot create two with the same name       
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("SELECT RE_Name, RE_Expression FROM Reg_Exp WHERE [RE_Expression] = ?",(expression))
        data_expression=cursor.fetchall()
        conn.commit()
        conn.close()
        
        #if repeats, came back
        if data_expression:
          messagebox.showerror("ERROR", "Regular Expression already registered. Choose another, please.")
          return
        
        #if not repeated, inserted
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Reg_Exp (RE_Name, RE_Expression, Editable) VALUES (?, ?, ?)", name, expression, "1")
        conn.commit()
        conn.close()
        messagebox.showinfo("Added", "New Regular Expression added successfully")
    
    else:
        messagebox.showwarning("Warning", "Please complete all fields")
   
   
def back_user(): #came back to Main Users window
    win_add.destroy()
    runpy.run_path("users.py")
    
    return   
   
       
def open_main_add():
     
    name_entry=tka.Entry(win_add)
    expression_entry=tka.Entry(win_add)
     
    heading_label = tka.Label(win_add, text="PatroniX - New Regular Expression", font=font_1, bg='#151547',fg="white").place(x=190,y=5)
    
    name_label = tka.Label(win_add, text="New Name: ",font=font_1,bg='#151547',fg="white", anchor="w").place(x=20, y=50)
    name_entry = tka.Entry(win_add,textvariable=name_text, font=font_1, width=40).place(x=250, y=50)

    expression_label = tka.Label(win_add, text="New Regular Expression:",font=font_1,bg='#151547',fg="white", anchor="w").place(x=20, y=90)
    expression_label2 = tka.Label(win_add,text="IMPORTANT!  Please, make sure the code is correct.", font=font_0,bg='#151547',fg="white", anchor="w").place(x=250,y=125)
    expression_label3 = tka.Label(win_add,text="This application does not validate the Regular Expressions ", font=font_0,bg='#151547',fg="white", anchor="w").place(x=250,y=145)
    expression_entry = tka.Entry(win_add,textvariable=expression_text, font=font_1, width=40).place(x=250, y=90)
       
    login_button = tka.Button(win_add, text="Add New Line", command=add_data, font=font_1B).place(x=70, y=190)
    back_button = tka.Button(win_add, text="Back to User Panel", command=back_user, font=font_1B).place(x=290, y=190)      
    exit_button = tka.Button(win_add, text="Exit", command=win_add.destroy, font=font_1B).place(x=550, y=190)
    
    win_add.mainloop()

open_main_add()

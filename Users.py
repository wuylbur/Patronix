#this code is part of the Final Degree Project in UNIR by Gonzalo Castro

#import package (“Tk interface”) is the standard Python interface to the Tcl/Tk GUI toolkit. 
import tkinter as tku
import tkinter.messagebox as messagebox

#This module implements a common interface to many different secure hash and message digest algorithms.
import hashlib

#module that makes accessing ODBC databases simple
import pyodbc

#This module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter
import sys

#this module is used to locate and run Python modules without importing them first.
import runpy

from connection_database import connection_db, check_db
from reports import reports

connection_string=connection_db()
 
#Font Types
font_1 = ("Arial",14)
font_1B = ("Arial",14,"bold")
font_2B = ("Arial",16, "bold")

#Main window
win_user = tku.Tk()
win_user.title("Patronix - Log In")
win_user.geometry("680x400")
win_user.configure(bg='#151547')
win_user.resizable(False,False)


#entry user variables
user_text = tku.StringVar()
password_text = tku.StringVar()
  
def log_in():
  """
  The user type user and password.
  Checks if the combination of both are in the database table and if so, returns the user's group

  """
  username = user_text.get()
  password = password_text.get()
    
  if username and password:
      hashed_password = hashlib.sha256(password.encode()).hexdigest()
      conn = pyodbc.connect(connection_string)
      cursor = conn.cursor()
      cursor.execute("SELECT [Group] FROM USERS WHERE [User]=? AND [Password]=?", (username, hashed_password))
      row = cursor.fetchone()
      if row:
          group = row[0]
          messagebox.showinfo("Successful login", "Welcome, {}!".format(username))
      else:
          messagebox.showerror("Login Error", "Invalid username or password.")
          group="error"
  else:
    messagebox.showwarning("Warning", "Please complete all fields")
    group="error"
        
  return (group)
      
def reports():
  
  #if the group has permission to open REPORTS, proceed. If not, return error.
  group = log_in()
   
  if group == "Admin":
    win_user.destroy()
    reports()
  elif group=="Normal":    
    messagebox.showerror("Warning", "Sorry, you have not permissions. You must be Admin user.")
  else:
    return  
    
def logIn():
  #if the group has permission to open SEARCH, proceed. All groups has permission by default.
  group = log_in()
  if group == "Admin" or group=="Normal":
    win_user.destroy()
    runpy.run_path("search.py")
 
  return  

def view_RE():
  #if the group has permission to view Regular Expresions, proceed. All groups has permission by default.
  group = log_in()
  if group == "Admin" or group=="Normal":
    runpy.run_path("view.py")
  
  return    
 
def add_RE():
   #if the group has permission to add Regular Expressions, proceed. If not, return error.
    
  group = log_in()
   
  if group == "Admin":
    win_user.destroy()
    runpy.run_path("add.py")
  elif group=="Normal":    
    messagebox.showerror("Warning", "Sorry, you have not permissions. You must be Admin user.")
  else:
    return  
 
def edit_RE():
  #if the group has permission to edit Regular Expressions, proceed. If not, return error.
  
  group = log_in()
  
  if group == "Admin":
    win_user.destroy()
    runpy.run_path("edit.py")
  elif group=="Normal":    
    messagebox.showerror("Warning", "Sorry, you have not permissions. You must be Admin user.")
  else:
    return  
  
def open_main_users(): 
  #main window
  heading_label = tku.Label(win_user, text="PatroniX Search Tool", font=("Arial", 30, "bold"), bg='#151547',fg="white").place(x=150,y=5)
  heading2_label = tku.Label(win_user, text="Welcome to PatroniX. ", font=font_1,bg='#151547',fg="white", anchor="w").place(x=50,y=70)
  heading3_label = tku.Label(win_user, text="Please, type your user and password and choice one option. ", font=font_1,bg='#151547',fg="white", anchor="w").place(x=50,y=100)

  user_label = tku.Label(win_user, text="User:",font=font_2B,bg='#151547',fg="white", anchor="w").place(x=50, y=170)
  user_entry = tku.Entry(win_user,textvariable=user_text, font=font_1B, width=20).place(x=170, y=170)

  password_label = tku.Label(win_user, text="Password:",font=font_2B,bg='#151547',fg="white", anchor="w").place(x=50, y=200)
  password_entry = tku.Entry(win_user,textvariable=password_text, show="*",font=font_1B, width=20).place(x=170, y=200)

  login_button = tku.Button(win_user, text="Log In to App", command=logIn, font=font_1B).place(x=50, y=290)
  reportes_button =tku.Button (win_user, text="Reports", command=reports,font=font_1B).place(x=50,y=340)
  re_label=tku.Label(win_user, text="Regular Expresions:",font=font_2B,bg='#151547',fg="white", anchor="w").place(x=285, y=290)
  view_button = tku.Button(win_user, text="View", command=view_RE, font=font_1B).place(x=280, y=340)
  edit_button = tku.Button(win_user, text="Modify", command=edit_RE, font=font_1B).place(x=350, y=340)
  add_button = tku.Button(win_user, text="Add", command=add_RE, font=font_1B).place(x=440, y=340)
  cancel_button= tku.Button (win_user, text="Exit", command=win_user.destroy, font=font_1B).place(x=585, y=340)
 
  win_user.mainloop()
  
  
if check_db(connection_string):
  print("Successful connection")
  
else:
  print("Connection Error in DB ")
  sys.exit()
  
open_main_users() 
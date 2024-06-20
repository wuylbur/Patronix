#this code is part of the Final Degree Project in UNIR by Gonzalo Castro


#import package (“Tk interface”) is the standard Python interface to the Tcl/Tk GUI toolkit. 
import tkinter as tks
from tkinter import *
from tkinter import messagebox, filedialog

#This module provides a portable way of using operating system dependent functionality
import os

#This module supplies classes for manipulating dates and times.
from datetime import datetime

#module that makes accessing ODBC databases simple
import pyodbc

#This module implements a common interface to many different secure hash and message digest algorithms.
import hashlib

#This module offers classes representing filesystem paths with semantics appropriate for different operating systems
from pathlib import Path

#this module is used to locate and run Python modules without importing them first.
import runpy


from connection_database import connection_db
from idscan import generate_id_scan
from search_intext import Search_Pattern, Search_GDPR
from convert_text import convert_txt
from Add_Meta import add_Metadata_GDPR, add_Metadata_Pattern
from verify_path import verify

#main window
window = tks.Tk()
window.title("PatroniX Search Tool")
window.geometry("1070x500")
window.configure(bg='#151547')
window.resizable(False,False)

# Variables
path_seach= tks.StringVar()
pattern=tks.StringVar()
gdpr = tks.BooleanVar()
file_large= tks.BooleanVar()
recursive=tks.BooleanVar()
metadata_check=tks.BooleanVar()
pdf_check=tks.BooleanVar()
doc_check=tks.BooleanVar()
docx_check=tks.BooleanVar()
xls_check=tks.BooleanVar()
xlsx_check=tks.BooleanVar()
rtf_check=tks.BooleanVar()
txt_check=tks.BooleanVar()
csv_check=tks.BooleanVar()
ppt_check=tks.BooleanVar()
pptx_check=tks.BooleanVar()
expreg_check=tks.BooleanVar()
odt_check=tks.BooleanVar()
ods_check=tks.BooleanVar()
odp_check=tks.BooleanVar()
checkboxes = []

connection_string=connection_db()

#Font Types
font_0= ("Arial",9)
font_1 = ("Arial",14)
font_1B = ("Arial",14,"bold")
font_1C = ("Arial",12,"bold")
font_2B = ("Arial",16, "bold")


def search_files(pathway, extensiones,file_large_flag,recursive_value):
  """
  Given a specific path, we search for files whose extensions have been selected,
  taking into account whether we want to search for large files and whether the recursion option is checked
  
  """
  files = []
  
  if recursive_value: #if we mark the recursion
    path_temp= Path(pathway).rglob("*")
  else: #if we do not mark the recursion
    path_temp=Path(pathway).glob("*")
    
  
  for file in path_temp: #for each file found in the path
    if file.is_file(): #if is a file (it is not a folder)
      #extract the name and extension
      extension = file.suffix.upper()[1:]
      name,ext=os.path.splitext(file.name)
      
      if not (name.startswith("~$")): #discard the temporary files
        if (extension in extensiones): #if the extension is within those chosen
          
          #take the date of creation and last modification and size
          fecha_creacion = datetime.fromtimestamp(file.stat().st_ctime)
          fecha_modificacion = datetime.fromtimestamp(file.stat().st_mtime)
          size_tmp = file.stat().st_size
          
          if file_large_flag==0 and size_tmp > 50000000: #If we choose NOT to review a large file and file size is greater than 50MB
            print ("fichero grande, no registar")
          else:
            file_info = { #collect information from the file
              "name": file.name,
              "extension": extension,
              "size": file.stat().st_size,
              "date_create": fecha_creacion.strftime("%d/%m/%Y %H:%M"),
              "date_modify": fecha_modificacion.strftime("%d/%m/%Y %H:%M"),
              "path_complete": str(file)
            }
            files.append(file_info) #add the information from the file to the final list
  print (len(files))
  return files


def storage_data_main ():
  """
  save the search values ​​in the database
  """
  path_search_value = path_seach.get()
  pattern_value = pattern.get()
  gdpr_value=gdpr.get()
  expreg_value=expreg_check.get()
  file_large_value=file_large.get()
  date_time_now = datetime.now()
  date_search_value = date_time_now.strftime("%d/%m/%Y %H:%M")
  ID_Scan_value= generate_id_scan()
  recursive_value=recursive.get()
 
    
  if not path_search_value or not path_search_value: #if any field is missing on the path or pattern return error.
    messagebox.showerror("Error", "Please enter all details about Path or Pattern correctly.")
  else:
    try: #connect to the database and save the search 
      conn = pyodbc.connect(connection_string)
      cursor = conn.cursor()
      cursor.execute("INSERT INTO dbo.Main_Scan (ID_Scan,Path,Pattern,GDPR,Personalized,File_large,Recursive,Date) VALUES (?,?,?,?,?,?,?,?)",(ID_Scan_value,path_search_value,pattern_value,gdpr_value,expreg_value,file_large_value,recursive_value,date_search_value))
      conn.commit()
      conn.close()
      
    except Exception as e:
      messagebox.showerror("Error", f"Main Registration failed: {e}")
        
  return ID_Scan_value #return IDScan value

def storage_data_documents(Files_list,ID_Scan_value):
  """
  save the data of the files found with the search criteria in the database
  """
  
  File_List_full=[]
  
  for file in Files_list:
    
    if file["size"] > 5000000:
      file_large_tmp = 1 #the file is big size
    else:
      file_large_tmp = 0 #the file is small size 
    
    #calculate the SHA-256 hash of the file with the full path, extension, size, creation and last modification date and the IDScan
    hash_id = hashlib.sha256(
        (file["path_complete"] + file["extension"] + str(file["size"]) +
         file["date_create"] + file["date_modify"]+ str(ID_Scan_value)).encode()
    ).hexdigest()
            
    try: #connect to the database and add the information to the table
      conn = pyodbc.connect(connection_string)
      cursor = conn.cursor()
      cursor.execute("INSERT INTO dbo.Documents (ID_Document,ID_Scan,Name,Extension,Modify_Date,Creation_Date,Path_Document,Size,Large) VALUES (?,?,?,?,?,?,?,?,?)",
                     (hash_id,ID_Scan_value,file["name"],file["extension"],file["date_modify"],file["date_create"],file["path_complete"],file["size"],file_large_tmp))
      conn.commit()
      conn.close()
      
      files_info = {
          "ID_Document": hash_id,
          "ID_Scan": ID_Scan_value,
          "name": file["name"],
          "extension": file["extension"],
          "size":file["size"] ,
          "date_create":file["date_create"],
          "date_modify":file["date_modify"],
          "path_complete": file["path_complete"],
          "file_large": file_large_tmp
          }
      File_List_full.append(files_info)
      
    except Exception as e:
      messagebox.showerror("Error", f"Document Registration failed: {e}")
  
  return File_List_full #We return the complete list of files that meet the search criteria so as not to have to read them again from the database

def Get_Exp_reg(value0,value1):
  """
  go to the database and pull out all the regular expressions stored in the table
  
  """
  query="SELECT [RE_Name],[RE_Expression] FROM REG_EXP" #select all regular expressions
  if value0 is True and value1 is False: #if GDPR check is enable to include in the search
    query= query + " WHERE EDITABLE=0"
  elif value0 is False and value1 is True: #custom regular expressions checking is enabled to include in search
    query= query + " WHERE EDITABLE=1"
    
  try: #execute query
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(query)
    reg_exp = cursor.fetchall()
    conn.commit()
    conn.close()
    
  except Exception as e:
    messagebox.showerror("Error", f"Main Registration failed: {e}")
     
  return reg_exp #return regular expression 
           

def add_GDPR_BD(result_GDPR, IDF,IDS, OK_Meta):
  #add the found expressions to the DataBase
  conn = pyodbc.connect(connection_string)
    
  for result in result_GDPR: #For each regular expression found in the file, we save a line with the file and regular expression information
    type_value=result[0]
    type_infotypes=result[1]
    print("1: ", result)
    for type_infotype in type_infotypes:
      try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO dbo.Scan_Details_GDPR (ID_Document,ID_Scan,Type,Infotype, Metadata) VALUES (?,?,?,?,?)",(IDF, IDS,type_value, type_infotype,OK_Meta))
        conn.commit()
        
      except Exception as e:
        messagebox.showerror("Error", f"Document Registration failed: {e}")
  conn.close()
  
  return
  

def add_Pattern_BD (pattern_value,IDF,IDS,OK_Meta2): #add the pattern to the DataBase
  conn = pyodbc.connect(connection_string)
  try:#For each pattern found in the file, we save a line with the file and regular expression information
    cursor = conn.cursor()
    cursor.execute("INSERT INTO dbo.Scan_Details_Pattern (ID_Document,ID_Scan,Pattern,Metadata) VALUES (?,?,?,?)",(IDF, IDS,pattern_value,OK_Meta2))
    conn.commit()
              
  except Exception as e:
   messagebox.showerror("Error", f"Document Registration failed: {e}")
  conn.close()
  return
  


def explore_path():#path search button function
  ruta = filedialog.askdirectory()
  path_seach.set(ruta)
  


def select_all_check():#Check all extension options with a button
  for checkbox in checkboxes:
    checkbox.set(True)

  
def deselect_all_check():#Uncheck all extension options with a button    
  for checkbox in checkboxes:
    checkbox.set(False)
       


def search_main():
  """
  launch the search for patterns and/or regular expressions based on the parameters entered in the form
  """
  
  #we take all the options of the form
  path_search_value = path_seach.get()
  pattern_value = pattern.get()
  gdpr_value=gdpr.get()
  file_large_value=file_large.get()
  ID_Scan_value= generate_id_scan()
  recursive_value=recursive.get()
  expreg_value=expreg_check.get()
  pdf_value=pdf_check.get()
  doc_value=doc_check.get()
  docx_value=docx_check.get()
  xls_value=xls_check.get()
  xlsx_value=xlsx_check.get()
  rtf_value=rtf_check.get()
  txt_value=txt_check.get()
  csv_value=csv_check.get()
  ppt_value=ppt_check.get()
  pptx_value=pptx_check.get()
  odt_value=odt_check.get()
  ods_value=ods_check.get()
  odp_value=odp_check.get()
  metadata_value = metadata_check.get()
  
  if verify(path_search_value): #verify the path
    print("path OK")
  else:
    messagebox.showerror("Error", "The path is not exits or is empty. Please, type a correct one.")
    return
  
  #need either the GDPR expressions, or the custom expressions or the pattern to be active. It doesn't work if I have nothing to search for   
  if gdpr_value is False and pattern_value == "" and expreg_value is False: 
    messagebox.showerror ("Error","All options cannot be empty. Choose GDPR, Custom Regular Expressions and/or enter a valid pattern")
    return
   
  #list of extensions selected
  extensions=[]
  if pdf_value:
    extensions.append ("PDF")
  
  if doc_value:
    extensions.append ("DOC")
  
  if docx_value:
    extensions.append ("DOCX")
  
  if xls_value:
   extensions.append ("XLS")
  
  if xlsx_value:
    extensions.append ("XLSX")
    
  if ppt_value:
   extensions.append ("PPT")  
    
  if pptx_value:
    extensions.append ("PPTX")  

  if rtf_value:
   extensions.append ("RTF")

  if csv_value:
    extensions.append ("CSV")
    
  if txt_value:
    extensions.append ("TXT")
    
  if odt_value:
    extensions.append ("ODT")
  
  if ods_value:
    extensions.append ("ODS")

  if odp_value:
    extensions.append ("ODP")
  
  ID_Scan_value = storage_data_main() #Let's store the generic search data and return the IDScan
  Files_list=[]
  Files_list = search_files(path_search_value,extensions,file_large_value,recursive_value) #search all files in the path with conditions
  
  if len(Files_list) > 0: #if the list is not empty
    File_List_Full = storage_data_documents(Files_list, ID_Scan_value)
  else:
    messagebox.showerror ("Error","The list is empty. We have not found valid files for the default extensions")
    return
    
    
  for i in range (len(File_List_Full)): #For each of the files
    
    file_txt = convert_txt (File_List_Full[i]) #launch conversion to plain text
    
    OK_Meta1 =False
    OK_Meta2 =False
    #settings of the file
    IDF = File_List_Full[i]["ID_Document"]
    IDS = File_List_Full[i]["ID_Scan"]
    e1= File_List_Full[i]["extension"]
    p1=File_List_Full[i]["path_complete"]
            
    if gdpr_value is True or expreg_value is True: #if GDPR or custom Exp. Reg. are selected
    
      expresiones_regulares=Get_Exp_reg(gdpr_value,expreg_value)
      result_GDPR = Search_GDPR (file_txt,expresiones_regulares)
      
      
      if len(result_GDPR) > 0: #if search more than one GDPR Reg. Exp.
        if metadata_value:
          OK_Meta1 = add_Metadata_GDPR (p1,e1,result_GDPR)
    
         
      add_GDPR_BD(result_GDPR, IDF,IDS,OK_Meta1 ) #add the GDPR search to the database
      
          
    if pattern_value != "": #If we want to search for a pattern, the pattern field is not empty.
      result_Pattern = Search_Pattern(file_txt,pattern_value)
      
      if result_Pattern: #matches have been found
        OK_Meta2 = add_Metadata_Pattern (p1,e1,pattern_value)
        add_Pattern_BD (pattern_value,IDF,IDS,OK_Meta2) #add the pattern search to the database
      else:
        messagebox.showinfo("ATTENTION","No matches found.")
      
  messagebox.showinfo("CONGRATULATION", "SEARCH COMPLETED")
      
  return



def back_user():#back to user window
  
    window.destroy()
    runpy.run_path("users.py")
    
    return   
   
def open_Main_search():
    
  heading_label = tks.Label(window, text="PatroniX Search Tool", font=("Arial", 30, "bold"), bg='#151547',fg="white").place(x=270,y=5)

  path_searchtk_label = tks.Label(text="Type a seach path:", font=font_1,bg='#151547',fg="white", anchor="w").place(x=30,y=80)
  path_searchtk_label2 = tks.Label(text="Format: U:\\ folder\\ folder2", font=font_0,bg='#151547',fg="white", anchor="w").place(x=230,y=105)
  path_searchtk_boton = tks.Button(text="Search", command=explore_path, font=font_1C).place(x=805,y=75)

  patron_search_label = tks.Label(text="Search Pattern:", font=font_1,bg='#151547',fg="white", anchor="w").place(x=30,y=130)
  patron2_search_label = tks.Label(text="(distinguishes uppercase from lowercase)", font=font_0,bg='#151547',fg="white", anchor="w").place(x=230, y=155)

  path_searchtk_entry = tks.Entry(textvariable=path_seach,font=font_1, width=50).place(x=230, y=80)
  patron_search_entry = tks.Entry(textvariable=pattern,font=font_1, width=30).place(x=230, y=130)

  gdpr_checkbutton = tks.Checkbutton(text="", variable=gdpr, font=font_1,bg='#151547',fg="red").place (x=30,y=180)
  gdpr_label = tks.Label(text="Do you want to search for Spanish GDPR regular expressions?", font=font_1,bg='#151547',fg="white", anchor="w").place(x=54,y=183)

  expreg_checkbutton=tks.Checkbutton (text="",variable=expreg_check,font=font_1,bg='#151547',fg="red").place (x=30,y=220)
  expreg_label =tks.Label(text="Do you want to include custom Regular Expressions in the search?", font=font_1,bg='#151547',fg="white", anchor="w").place(x=54,y=223)
 
  file_large_checkbutton= tks.Checkbutton(text="", variable=file_large, font=font_1,bg='#151547',fg="red").place(x=30, y=260)
  file_large_label = tks.Label(text="Do you want to include a file larger than 50 MB in size in the search?", font=font_1,bg='#151547',fg="white", anchor="w").place(x=54,y=263)

  recursive_checkbutton=tks.Checkbutton(text="",variable=recursive,font=font_1,bg='#151547',fg="red").place(x=30, y=300)
  recursive_label= tks.Label(text="Do you want to do the recursive search? ",font=font_1,bg='#151547',fg="white", anchor="w").place(x=54,y=303)
  
  metadata_checkbutton=tks.Checkbutton(text="",variable=metadata_check,font=font_1,bg='#151547',fg="red").place(x=30, y=340)
  metadata_label= tks.Label(text="Do you want the metadata of the file with the search found to be modified? ",font=font_1,bg='#151547',fg="white", anchor="w").place(x=54,y=343)
  
  extension_label=tks.Label(text="Choose the extension to search:",font=font_1,bg='#151547',fg="white", anchor="w").place(x=710, y=160)
    
  pdf_checkbutton=tks.Checkbutton(text=" ",variable=pdf_check,font=font_1,bg='#151547',fg="red").place(x=730, y=190)
  pdf_label=tks.Label(text="PDF",font=font_1,bg='#151547',fg="white", anchor="w").place(x=754, y=193)
  checkboxes.append(pdf_check)
  
  doc_checkbutton=tks.Checkbutton(text="",variable=doc_check,font=font_1,bg='#151547',fg="red").place(x=730, y=220)
  doc_label=tks.Label(text="DOC",font=font_1,bg='#151547',fg="white").place(x=754, y=223)
  checkboxes.append(doc_check)
    
  xls_checkbutton=tks.Checkbutton(text="",variable=xls_check,font=font_1,bg='#151547',fg="red").place(x=730, y=250)
  xls_label=tks.Label(text="XLS",font=font_1,bg='#151547',fg="white").place(x=754, y=253)
  checkboxes.append(xls_check)
  
  ppt_checkbutton=tks.Checkbutton(text="",variable=ppt_check,font=font_1,bg='#151547',fg="red").place(x=730, y=280)
  ppt_label=tks.Label(text="PPT",font=font_1,bg='#151547',fg="white").place(x=754, y=283)
  checkboxes.append(ppt_check)
  
  txt_checkbutton=tks.Checkbutton(text="",variable=txt_check,font=font_1,bg='#151547',fg="red").place(x=730, y=310)
  txt_label=tks.Label(text="TXT",font=font_1,bg='#151547',fg="white").place(x=754, y=313)
  checkboxes.append(txt_check)
  
  odt_checkbutton=tks.Checkbutton(text="",variable=odt_check,font=font_1,bg='#151547',fg="red").place(x=730, y=340)
  odt_label=tks.Label(text="ODT",font=font_1,bg='#151547',fg="white").place(x=754, y=343)
  checkboxes.append(odt_check)
  
  ods_checkbutton=tks.Checkbutton(text="",variable=ods_check,font=font_1,bg='#151547',fg="red").place(x=730, y=370)
  ods_label=tks.Label(text="ODS",font=font_1,bg='#151547',fg="white").place(x=754, y=373)
  checkboxes.append(ods_check)
    
  rtf_checkbutton=tks.Checkbutton(text="",variable=rtf_check,font=font_1,bg='#151547',fg="red").place(x=870, y=190)
  rtf_label=tks.Label(text="RTF",font=font_1,bg='#151547',fg="white").place(x=900, y=193)
  checkboxes.append(rtf_check) 
 
  docx_checkbutton=tks.Checkbutton(text="",variable=docx_check,font=font_1,bg='#151547',fg="red").place(x=870, y=220)
  docx_label=tks.Label(text="DOCX",font=font_1,bg='#151547',fg="white", anchor="w").place(x=900, y=223)
  checkboxes.append(docx_check)
  
  xlsx_checkbutton=tks.Checkbutton(text="",variable=xlsx_check,font=font_1,bg='#151547',fg="red").place(x=870, y=250)
  xlsx_label=tks.Label(text="XLSX",font=font_1,bg='#151547',fg="white", anchor="w").place(x=900, y=253)
  checkboxes.append(xlsx_check)
  
  pptx_checkbutton=tks.Checkbutton(text="",variable=pptx_check,font=font_1,bg='#151547',fg="red").place(x=870, y=280)
  pptx_label=tks.Label(text="PPTX",font=font_1,bg='#151547',fg="white", anchor="w").place(x=900, y=283)
  checkboxes.append(pptx_check)
  
  csv_checkbutton=tks.Checkbutton(text="",variable=csv_check,font=font_1,bg='#151547',fg="red").place(x=870, y=310)
  csv_label=tks.Label(text="CSV",font=font_1,bg='#151547',fg="white", anchor="w").place(x=900, y=313)
  checkboxes.append(csv_check)
  
  odp_checkbutton=tks.Checkbutton(text="",variable=odp_check,font=font_1,bg='#151547',fg="red").place(x=870, y=340)
  odp_label=tks.Label(text="ODP",font=font_1,bg='#151547',fg="white").place(x=900, y=343)
  checkboxes.append(odp_check)
    
  check_button=tks.Button(text="Check All",command=select_all_check,font=font_1C).place (x=710, y=420)
  uncheck_button=tks.Button(text="Uncheck All",command=deselect_all_check,font=font_1C).place(x=870,y=420)
     
  buscar_button = tks.Button(text="Search", command=search_main, font=font_1B).place(x=90,y=420)
  exit_button = tks.Button(text="Back to User Panel", command=back_user, font=font_1B).place(x=290,y=420)
  
  window.mainloop()


open_Main_search()
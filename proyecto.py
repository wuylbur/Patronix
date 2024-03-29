#libreria de entorno grafico
import tkinter as tk
import tkinter as tk2
from tkinter import messagebox
#módulo estándar que proporciona una interfaz para interactuar con el sistema operativo en el que se ejecuta el programa
import os
import sys
#importamos biblioteca de tiempo
from datetime import date, time, datetime
#importa biblioteca de SQL ODBC
import pyodbc
#importa la biblioteca de hash SHA-256, entre otros
import hashlib
#biblioteca de trabajo con rutas
from pathlib import Path
#para sacar texto de PDF y DOC
from tika import parser
#biblioteca de trabajo con expresiones regulares
import re

Window_Main = None
Window_Report = None

window = tk.Tk()
windowR = tk.Tk()
windowR.withdraw()

window.title("PatroniX Search Tool")
window.geometry("970x480")
window.configure(bg='#151547')
window.resizable(False,False)


# Variables
path_seach= tk.StringVar()
pattern=tk.StringVar()
gdpr = tk.BooleanVar()
file_large= tk.BooleanVar()
recursive=tk.BooleanVar()

var_ids = tk2.StringVar()
var_fname = tk2.StringVar()
var_fname = tk2.StringVar()
var_ext = tk2.StringVar()
var_date = tk2.StringVar()
var_pattern = tk2.StringVar()

  
# Lista de extensiones a buscar

extensions = ["DOC", "PDF", "DOCX","XLS","XLSX","RTF","PPT","PPTX","CSV"] 

# Diccionario de expresiones regulares y nombres
expresiones_regulares = {
  #Correo Electronico
  r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b': "Correo Electrónico",
  # Pasaporte
  r'\b[A-Z]{1}[0-9A-Z]{1}[0-9]{6,8}\b': "Pasaporte",
  # Número de la Seguridad Social española
  r'\d{8}[A-Z]': "Número de la Seguridad Social española",
  # Código IBAN
  r'^[A-Z]{2}\d{2}[A-Z0-9]{4}\d{7}([A-Z0-9]?){0,16}$': "Código IBAN",
  # VAT number (Número de IVA)
  r'^[A-Z]{2}[0-9A-Z]{2,}$': "VAT number",
  #Tarjeta Generica
  r'\b(?:\d[ -]*?){13,16}\b': "Tarjeta de Crédito Genérica"
  }

#SQL Variables
server = '**************\SQLEXPRESS'
database = 'BD_Patronix'
username = '************'
password = '****************'

# Crear una conexión para mas adelante
cadena_conexion = f'Driver={{SQL Server}};Server={server};Database={database};Uid={username};Pwd={password}'

# Configurar la fuente
font_1 = ("Arial",14)
font_1B = ("Arial",14,"bold")
font_2= ("Arial",9)

#generate ID to File with hash SHA-256
def generar_id_fichero(nombre_fichero):
  """
  Genera un ID para un fichero usando un hash del nombre del fichero.
  Parámetros:
    nombre_fichero: Nombre del fichero.
  Retorno:
    ID del fichero.
  """
  hash_sha= hashlib.sha256(nombre_fichero.encode("utf-8")).hexdigest()
  #hash_md5 = hashlib.md5(nombre_fichero.encode("utf-8")).hexdigest()
  return hash_sha

#search all files with specify extensions in a path
def buscar_archivos(ruta, extensiones,file_large_flag,recursive_value):
  """
  Función que busca archivos con extensions específicas en un directorio y sus subdirectorios.

  Parámetros:
    ruta: Ruta del directorio donde se inicia la búsqueda.
    extensiones: Lista de extensions a buscar.

  Retorno:
    Generador que devuelve una tupla con la información de cada archivo encontrado.
  """
  archivos = []
  if recursive_value:
    path_temp= Path(ruta).rglob("*")
  else:
    path_temp=Path(ruta).glob("*")
    
  for archivo in path_temp:
    
    if archivo.is_file():
      extension = archivo.suffix.upper()[1:]
      
      if extension in extensiones:
        print(archivo, "filtrado por extension: ",extension)
        
        fecha_creacion = datetime.fromtimestamp(archivo.stat().st_ctime)
        fecha_modificacion = datetime.fromtimestamp(archivo.stat().st_mtime)
        
        size_tmp = archivo.stat().st_size
        
        if file_large_flag==0 and size_tmp > 5000000:
          print ("fichero grande, no registar")
        else:
          archivo_info = {
            "name": archivo.name,
            "extension": extension,
            "size": archivo.stat().st_size,
            "date_create": fecha_creacion.strftime("%d/%m/%Y %H:%M"),
            "date_modify": fecha_modificacion.strftime("%d/%m/%Y %H:%M"),
            "path_complete": str(archivo)
           }
          archivos.append(archivo_info)
  print (len(archivos))
  return archivos

#verifica si la ruta introducida es valida
def verify(ruta):
  """
  Verifica si una ruta de archivo es válida.
  Parámetros:
    ruta: Ruta de archivo a verificar.
  Retorno:
    True si la ruta es válida, False si no.
  """
  if not ruta:
    messagebox.showerror("Error", "Please enter all details about Path or Pattern correctly.")
    return  False
    #ruta2=Path(ruta)
  return os.path.exists(ruta)
  
#storage data main in window to SQL Server table     
#guarda datos en la BD del formulario inicial, y devuleve el ID_Scan generado
def storage_data_main ():
  # Obtener los valores de las entradas de texto
  path_search_value = path_seach.get()
  pattern_value = pattern.get()
  gdpr_value=gdpr.get()
  file_large_value=file_large.get()
  date_time_now = datetime.now()
  date_search_value = date_time_now.strftime("%d/%m/%Y %H:%M")
  ID_Scan_value= generar_id_scan()
  recursive_value=recursive.get()
   
  # muestra las variable sen Terminal.
  print ("ID_Scan: ", ID_Scan_value)
  print ("Ruta: ", path_search_value)
  print ("Patron: " , pattern_value)
  print ("Valor GDPR: " , gdpr_value)
  print("File Large?", file_large_value)
  print("Dia y Hora actual:", date_search_value)
  print("Recursividad: ", recursive_value)
  
  
  if not path_search_value or not path_search_value:
    messagebox.showerror("Error", "Please enter all details about Path or Pattern correctly.")
  else:
      try:
        conn = pyodbc.connect(cadena_conexion)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO dbo.Main_Scan (ID_Scan,Path,Pattern,GDPR,File_large,Recursive,Date) VALUES (?,?,?,?,?,?,?)",(ID_Scan_value,path_search_value,pattern_value,gdpr_value,file_large_value,recursive_value,date_search_value))
        conn.commit()
        conn.close()
        #messagebox.showinfo("Success", "Main Registration successful!")
      except Exception as e:
        messagebox.showerror("Error", f"Main Registration failed: {e}")
        
  return ID_Scan_value

#guardamos en BD los datso de los files encontrados
def storage_data_documents(Files_list,ID_Scan_value):
  File_List_full=[]
  
  for file in Files_list:
    
    if file["size"] > 5000000:
      file_large_tmp = 1 #el fichero es grande
    else:
      file_large_tmp = 0 # el fichero es pequeño
    
    
    
    
    hash_id = hashlib.sha256(
        (file["path_complete"] + file["extension"] + str(file["size"]) +
         file["date_create"] + file["date_modify"]+ str(ID_Scan_value)).encode()
    ).hexdigest()
    print (hash_id)
        
    
  
    try:
      conn = pyodbc.connect(cadena_conexion)
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
      
      #messagebox.showinfo("Success", "Document Registration successful!")
    except Exception as e:
      messagebox.showerror("Error", f"Document Registration failed: {e}")
  
  #messagebox.showinfo("Success", "Document Registration successful!")
  return File_List_full

#conetar con  la BD de SQL
def check_db ():
  
  # Credenciales de conexión
  server = 'PLX3000003578\SQLEXPRESS'
  database = 'BD_Patronix'
  username = 'sa'
  password = 'Admin.1234'

  # Crear una cadena de conexión
  cadena_conexion = f'Driver={{SQL Server}};Server={server};Database={database};Uid={username};Pwd={password}'

  # Conectarse a la base de datos
  try:
      conexion = pyodbc.connect(cadena_conexion)
      print("Conexión exitosa")
      return True
  except pyodbc.Error as e:
      print("Error al conectar:", e)
      return False
  finally:
    conexion.close()    
 
#genera ID Scan YYYYMMDDHHmmssSSS
def generar_id_scan():
  """
  Genera un ID único basado en la fecha y hora actual.
  Formato del ID: YYYYMMDDHHmmssSSS
  Retorno:
    str: ID único generado.
  """
  # Obtiene la fecha y hora actual
  fecha_hora_actual = datetime.now()

  # Formateo de la fecha y hora
  anio = str(fecha_hora_actual.year).zfill(4)
  mes = str(fecha_hora_actual.month).zfill(2)
  dia = str(fecha_hora_actual.day).zfill(2)
  hora = str(fecha_hora_actual.hour).zfill(2)
  minuto = str(fecha_hora_actual.minute).zfill(2)
  segundo = str(fecha_hora_actual.second).zfill(2)
  milisegundo = str(fecha_hora_actual.microsecond)[:3]

  # Concatenación para formar el ID único
  id_scan = f"{anio}{mes}{dia}{hora}{minuto}{segundo}{milisegundo}"

  return id_scan  

#convierte el ficheroofimatico en texto plano apra tratarlo
def convert_txt(info_file):
  path_txt = info_file["path_complete"]
  
  if info_file["extension"]=="PDF" or info_file["extension"]=="DOC" or info_file["extension"]=="DOCX" or info_file["extension"]=="XLS" or info_file["extension"]=="XLSX" or info_file["extension"]=="PPTX" or info_file["extension"]=="PPT" or info_file["extension"]=="CSV" or info_file["extension"]=="RTF":
   # Parse data from file
   file_data = parser.from_file(path_txt)
   # Get files text content
   text = file_data['content']
   #print(text)
  return text  

  if info_file["extension"]=="TXT":
      with open(path_txt,"r") as archivo:
        contenido=archivo.read()
      archivo.close()
  return text
  
 
def Total_Search():
  
  Sentencia = """
  SELECT
      D.ID_Document,
      D.ID_Scan,
      D.Name,
      D.Extension,
      D.Modify_Date,
      D.Creation_Date,
      D.Path_Document,
      D.Size,
      D.Large,
      MS.Path AS Scan_Path,
      MS.Pattern AS Main_Scan_Pattern,
      MS.GDPR,MS.File_Large AS Scan_File_Large,
      MS.Date AS Scan_Date,
      SDG.Type,
      SDG.Infotype,
      SDP.Pattern AS Details_Pattern 
  FROM Documents AS D INNER JOIN Main_Scan AS MS ON D.ID_Scan = MS.ID_Scan
  LEFT JOIN Scan_Details_GDPR AS SDG ON D.ID_Document = SDG.ID_Document
  LEFT JOIN Scan_Details_Pattern AS SDP ON D.ID_Document = SDP.ID_Document
  ORDER BY D.ID_Scan, MS.Date;
  """
  
  conn = pyodbc.connect(cadena_conexion)
  cursor = conn.cursor()
  cursor.execute(Sentencia)
  resultados = cursor.fetchall() 
  
  for fila in resultados:
    print(fila)
  
      
      
#generar reporte con filtros
def generate():
     
  ids_value = var_ids.get()
  idf_value = var_fname.get()
  fname_value= var_fname.get()
  ext_value = var_ext.get()
  date_value = var_date.get()
  pattern_value = var_pattern.get()
    
  if ids_value=="" and idf_value=="" and fname_value=="" and ext_value=="" and date_value=="" and pattern_value=="":
     
    ALL = messagebox.askquestion("Attention!", "Are you sure you want to generate the complete report?")
    
    if ALL:
      Total_Search()
      
      print ("pasa por aqui")    
      return
    else:
      
      OK_IDS, OK_IDF, OK_Fname,OK_Ext,OK_Date,OK_patt = validate_fields(ids_value,idf_value,fname_value, ext_value,date_value,pattern_value)
      #Seach_Filter  
      
  
def validate_fields(ids, idf, fname, ext, date, patt):
  
  OK_IDS = False
  OK_IDF = False
  OK_Fname = False
  OK_Ext = False
  OK_Date = False
  OK_patt = False
  
  
  patron_ids = "r'^\d{4}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])([01]\d|2[0-3])([0-5]\d){2}\d{3}$'"
       
  if ids!="":
    if bool(re.match(patron_ids, ids)):
      OK_IDS = True
    else:
      messagebox.showerror("Error", "Please review the ID Scan. The format is not correct.")
      return

      
  if idf!="":
    if len(idf)==64:
     OK_IDF = True
    else:
      messagebox.showerror("Error", "Please check the ID Document. Must be 64 characters.")
      return
  
  if fname != "":
      OK_Fname= True
    
  if ext !="":
      if ext in extensions:
        OK_Ext=True
      else:
        messagebox.showerror("Error", "Please check the extension typed. Must be one of ", extensions)
        return
    
    
  if date!="":
    formatos = ["DD/MM/AAAA", "DD-MM-AAAA", "DD.MM.AAAA"]
    for formato in formatos:
      try:
          dia, mes, año = map(int, date.split(formato[2]))
      except ValueError:
          continue

      if not 1 <= dia <= 31:
          continue
      if not 1 <= mes <= 12:
          continue
      if not 0 <= año <= 9999:
          continue
      OK_Date = True
    else:
       messagebox.showerror("Error", "Please check the date format.") 


        
    if patt !="":
      OK_patt = True   

  return OK_IDS, OK_IDF, OK_Fname,OK_Ext,OK_Date,OK_patt
          
#añadir las expresiones encontradas a la BD
def add_GDPR_BD(result_GDPR, IDF,IDS):
  
  conn = pyodbc.connect(cadena_conexion)
    
  for result in result_GDPR:
    type_value=result[0]
    type_infotypes=result[1]
    print("1: ", result)
    for type_infotype in type_infotypes:
      try:
        print("añadir: ", type_value, " y " , type_infotype)
        
        cursor = conn.cursor()
        cursor.execute("INSERT INTO dbo.Scan_Details_GDPR (ID_Document,ID_Scan,Type,Infotype) VALUES (?,?,?,?)",(IDF, IDS,type_value, type_infotype))
        conn.commit()
        #messagebox.showinfo("Success", "Details SCAN GDPR Complete PARTIAL! 295")
      except Exception as e:
        messagebox.showerror("Error", f"Document Registration failed: {e}")
  conn.close()
  #messagebox.showinfo("Success", "Details SCAN GDPR Complete! 325")
  pass
  
#añade a la BD los patrones encontrados en los docuemntos
def add_Pattern_BD (pattern_value,IDF,IDS):
  conn = pyodbc.connect(cadena_conexion)
  try:
    print("añadir: ", pattern_value)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO dbo.Scan_Details_Pattern (ID_Document,ID_Scan,Pattern) VALUES (?,?,?)",(IDF, IDS,pattern_value))
    conn.commit()
              
  except Exception as e:
   messagebox.showerror("Error", f"Document Registration failed: {e}")
  conn.close()
  
  #messagebox.showinfo("Success", "Details SCAN Pattern Complete!")

#busca expresiones regulares en texto plano
def Search_GDPR(texto_plano,expresion_regular):
  """
  Busca expresiones regulares en un texto plano.

  Parámetros:
    texto_plano: Texto plano en el que se desea buscar expresiones regulares.

  Devuelve:
    Lista con las expresiones regulares encontradas y sus nombres.
  """
  
  # Lista para almacenar las expresiones regulares encontradas
  resultados = []

  # Recorrer las expresiones regulares
  for expresion_regular, nombre in expresiones_regulares.items():
    # Buscar coincidencias en el texto plano
    coincidencias = re.findall(expresion_regular, texto_plano)
    print ("Encontrados: ",coincidencias)
    # Si se encuentra una coincidencia, agregar el resultado a la lista
    if coincidencias:
      resultados.append((nombre, coincidencias)) #FALTA METER EL ID DE FICHERO
      
  print ("Resultados", resultados)
  return resultados

#busca patones de texto en textos planos
def Search_Pattern(texto,patron):
  """
  Función que busca un patrón en un texto plano.
  Parámetros:
    texto (str): El texto plano donde se busca el patrón.
    patron (str): El patrón a buscar en el texto.
  Retorno:
    bool: True si se encuentra el patrón, False si no.
  """
  # Compilar la expresión regular
  expresion_regular = re.compile(patron)
  # Buscar el patrón en el texto
  resultado = expresion_regular.search(texto)

  # Si se encuentra el patrón, devolver True
  if resultado:
    return True

  # Si no se encuentra el patrón, devolver False
  return False
  



def abrir_Report():        
  wR_bg ="#265100"
  windowR = tk2.Tk()
  windowR.geometry("970x480")
  windowR.title("Report Filters")
  windowR.configure(bg="#265100")
  windowR.resizable(False,False)
    
  var_ids = tk2.StringVar()
  var_idd = tk2.StringVar()
  var_fname=tk2.StringVar()
  var_ext= tk2.StringVar()
  var_date = tk2.StringVar()
  var_pattern = tk2.StringVar()
  
  heading_label = tk2.Label(windowR, text="Report Filters", font=("Arial", 30, "bold"), bg=wR_bg,fg="white").place(x=270,y=5)

  label_ids = tk2.Label(windowR, text="By Scan ID: ",font=font_1,bg = wR_bg,fg="white", anchor="w").place(x=30,y=80)
  label_ids2 = tk2.Label(windowR, text="Format: YYYYMMDDHHmmssSSS ",font=font_2,bg = wR_bg ,fg="white", anchor="w").place(x=230,y=105)

  label_idd = tk2.Label(windowR,text="By Document ID: ",font=font_1,bg=wR_bg,fg="white", anchor="w").place(x=30,y=130)
  label_idd2 = tk2.Label(windowR,text="Format: 64 characters in Hexadecimal",font=font_2,bg=wR_bg,fg="white", anchor="w").place(x=230,y=155)

  label_fname = tk2.Label(windowR,text="By Document Name: ",font=font_1,bg=wR_bg,fg="white", anchor="w").place(x=30,y=180)
  label_fname2 = tk2.Label(windowR,text="Format: Document Name without Extension ",font=font_2,bg=wR_bg,fg="white", anchor="w").place(x=230,y=205)

  label_extension = tk2.Label(windowR,text="By Extension Name: ",font=font_1,bg=wR_bg,fg="white", anchor="w").place(x=30,y=230)
  label_extension2 = tk2.Label(windowR,text="Formats: DOC, PDF, DOCX, XLS, XLSX, RTF, PPT, PPTX, CSV",font=font_2,bg=wR_bg,fg="white", anchor="w").place(x=230,y=255)

  label_date = tk2.Label(windowR,text="Scan Date: ",font=font_1,bg=wR_bg,fg="white", anchor="w").place(x=30,y=280)
  label_date2 = tk2.Label(windowR,text="Format: DD/MM/AAAA: ",font=font_2,bg=wR_bg,fg="white", anchor="w").place(x=230,y=305)

  label_pattern = tk2.Label(windowR,text="Find a Pattern: ",font=font_1,bg=wR_bg,fg="white", anchor="w").place(x=30,y=330) 
  label_pattern2 = tk2.Label(windowR,text="Format: one word  ",font=font_2,bg=wR_bg,fg="white", anchor="w").place(x=230,y=355) 


  ids_entry = tk2.Entry(windowR,textvariable=var_ids,font=font_1, width=20).place (x=230,y=80)
  idd_entry = tk2.Entry(windowR,textvariable=var_idd, font=font_1,width=63).place (x=230,y=130)
  fname_entry = tk2.Entry(windowR,textvariable=var_fname,font=font_1,width=50).place (x=230,y=180)
  ext_entry = tk2.Entry (windowR,textvariable=var_ext,font=font_1, width=5).place (x=230,y=230)
  date_entry = tk2.Entry(windowR,textvariable=var_date,font=font_1, width=10).place (x=230,y=280)
  pattern_entry = tk2.Entry(windowR,textvariable=var_pattern,font=font_1, width=50).place (x=230,y=330)

  search2_button = tk2.Button(windowR,text="GENERATE", command = generate, font=font_1B).place(x=230,y=410)
  back_button = tk2.Button(windowR,text="BACK", command = windowR.destroy, font=font_1B).place(x=710,y=410)
  search2_button.pack()
  back_button.pack()
  
  

  # Iniciar el bucle principal
  windowR.focus_force()
  windowR.mainloop()
  return
             

"""
  Funciones Principales
  EXIT: salir de la aplicacion
  SEARCH: busqueda de ficheros segun ruta, patron, etc.
  REPORTS: reportes de ficheros ya buscados.

"""

def abrir_Main():
  heading_label = tk.Label(window, text="PatroniX Search Tool", font=("Arial", 30, "bold"), bg='#151547',fg="white").place(x=270,y=5)

  path_searchtk_label = tk.Label(text="Type a seach path:", font=font_1,bg='#151547',fg="white", anchor="w").place(x=30,y=80)
  path_searchtk_label2 = tk.Label(text="Format: U:\\ folder\\ folder2", font=font_2,bg='#151547',fg="white", anchor="w").place(x=230,y=105)

  patron_busqueda_label = tk.Label(text="Search Pattern:", font=font_1,bg='#151547',fg="white", anchor="w").place(x=30,y=130)
  patron2_busqueda_label = tk.Label(text="(distinguishes uppercase from lowercase)", font=font_2,bg='#151547',fg="white", anchor="w").place(x=230, y=155)

  path_searchtk_entry = tk.Entry(textvariable=path_seach,font=font_1, width=50).place(x=230, y=80)
  patron_busqueda_entry = tk.Entry(textvariable=pattern,font=font_1, width=30).place(x=230, y=130)

  # Crear el checkbotón GDPR
  gdpr_checkbutton = tk.Checkbutton(text="", variable=gdpr, font=font_1,bg='#151547',fg="red").place (x=30,y=180)
  gdpr_label = tk.Label(text="Spanish GDPR", font=font_1,bg='#151547',fg="white", anchor="w").place(x=54,y=183)

  # Crear el cherckbutton Ficheros Largos
  file_large_checkbutton= tk.Checkbutton(text="", variable=file_large, font=font_1,bg='#151547',fg="red").place(x=30, y=220)
  file_large_label = tk.Label(text="Do you want to include a file larger than 5 MB in size in the search?", font=font_1,bg='#151547',fg="white", anchor="w").place(x=54,y=223)

  #Hacer la busqueda recursiva
  recursive_checkbutton=tk.Checkbutton(text="",variable=recursive,font=font_1,bg='#151547',fg="red").place(x=30, y=260)
  recursive_label= tk.Label(text="Do you want to do the recursive search? ",font=font_1,bg='#151547',fg="white", anchor="w").place(x=54,y=263)
  
  
  
  # Crear los botones
  buscar_button = tk.Button(text="SEARCH", command=busqueda, font=font_1B).place(x=110,y=410)
  reportes_button = tk.Button(text="REPORTS", command=reportes, font=font_1B).place(x=400,y=410)
  exit_button = tk.Button(text="EXIT", command=exit, font=font_1B).place(x=730,y=410)
  #buscar_button.pack()
  #reportes_button.pack()
  #exit_button.pack()

  window.mainloop()


# Función para salir de la aplicación

# Función para comenzar a realizar la búsqueda
# hay que pasar ruta, patron, gdpr.
def busqueda():
  path_search_value = path_seach.get()
  pattern_value = pattern.get()
  gdpr_value=gdpr.get()
  file_large_value=file_large.get()
  date_time_now = datetime.now()
  date_search_value = date_time_now.strftime("%d/%m/%Y %H:%M")
  ID_Scan_value= generar_id_scan()
  recursive_value=recursive.get()
  
  
  #path_search_value = path_seach.get()
  print (f"valor de path es: {path_search_value}") 
    
  if not path_search_value:
    messagebox.showerror("Error", "Please enter all details about Path or Pattern correctly.")
    return    
     
  if verify(path_search_value):
    print("La ruta es válida")
  else:
    print("La ruta no es válida")
    messagebox.showerror("Error", "The path is not exits or is empty. Please, type a correct one.")
    return
  
  
  if gdpr_value is False and pattern_value == "":
    print (pattern_value)
    print (f"Valor de GDPR es: ",{gdpr_value})
    messagebox.showerror ("Error","Both options cannot be empty. Please choose either GDPR and/or enter a valid pattern")
    return
     
  #esta funcion guarda los registros del formulario inicial, comprobando que el path funciona
  ID_Scan_value = storage_data_main()
   
  Files_list=[]
  Files_list = buscar_archivos(path_search_value,extensions,file_large_value,recursive_value)
  
  #comprobar que la lista no es vacia
  if len(Files_list) > 0:
    print("La lista no está vacía.")
    File_List_Full = storage_data_documents(Files_list, ID_Scan_value)
    
  else:
    print("La lista está vacía. No hemos encontrado archivos válidos")
    return
    
  print ("Numero de fichero a Revisar: ", len(File_List_Full))
  
  for i in range (len(File_List_Full)):
            
    print("Fichero num: ",i, "de ", len(File_List_Full))
    print(File_List_Full[i])
    print("Lanzamos conversion de texto")
    
    file_txt = convert_txt (File_List_Full[i])
    
    print ("IMPRESION DEL TEXTO: ")
    print (file_txt)
    print( "FIN TEXTO")
    
    IDF = File_List_Full[i]["ID_Document"]
    IDS = File_List_Full[i]["ID_Scan"]
            
    if gdpr_value is True:
      result_GDPR = Search_GDPR (file_txt,expresiones_regulares)
      #messagebox.showinfo("GDPR Search", "GDPR search successful")
      
      print("El resultado de la busqueda GDPRes: ", result_GDPR)
      
      print ("IDFICHERO",IDF,"IDSCAN", IDS)      
      add_GDPR_BD(result_GDPR, IDF,IDS )
      print("GDPR guardado")
      
   
      
    if pattern_value != "":
      result_Pattern = Search_Pattern(file_txt,pattern_value)
      #messagebox.showinfo("Pattern Search", "Pattern search successful")
      if result_Pattern:
        print("Se han encontrado coincidencias. ")
        add_Pattern_BD (pattern_value,IDF,IDS)
        print("Pattern guardado")
      else:
        print("No se han encontrado coincidencias. ")
      
  messagebox.showinfo("BUSQUEDA FINALIZADA", "BUSQUEDA FINALIZADA")
  
      
  pass

# Función para generar reportes
def reportes():
      
  abrir_Report()
      
    
  # Implementar la lógica de generación de reportes
  

    
#COMIENZA PROCESO CENTRAL
  
#comprueba que la BD esta correcta
if check_db():
  print("Successful connection")
else:
  print("Error en conexion BD ")
  sys.exit()
    
# Etiquetas de cabecera y box  
abrir_Main()

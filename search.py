#libreria de entorno grafico
import tkinter as tks
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
#módulo estándar que proporciona una interfaz para interactuar con el sistema operativo en el que se ejecuta el programa
import os
#importamos biblioteca de tiempo
from datetime import datetime
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
#biblioteca docx que nos permite trabajar con archivos DOC y DOCX
import docx
from docx import Document
#biblioteca docx que nos permite trabajar con archivos XLS y XLSX
import openpyxl
#biblioteca docx que nos permite trabajar con archivos XLS y XLSX
from pptx import Presentation
#biblioteca para obtener numeros random
import random
import runpy
from connection_database import connection_db

#variables de la ventana
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

cadena_conexion=connection_db()

# Configurar la fuente
font_0= ("Arial",9)
font_1 = ("Arial",14)
font_1B = ("Arial",14,"bold")
font_1C = ("Arial",12,"bold")
font_2B = ("Arial",16, "bold")

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
      nombre,ext=os.path.splitext(archivo.name)
      if not (nombre.startswith("~$")):
        if (extension in extensiones):
          print(archivo, "filtrado por extension: ",extension)
          
          fecha_creacion = datetime.fromtimestamp(archivo.stat().st_ctime)
          fecha_modificacion = datetime.fromtimestamp(archivo.stat().st_mtime)
          
          size_tmp = archivo.stat().st_size
          
          if file_large_flag==0 and size_tmp > 20000000:
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
  expreg_value=expreg_check.get()
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
  print ("Expresiones Regulares Personalizadas", expreg_value)
  print("File Large?", file_large_value)
  print("Dia y Hora actual:", date_search_value)
  print("Recursividad: ", recursive_value)
  
  
  if not path_search_value or not path_search_value:
    messagebox.showerror("Error", "Please enter all details about Path or Pattern correctly.")
  else:
      try:
        conn = pyodbc.connect(cadena_conexion)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO dbo.Main_Scan (ID_Scan,Path,Pattern,GDPR,Personalized,File_large,Recursive,Date) VALUES (?,?,?,?,?,?,?,?)",(ID_Scan_value,path_search_value,pattern_value,gdpr_value,expreg_value,file_large_value,recursive_value,date_search_value))
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
    
    #generate ID to File with hash SHA-256
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

#genera ID Scan YYYYMMDDHHmmssSSS
def generar_id_scan():
  """
  Genera un ID único basado en la fecha y hora actual.
  Formato del ID: YYYYMMDDHHmmssSSSSS
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
  milisegundo = str(fecha_hora_actual.microsecond)[:5]
  num_random = random.randint(10**18, 10**19 - 1) #19 digitos enteros
  # Concatenación para formar el ID único
  id_scan_inter = f"{anio}{mes}{dia}{hora}{minuto}{segundo}{milisegundo}"
  id_scan = hashlib.sha256(
        ( str(id_scan_inter) + str(num_random)).encode()
    ).hexdigest()
  

  return id_scan  

#convierte el ficheroofimatico en texto plano apra tratarlo
def convert_txt(info_file):
  path_txt = info_file["path_complete"]
  contenido=[]
  if info_file["extension"]=="TXT":
      with open(path_txt,"r") as archivo:
        contenido=archivo.read()
      archivo.close()
      return contenido
  else: 
    file_data = parser.from_file(path_txt)
    contenido = file_data['content']
    return contenido  

def add_Metadata_GDPR (p1,e1,result_GDPR):
  OK_Meta= False  
  
  for result in result_GDPR:
      
    coment = result[0]
          
    if e1== "DOCX" or "DOC":  
      try:   
        file_meta= docx.Document(p1)
        propiedades = file_meta.core_properties
        
        if propiedades.comments is not None:
          propiedades.comments += "\n" + coment
        else:
          propiedades.comments = coment
        
        file_meta.save(p1)
        OK_Meta=True
        print("GUARDADO METADATO:", coment, p1)
        
      except Exception as e:
        print(f"Error: {e}")
    
        
    elif e1 == "XLS" or "XLSX":
      try:
        libro = openpyxl.load_workbook(p1)
        propiedades = libro.properties
        
        if propiedades.description is not None:
          propiedades.description += "\n" + coment
        else:
          propiedades.description = coment
        
        libro.save(p1)
        OK_Meta=True
        print("GUARDADO METADATO:", coment,p1)
        
      except Exception as e:
        print(f"Error: {e}")
    elif e1=="PPT" or "PPTX":
      try:
        presentacion = Presentation(p1)  
        propiedades = presentacion.core_properties
        propiedades.comments = coment
        presentacion.save(p1)
        
        OK_Meta=True
        print("GUARDADO METADATO:", coment,p1)
        
      except Exception as e:
        print(f"Error: {e}")
    #elif file_extension == "PDF":
      
      
      
         
  
  return OK_Meta  
  
def add_Metadata_Pattern (p1,e1,pattern_value):
  OK_Meta=False
  
  if e1== "DOCX" or "DOC":  
      try:   
        file_meta= docx.Document(p1)
        propiedades = file_meta.core_properties
        
        if propiedades.comments is not None:
          propiedades.comments += "\n" + pattern_value
        else:
          propiedades.comments = pattern_value
        
        file_meta.save(p1)
        OK_Meta=True
        print("GUARDADO METADATO:", pattern_value, p1)
        
      except Exception as e:
        print(f"Error: {e}")
  elif e1 == "XLS" or "XLSX":
    try:
      libro = openpyxl.load_workbook(p1)
      propiedades = libro.properties
      
      if propiedades.description is not None:
        propiedades.description += "\n" + pattern_value
      else:
        propiedades.description = pattern_value
      
      libro.save(p1)
      OK_Meta=True
      print("GUARDADO METADATO:", pattern_value,p1)
    except Exception as e:
      print(f"Error: {e}")
  elif e1=="PPT" or "PPTX":
    try:
      presentacion = Presentation(p1)  
      propiedades = presentacion.core_properties
      propiedades.comments = pattern_value
      presentacion.save(p1)
      
      OK_Meta=True
      print("GUARDADO METADATO:", pattern_value,p1)
      
    except Exception as e:
      print(f"Error: {e}")
    #elif file_extension == "PDF": 
   
   
   
   
   
   
   
  return OK_Meta
    
def Get_Exp_reg(value0,value1):
  """
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
  """
  query="SELECT [RE_Name],[RE_Expression] FROM REG_EXP"
  if value0 is True and value1 is False:
    query= query + " WHERE EDITABLE=0"
  elif value0 is False and value1 is True:
    query= query + " WHERE EDITABLE=1"
    
  try:
    conn = pyodbc.connect(cadena_conexion)
    cursor = conn.cursor()
    cursor.execute(query)
    expresiones_regulares = cursor.fetchall()
    conn.commit()
    conn.close()
    #messagebox.showinfo("Success", "Main Registration successful!")
  except Exception as e:
    messagebox.showerror("Error", f"Main Registration failed: {e}")
       
  
  
  return expresiones_regulares
           
#añadir las expresiones encontradas a la BD
def add_GDPR_BD(result_GDPR, IDF,IDS, OK_Meta):
  
  conn = pyodbc.connect(cadena_conexion)
    
  for result in result_GDPR:
    type_value=result[0]
    type_infotypes=result[1]
    print("1: ", result)
    for type_infotype in type_infotypes:
      try:
        print("añadir: ", type_value, " y " , type_infotype)
        
        cursor = conn.cursor()
        cursor.execute("INSERT INTO dbo.Scan_Details_GDPR (ID_Document,ID_Scan,Type,Infotype, Metadata) VALUES (?,?,?,?,?)",(IDF, IDS,type_value, type_infotype,OK_Meta))
        conn.commit()
        #messagebox.showinfo("Success", "Details SCAN GDPR Complete PARTIAL! 295")
      except Exception as e:
        messagebox.showerror("Error", f"Document Registration failed: {e}")
  conn.close()
  #messagebox.showinfo("Success", "Details SCAN GDPR Complete! 325")
  pass
  
#añade a la BD los patrones encontrados en los documentos
def add_Pattern_BD (pattern_value,IDF,IDS,OK_Meta2):
  conn = pyodbc.connect(cadena_conexion)
  try:
    print("añadir: ", pattern_value)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO dbo.Scan_Details_Pattern (ID_Document,ID_Scan,Pattern,Metadata) VALUES (?,?,?,?)",(IDF, IDS,pattern_value,OK_Meta2))
    conn.commit()
              
  except Exception as e:
   messagebox.showerror("Error", f"Document Registration failed: {e}")
  conn.close()
  
  #messagebox.showinfo("Success", "Details SCAN Pattern Complete!")

#busca expresiones regulares en texto plano
def Search_GDPR(texto_plano,expresiones_regulares):
    
  # Lista para almacenar las expresiones regulares encontradas
  resultados = []
  print (f"EXPREG son:,{expresiones_regulares}")
  
  # Recorrer las expresiones regulares
  for nombre,expresion_regular in expresiones_regulares:
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

 #funcion de botón de path

#funcion de boton de busqueda de path
def explorar_ruta():
  ruta = filedialog.askdirectory()
  path_seach.set(ruta)

#marca todas las opciones de extensiones
def select_all_check():
  for checkbox in checkboxes:
    checkbox.set(True)

#desmarca todas las opciones de extensiones        
def deselect_all_check():
  for checkbox in checkboxes:
    checkbox.set(False)
       
       
"""
  Funciones Principales
  EXIT: salir de la aplicacion
  SEARCH: busqueda de ficheros segun ruta, patron, etc.
  REPORTS: reportes de ficheros ya buscados.

"""


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
  
  
  if gdpr_value is False and pattern_value == "" and expreg_value is False:
    print (pattern_value)
    print (f"Valor de GDPR es: ",{gdpr_value})
    print (f"Valor de Personalizada es: ",{expreg_value})
    messagebox.showerror ("Error","All options cannot be empty. Choose GDPR, Custom Regular Expressions and/or enter a valid pattern")
    return
  
  
  # Lista de extensiones a buscar
  #extensions = ["DOC", "PDF", "DOCX","XLS","XLSX","RTF","PPT","PPTX","CSV","TXT"] 
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


  print("la lista de extensiones final es: ", extensions)  
  #esta funcion guarda los registros del formulario inicial, comprobando que el path funciona
  
  ID_Scan_value = storage_data_main()
   
  Files_list=[]
  Files_list = buscar_archivos(path_search_value,extensions,file_large_value,recursive_value)
  
  #comprobar que la lista no es vacia
  if len(Files_list) > 0:
    print("La lista no está vacía.")
    File_List_Full = storage_data_documents(Files_list, ID_Scan_value)
    
  else:
    print("La lista está vacía. No hemos encontrado archivos válidos para las extensiones predeterminadas")
    return
    
  print ("Numero de archivos a Revisar: ", len(File_List_Full))
  
  for i in range (len(File_List_Full)):
            
    print("Fichero num: ",i, "de ", len(File_List_Full))
    print(File_List_Full[i])
    print("Lanzamos conversion de texto")
    
    file_txt = convert_txt (File_List_Full[i])
      
    
    #print ("IMPRESION DEL TEXTO: ")
    #print (file_txt)
    print( "FIN TEXTO")
    OK_Meta1 =False
    OK_Meta2 =False
    IDF = File_List_Full[i]["ID_Document"]
    IDS = File_List_Full[i]["ID_Scan"]
    e1= File_List_Full[i]["extension"]
    p1=File_List_Full[i]["path_complete"]
            
    if gdpr_value is True or expreg_value is True:
      
        expresiones_regulares=Get_Exp_reg(gdpr_value,expreg_value)
      
        result_GDPR = Search_GDPR (file_txt,expresiones_regulares)
        #messagebox.showinfo("GDPR Search", "GDPR search successful")
        
        print("El resultado de la busqueda GDPRes: ", result_GDPR)
        
        if len(result_GDPR) > 0:
          if metadata_value:
            #meter metadatos y ver si tiene metadatos
            #e1= File_List_Full[i]["extension"]
            #p1=File_List_Full[i]["path_complete"]
            OK_Meta1 = add_Metadata_GDPR (p1,e1,result_GDPR)
      
        print ("IDFICHERO",IDF,"IDSCAN", IDS)      
        add_GDPR_BD(result_GDPR, IDF,IDS,OK_Meta1 )
        print("GDPR guardado")
        
        
      
    if pattern_value != "":
      result_Pattern = Search_Pattern(file_txt,pattern_value)
      #messagebox.showinfo("Pattern Search", "Pattern search successful")
      if result_Pattern:
        print("Se han encontrado coincidencias. ")
        
        OK_Meta2 = add_Metadata_Pattern (p1,e1,pattern_value)
        add_Pattern_BD (pattern_value,IDF,IDS,OK_Meta2)
        print("Pattern guardado")
        
        
        
        
      else:
        print("No se han encontrado coincidencias. ")
      
  messagebox.showinfo("BUSQUEDA FINALIZADA", "BUSQUEDA FINALIZADA")
  
  
  
      
      
      
      
  pass

# Función para generar reportes

def back_user():
    window.destroy()
    runpy.run_path("TFG_TKINTER\\users.py")
    
    return   
   
  
  


def abrir_Main_search():
    
  heading_label = tks.Label(window, text="PatroniX Search Tool", font=("Arial", 30, "bold"), bg='#151547',fg="white").place(x=270,y=5)

  path_searchtk_label = tks.Label(text="Type a seach path:", font=font_1,bg='#151547',fg="white", anchor="w").place(x=30,y=80)
  path_searchtk_label2 = tks.Label(text="Format: U:\\ folder\\ folder2", font=font_0,bg='#151547',fg="white", anchor="w").place(x=230,y=105)
  path_searchtk_boton = tks.Button(text="Search", command=explorar_ruta, font=font_1C).place(x=805,y=75)

  patron_busqueda_label = tks.Label(text="Search Pattern:", font=font_1,bg='#151547',fg="white", anchor="w").place(x=30,y=130)
  patron2_busqueda_label = tks.Label(text="(distinguishes uppercase from lowercase)", font=font_0,bg='#151547',fg="white", anchor="w").place(x=230, y=155)

  path_searchtk_entry = tks.Entry(textvariable=path_seach,font=font_1, width=50).place(x=230, y=80)
  patron_busqueda_entry = tks.Entry(textvariable=pattern,font=font_1, width=30).place(x=230, y=130)

  # Crear el checkbotón GDPR
  gdpr_checkbutton = tks.Checkbutton(text="", variable=gdpr, font=font_1,bg='#151547',fg="red").place (x=30,y=180)
  gdpr_label = tks.Label(text="Do you want to search for Spanish GDPR regular expressions?", font=font_1,bg='#151547',fg="white", anchor="w").place(x=54,y=183)

  #Lista de expresione regulares
  expreg_checkbutton=tks.Checkbutton (text="",variable=expreg_check,font=font_1,bg='#151547',fg="red").place (x=30,y=220)
  expreg_label =tks.Label(text="Do you want to include custom Regular Expressions in the search?", font=font_1,bg='#151547',fg="white", anchor="w").place(x=54,y=223)
 
  # Crear el cherckbutton Ficheros Largos
  file_large_checkbutton= tks.Checkbutton(text="", variable=file_large, font=font_1,bg='#151547',fg="red").place(x=30, y=260)
  file_large_label = tks.Label(text="Do you want to include a file larger than 20 MB in size in the search?", font=font_1,bg='#151547',fg="white", anchor="w").place(x=54,y=263)

  #Hacer la busqueda recursiva
  recursive_checkbutton=tks.Checkbutton(text="",variable=recursive,font=font_1,bg='#151547',fg="red").place(x=30, y=300)
  recursive_label= tks.Label(text="Do you want to do the recursive search? ",font=font_1,bg='#151547',fg="white", anchor="w").place(x=54,y=303)
  
  #Hacer la busqueda recursiva
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
   
  # Crear los botones
  buscar_button = tks.Button(text="Search", command=busqueda, font=font_1B).place(x=90,y=420)
  exit_button = tks.Button(text="Back to User Panel", command=back_user, font=font_1B).place(x=290,y=420)
  
  window.mainloop()

#COMIENZA PROCESO CENTRAL
  
abrir_Main_search()
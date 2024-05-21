import pyodbc
import sys

def connection_db():

    config_filename = 'TFG_TKINTER\\config.env'
    config = {}
    try:
        with open(config_filename, 'r') as file:
            for line in file:
                key, value = line.strip().split('=')
                config[key.strip()] = value.strip()
            
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {config_filename}")
        sys.exit()
    except Exception as e:
        print(f"Error al leer el archivo {config_filename}: {e}")
        sys.exit()
   
    server = config['server']
    database = config['database']
    username = config['username']
    password = config['password']
    # Crear una conexión para mas adelante
    cadena_conexion = f'Driver={{SQL Server}};Server={server};Database={database};Uid={username};Pwd={password}'
    
    return (cadena_conexion)


def cargar_datos_vista():
    cadena_conexion=connection_db()
    conn = pyodbc.connect(cadena_conexion)
    cursor = conn.cursor()
    cursor.execute("SELECT RE_Name, RE_Expression, Editable FROM Reg_Exp order by editable")
    datos = cursor.fetchall()
    conn.close()
    return datos

def check_db (cadena_conexion):
  
  # Conectarse a la base de datos
  try:
      conexion = pyodbc.connect(cadena_conexion)
      return True
  except pyodbc.Error as e:
      print("Error al conectar:", e)
      return False
  finally:
    conexion.close()    
 
       
if __name__ == "__main__":
    connection_db()
    check_db()
    cargar_datos_vista()
"""
server = config['server']
database = config['database']
username = config['username']
password = config['password']
"""    
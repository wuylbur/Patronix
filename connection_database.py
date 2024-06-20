#this code is part of the Final Degree Project in UNIR by Gonzalo Castro

#module that makes accessing ODBC databases simple
import pyodbc

#This module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter
import sys

def connection_db(): #take the configuration data and create the connection with the database
    config_filename = 'config.env'
    config = {}
    try:
        with open(config_filename, 'r') as file:
            for line in file:
                key, value = line.strip().split('=')
                config[key.strip()] = value.strip()
            
    except FileNotFoundError:
        print(f"Error: Could not find file {config_filename}")
        sys.exit()
    except Exception as e:
        print(f"Error reading file {config_filename}: {e}")
        sys.exit()
   
    server = config['server']
    database = config['database']
    username = config['username']
    password = config['password']
 
    connection_string = f'Driver={{SQL Server}};Server={server};Database={database};Uid={username};Pwd={password}'
    
    return (connection_string)

def check_db (connection_string): #check if the database connection is correct
  try:
      conexion = pyodbc.connect(connection_string)
      return True
  except pyodbc.Error as e:
      print("Error to connect:", e)
      return False
  finally:
    conexion.close()    
       
if __name__ == "__main__":
    connection_db()
    check_db()
    
 
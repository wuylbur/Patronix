#this code is part of the Final Degree Project in UNIR by Gonzalo Castro

#This module provides a portable way of using operating system dependent functionality.
import os

#this module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.
import subprocess

#This module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter
import sys

config_filename = 'config.env' #read the file to know which path the PowerBI file is in 
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
    
ruta_pbix= config['ruta_pbix']      #path the PowerBI file

def reports():  #return the path of the file
  
  if os.path.exists(ruta_pbix):
    try:
      comando = ["C:\\Program Files\\WindowsApps\\Microsoft.MicrosoftPowerBIDesktop_2.128.1380.0_x64__8wekyb3d8bbwe\\bin\\PBIDesktop.exe", ruta_pbix]
      subprocess.Popen(comando)
      print("PBIX file successfully opened.")
    except Exception as e:
      print("Error to open PBIX file:", e)
        
  else:
      print("The .pbix file does not exist in the specified path.") 



if __name__ == "__main__":
    reports()
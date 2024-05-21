import os
import subprocess
import sys

config_filename = 'TFG_TKINTER\\config.env'
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
    
ruta_pbix= config['ruta_pbix']      

def reportes():
       
  #abrir_Report()
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
    reportes()
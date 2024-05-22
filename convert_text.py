from tika import parser

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

if __name__ == "__main__":
    
 convert_txt()

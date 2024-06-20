#this code is part of the Final Degree Project in UNIR by Gonzalo Castro


#import package (“Tk interface”) is the standard Python interface to the Tcl/Tk GUI toolkit. 
from tika import parser

def convert_txt(info_file): 
  """
  this function convert in plain texto any office file, but if the file is TXT extension, need a special method.
  """
  path_txt = info_file["path_complete"]
  content=[]
  if info_file["extension"]=="TXT":
      with open(path_txt,"r") as file:
        content=file.read()
      file.close()
      return content
  else: 
    file_data = parser.from_file(path_txt)
    content = file_data['content']
    return content  

if __name__ == "__main__":
    
 convert_txt()

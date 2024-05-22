import openpyxl
import docx
from pptx import Presentation

import sys
from odf.opendocument import load
from odf.meta import UserDefined


def add_Metadata_GDPR (p1,e1,result_GDPR):
  OK_Meta= False  
  
  for result in result_GDPR:
    comment = result[0]
          
    if e1 in ("DOCX", "DOC"):  
      try:   
        file_meta= docx.Document(p1)
        propiedades = file_meta.core_properties
        
        if propiedades.comments is not None:
          propiedades.comments += "\n" + comment
        else:
          propiedades.comments = comment
        
        file_meta.save(p1)
        OK_Meta=True
        print("GUARDADO METADATO:", comment, p1)
        
      except Exception as e:
        print(f"Error: {e}")
        
    elif e1 in  ("XLS","XLSX"):
      try:
        libro = openpyxl.load_workbook(p1)
        propiedades = libro.properties
        
        if propiedades.description is not None:
          propiedades.description += "\n" + comment
        else:
          propiedades.description = comment
        
        libro.save(p1)
        OK_Meta=True
        print("GUARDADO METADATO:", comment,p1)
        
      except Exception as e:
        print(f"Error: {e}")
    elif e1 in ("PPT", "PPTX"):
      try:
        presentacion = Presentation(p1)  
        propiedades = presentacion.core_properties
        propiedades.comments = comment
        presentacion.save(p1)
        
        OK_Meta=True
        print("GUARDADO METADATO:", comment,p1)
        
      except Exception as e:
        print(f"Error: {e}")

    elif e1 in ("ODS", "ODT", "ODP"):  
      try:   
        doc = load(p1)
        comment2= UserDefined(name="Comentario", text=comment)
        doc.meta.addElement(comment2)
        doc.save(p1)
        OK_Meta=True
        print("GUARDADO METADATO:", comment2, p1)
        
      except Exception as e:
        print(f"Error: {e}")   
   
  return OK_Meta  
  
def add_Metadata_Pattern (p1,e1,pattern_value):
  OK_Meta=False
  
  if e1 in ("DOCX", "DOC"):  
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
  elif e1 in  ("XLS","XLSX"):
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
  elif e1 in ("PPT", "PPTX"):
    try:
      presentacion = Presentation(p1)  
      propiedades = presentacion.core_properties
      propiedades.comments = pattern_value
      presentacion.save(p1)
      
      OK_Meta=True
      print("GUARDADO METADATO:", pattern_value,p1)
      
    except Exception as e:
      print(f"Error: {e}")
    
  elif e1 in ("ODS", "ODT", "ODP"):  
      try:   
        doc = load(p1)
        comment2= UserDefined(name="Comentario", text=pattern_value)
        doc.meta.addElement(comment2)
        doc.save(p1)
        OK_Meta=True
        print("GUARDADO METADATO:", comment2, p1)
        
      except Exception as e:
        print(f"Error: {e}")   
   
  return OK_Meta

if __name__ == "__main__":
    add_Metadata_GDPR()
    add_Metadata_Pattern()
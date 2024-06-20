#this code is part of the Final Degree Project in UNIR by Gonzalo Castro

#This module provides a portable way of using operating system dependent functionality
import os

#import package (“Tk interface”) is the standard Python interface to the Tcl/Tk GUI toolkit. 
from tkinter import messagebox


def verify(path):
  """
check the path where we should search for office files 
  """
  if not path:
    messagebox.showerror("Error", "Please enter all details about Path or Pattern correctly.")
    return  False
    #ruta2=Path(ruta)
  return os.path.exists(path)



if __name__ == "__main__":
    verify()
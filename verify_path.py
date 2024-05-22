import os
from tkinter import messagebox


def verify(ruta):
  if not ruta:
    messagebox.showerror("Error", "Please enter all details about Path or Pattern correctly.")
    return  False
    #ruta2=Path(ruta)
  return os.path.exists(ruta)



if __name__ == "__main__":
    verify()
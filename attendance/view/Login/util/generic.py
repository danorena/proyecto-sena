from tkinter import PhotoImage
from PIL import ImageTk, Image

# Redimensionar una imagen, la funcion recibe dos arg que son ruta y tamaño de la imagen a poner

def readImage(path,size):
    return ImageTk.PhotoImage(Image.open(path).resize(size, Image.ANTIALIAS))


# Centrar las ventanas

def centerWindows(window, width,height):

    actualWidth = window.winfo_screenwidth()
    actualHeight = window.winfo_screenheight()

    x = int((actualWidth/2) - (width/2))
    y = int((actualHeight/2)- (height/2))

    return window.geometry(f"{width}x{height}+{x}+{y}")

    
"""
Importamos librerías, tk para hacer el form y la screen, bold para el tipo de letra y util.generic para la imagen y calcular el centro de la ventana
"""
from email.mime import image
import tkinter as tk
from tkinter.font import BOLD

import sys
sys.path.append('../')
import util.generic as utl
from controller.path import path

class MasterPanel():

    def __init__(self):
        
        self.window = tk.Tk()
        self.window.title("Master Panel")
        w,h = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.geometry(("%dx%d+0+0") % (w, h))
        self.window.config(bg= "#F2E6E6")
        self.window.resizable(width=0,height=0)

        firstPath = path()
        secondPath = 'view//Login//images//attendance01.png'
        imagePath = firstPath + secondPath
        logo = utl.readImage(imagePath,(200,200))

        label = tk.Label(self.window, image = logo, bg = '#F2E6E6')

        label.place(x=0,y=0,relwidth=1,relheight=1)
        self.window.mainloop()
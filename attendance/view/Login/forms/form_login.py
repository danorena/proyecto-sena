# NO INICIAR, SOLO FUNCIONA CON LA RUTA DEL MAIN.

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD

# Importar util.generic y home

import sys
sys.path.append('../../')
import view.Login.util.generic as utl 
from view.Login.home import Home
from controller.path import path
from controller.controllerLogin import log

class App():

    # Funcion para verificar los datos ingresados
    def verify(self):
        userV = self.user.get()
        password = self.password.get()
        
        valid = log(userV,password)
        if (valid==True) :
            self.window.destroy()
            Home()
        else:
            messagebox.showerror(message="Los datos proporcionados son Incorrectos, intente denuevo", title="Incorrecto!")

    def __init__(self):
        self.window=tk.Tk()
        self.window.title("Smart Attendance Login")
        wSize = self.window.winfo_screenwidth()
        hSize = self.window.winfo_screenheight()
        self.window.geometry("%dx%d" % (wSize, hSize))
        self.window.config(bg = "#f0f1ee")
        self.window.resizable(width=0,height=0)
        utl.centerWindows(self.window,wSize,hSize)


        # Acá ajustamos que el masterForm se coloque a la derecha // RIGHT SIDE
        # LOGO
        firstPath = path()
        secondPath = 'view//Login//images//attendance01.png'
        imagePath = firstPath + secondPath
        logo = utl.readImage(imagePath,(300,300))
        frameLogo = tk.Frame(self.window, bd=0, width = 600 ,height=hSize, relief=tk.SOLID, padx=10 , pady = 10, bg = "#f0f1ee")
        frameLogo.pack(side="right",expand=tk.NO,fill=tk.BOTH)
        label = tk.Label(frameLogo, image = logo, bg= "#f0f1ee")
        label.place(x=0,y=0,relwidth=1,relheight=1)
        
        # LEFT SIDE

        frameForm = tk.Frame(self.window, bd=0, width=400, relief=tk.SOLID, padx=10 , pady = 10, bg = "#3894a1")

        frameForm.pack(side="right",expand=tk.YES,fill=tk.BOTH)
        

        # TOP LEFT SIDE

        frameFormTop = tk.Frame(frameForm, height=50, bd=0,relief=tk.SOLID, bg = "black")

        frameFormTop.pack(side="top",fill=tk.X)
        
        title = tk.Label(frameFormTop, text = "Iniciar Sesión", font=('Roboto 30 bold'), fg= "#f0f1ee", bg= '#3894a1', pady=50)

        title.pack(expand=tk.YES,fill=tk.BOTH)
        
        # BOTTOM LEFT SIDE
        frameFormBottom = tk.Frame(frameForm, height=50, bd=0,relief=tk.SOLID, bg = "#3894a1")

        frameFormBottom.pack(side="bottom",expand=tk.YES,fill=tk.BOTH)

        
        # Input Usuario
        userLabel = tk.Label(frameFormBottom,text="Usuario",font=('Roboto 15'), fg="#f0f1ee", bg="#3894a1", anchor = "w")

        userLabel.pack(fill=tk.X, padx= 20 , pady= 5)
        
        self.user = ttk.Entry(frameFormBottom, font=("Roboto 15"))
        
        self.user.pack(fill=tk.X, padx= 20, pady=5)

        # Input Password

        passwordLabel = tk.Label(frameFormBottom,text="Contraseña",font=('Roboto 15'), fg="#f0f1ee", bg="#3894a1", anchor = "w")

        passwordLabel.pack(fill=tk.X, padx= 20 , pady= 5)
        
        self.password = ttk.Entry(frameFormBottom, font=("Roboto 15"))
        
        self.password.pack(fill=tk.X, padx= 20, pady=5)
        
        self.password.config(show="*")

        # Boton Iniciar Sesion

        btnLogin = tk.Button(frameFormBottom, text="Iniciar Sesion", font=("Roboto 15 bold"),bd=0 ,fg="#f0f1ee", bg="#2f404f", command=self.verify)

        btnLogin.pack(fill=tk.X, padx=50, pady=50)
        btnLogin.bind('<Return>', (lambda event: self.verify()))


        
        
        
        # COLORES #2f404f , #3894a1 , #f0f1ee , #c7dad3 
        self.window.mainloop()

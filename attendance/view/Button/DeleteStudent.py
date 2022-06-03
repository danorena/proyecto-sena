import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD

import sys

from controller.deleteStudent import delete
sys.path.append('../../')
from controller.Group import Group


class DeleteStudent():
    def __init__(self):

        # Creación de la ventana
        self.window=tk.Tk()
        self.window.title("Eliminar Aprendiz")
        wSize = self.window.winfo_screenwidth()
        hSize = self.window.winfo_screenheight()
        self.window.geometry("%dx%d" % (wSize, hSize))
        self.window.config(bg = "#f0f1ee")
        self.window.resizable(width=0,height=0)

        # Titulo

        frameTitle = tk.Frame(self.window, height=10, bd=0,relief=tk.SOLID, bg = "#3894a1")
        frameTitle.pack(expand=tk.YES,fill=tk.BOTH)
        
        title = tk.Label(frameTitle, text = "Eliminar Aprendiz", font=('Roboto 30 bold'), fg= "#f0f1ee", bg= '#3894a1',pady = 20)
        title.pack(fill=tk.BOTH)

        # Frame e Inputs 

        frameInputs = tk.Frame(self.window, height=500, bd=0,relief=tk.SOLID, bg = "#3894a1")
        frameInputs.pack(side="top",fill=tk.BOTH,expand=tk.YES)
            # ID
        

            # NOMBRE
        nameLabel = tk.Label(frameInputs,text="Nombre Completo",font=('Roboto 15'), fg="#f0f1ee", bg="#3894a1", anchor = "w")
        nameLabel.pack(fill=tk.X, padx= 20 , pady= 5)
        
        self.name = ttk.Entry(frameInputs, font=("Roboto 15"))
        self.name.pack(fill=tk.X, padx= 20, pady=5)

        # FICHA
        """
        Para hacer que funcione de manera efectiva vamos a hacer uso de la libreria OS
        y leemos todas las carpetas que hay disponibles, ya que estas corresponden a las fichas
        
        ttk funciona con los sgtes params (vetana-Frame, variableGuardaOpt, default=None, *values, **kwargs)
        """
        ficha = Group()
        options = ficha.search()
        default = ("Porfavor seleccione la ficha a la que pertenece","----------------------------------------------------------------------------------------------------------------------------------------")
        
        opt = tk.StringVar(frameInputs)
        self.opt = opt
        optInput = ttk.OptionMenu(frameInputs,opt,default[0],*options)
        menu_width = len(max(default, key=len))
        optInput.pack(pady=30, ipadx=10)
        optInput.config(width=menu_width)
        
        # Botones
        frameBtn = tk.Frame(self.window, height=50, bd=0,relief=tk.SOLID, bg = "#3894a1")
        frameBtn.pack(side="bottom",expand=tk.YES,fill=tk.BOTH)

            # Volver
        btnVolver = tk.Button(frameBtn, text="Volver", font=("Roboto 15 bold"),bd=0 ,fg="#f0f1ee", bg="#2f404f",command=self.back)
        btnVolver.pack(side ='left', padx= 250)
        btnVolver.config(width=20, height = 2)
            
            # Registrar
        btnRegistrar = tk.Button(frameBtn, text="Eliminar", font=("Roboto 15 bold"),bd=0 ,fg="#f0f1ee", bg="#2f404f",command=self.studentName)
        btnRegistrar.pack(side ='right', padx= 250)
        btnRegistrar.config(width=20, height = 2)

        self.window.mainloop()
        # COLORES #2f404f , #3894a1 , #f0f1ee , #c7dad3
    def back(self):
        from controller.back import volver
        self.window.destroy()
        volver()
# Metodo para eliminar el usuario, recibe el id y la ficha
    def delete(self,id,ficha):
        from controller.unEnroll import unEnroll
        unEnroll(id,ficha)
        messagebox.showinfo(message= f'El aprendiz {self.showName} ha sido eliminado',title='Aprendiz Eliminado!')
# Metodo para obtener el nombre del aprendiz y a su vez evaluamos si existe o no
    def studentName(self):
        from controller.deleteStudent import delete
        name = self.name.get()
        wasDeleted = delete(name,self.opt.get())
        self.showName = wasDeleted[1]
        if wasDeleted[0] != False:
            self.delete(wasDeleted[0],self.opt.get())
        else:
            messagebox.showerror(message= f'El aprendiz {self.showName} no existe',title='Nombre Invalido!')
        
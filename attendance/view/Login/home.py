import atexit
from lib2to3.pgen2.token import AT
import tkinter as tk
from tkinter.font import BOLD

import sys
sys.path.append('../../')

import view.Login.util.generic as utl
from controller.path import path

class Home():
    
    # Creacion de la ventana o window
    def __init__(self):

        self.window=tk.Tk()
        self.window.title("Smart Attendance Home")
        # self.window.geometry("800x500")
        wSize = self.window.winfo_screenwidth()
        hSize = self.window.winfo_screenheight()
        self.window.geometry("%dx%d" % (wSize, hSize))
        self.window.config(bg = "#f0f1ee")
        self.window.resizable(width=0,height=0)
        utl.centerWindows(self.window,wSize,hSize)

        # LOGO
        firstPath = path()
        secondPath = 'view//Login//images//attendance02.png'
        imagePath = firstPath + secondPath
        logo = utl.readImage(imagePath,(150,150 ))
        frameLogo = tk.Frame(self.window, bd=0, width=wSize, height= 200, relief=tk.SOLID, pady = 10)
        frameLogo.pack(side="top",expand=tk.NO,fill=tk.BOTH)
        label = tk.Label(frameLogo, image = logo, bg= "#f0f1ee")
        label.place(x=0,y=0,relwidth=1,relheight=1)
        



        # FRAME REGISTRAR
        frameEnroll = tk.Frame(self.window, bd=0, width=wSize, height= 200, relief=tk.SOLID, pady = 10)
        frameEnroll.pack(side="top",expand=tk.NO,fill=tk.BOTH)
        
        # BOTONES REGISTRAR
        # ---------- Aprendiz -------------
        btnEnrollStudent = tk.Button(frameEnroll, text="Registrar Aprendiz", width = 20 , height= 2, font=("Roboto 15 bold"),bd=0 ,fg="#f0f1ee", bg="#2f404f", command=self.studentEnroll)
        btnEnrollStudent.pack(side = "left",fill=tk.Y, padx= 250, pady = 70)
        # ---------- Ficha -------------
        btnEnrollGroup = tk.Button(frameEnroll, text="Registrar Ficha", width = 20 , height= 2, font=("Roboto 15 bold"),bd=0 ,fg="#f0f1ee", bg="#2f404f", command=self.groupEnroll)
        btnEnrollGroup.pack(side = "right",fill=tk.Y, padx= 250, pady = 70)

        




        # FRAME ELIMINAR
        frameDelete = tk.Frame(self.window, bd=0, width=wSize, height= 200, relief=tk.SOLID, pady = 10)
        frameDelete.pack(side="top",expand=tk.NO,fill=tk.BOTH)
        # BOTONES ELIMINAR
        # ---------- Aprendiz -------------
        btnDeleteStudent = tk.Button(frameDelete, text="Eliminar Aprendiz", width = 20 , height= 2, font=("Roboto 15 bold"),bd=0 ,fg="#f0f1ee", bg="#2f404f", command=self.studentDelete)
        btnDeleteStudent.pack(side = "left",fill=tk.Y, padx= 250, pady = 70)
        # ---------- Ficha -------------
        btnDeleteGroup = tk.Button(frameDelete, text="Eliminar Ficha",width = 20 , height= 2, font=("Roboto 15 bold"),bd=0 ,fg="#f0f1ee", bg="#2f404f", command=self.groupDelete)
        btnDeleteGroup.pack(side = "right",fill=tk.Y, padx= 250, pady = 70)

        




        # FRAME TOMAR ASISTENCIA
        frameAttendance = tk.Frame(self.window, bd=0, width=wSize, height= 200, relief=tk.SOLID, pady = 10)
        frameAttendance.pack(side="top",expand=tk.NO,fill=tk.BOTH)


        # BOTON ASISTENCIA
        btnAttendance = tk.Button(frameAttendance, text="Tomar Asistencia", width = 20 , height= 2, font=("Roboto 15 bold"),bd=0 ,fg="#f0f1ee", bg="#2f404f", command=self.atendance)
        btnAttendance.pack(fill=tk.Y, padx= 300, pady = 70)
        
        
        # COLORES #2f404f , #3894a1 , #f0f1ee , #c7dad3
        self.window.mainloop()

    # Ir a Registrar Aprendiz
    def studentEnroll(self):
        from controller.enroll import enrollStudent
        self.window.destroy()
        enrollStudent()
        
    # Ir a Eliminar Aprendiz
    def studentDelete(self):
        from controller.delete import deleteStudent
        self.window.destroy()
        deleteStudent()

    # Ir a Registrar Ficha
    def groupEnroll(self):
        from controller.enroll import enrollGroup
        self.window.destroy()
        enrollGroup()

    # Ir a Eliminar Ficha
    def groupDelete(self):
        from controller.delete import deleteGroup
        self.window.destroy()
        deleteGroup()

    # Ir a Tomar Asistencia
    def atendance(self):
        from controller.AttendanceController import Attendance
        self.window.destroy()
        asistencia = Attendance()
        asistencia.attendanceFunction()


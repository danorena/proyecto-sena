import os
import shutil
from controller.path import path
from tkinter import messagebox
class Group():
    # Buscar la ficha
    def search(self):
        # Donde se va a buscar 
        firstPath = path()
        secondPath = 'model\\datasets\\attendance_system_dataset'
        folder = firstPath + secondPath
        
        # Creamos una lista para agregar todos los directorios
        folderList = []
        
        # Recorremos la ruta de folder, y la agregamos a la lista
        for file_name in os.listdir(folder):
            folderList.append(file_name)
        
        # Le damos el valor de la lista a una variable
        list = folderList
        # Devolvemos los valores para hacer uso de estos
        return list

    # Registrar Ficha
    def enroll(self,name):
        from controller.config import conf
        firstPath = path()
        secondPath = 'model\\datasets\\attendance_system_dataset\\'
        folder = firstPath + secondPath + name
        os.mkdir(folder)
        
        # Carpetas necesarias en cada ficha, config, output, config 
        dbFolder = folder + '\\database'
        os.mkdir(dbFolder)
        
        outputFolder = folder + '\\output'
        os.mkdir(outputFolder)
        
        configFolder = folder + '\\config'
        os.mkdir(configFolder)

        open(f'{folder}\\actual.txt','w').close()
        
        model = open(f'{folder}\\model.txt','w')
        model.write('0')
        model.close()
        
        conf.config(name)
        
        messagebox.showinfo(message="La ficha fue registrada correctamente", title="Ficha Registrada!")

    # Eliminar Ficha
    def delete(self,name):
        firstPath = path()
        secondPath = 'model\\datasets\\attendance_system_dataset\\'
        folder = firstPath + secondPath + name
        shutil.rmtree(folder)
        messagebox.showerror(message="La ficha fue eliminada correctamente", title="Ficha Eliminada!")



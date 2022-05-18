from email.encoders import encode_noop
from operator import le
import sys
import os
from xml.etree import ElementPath
sys.path.append('../')

def config(ficha):
    import shutil
    from controller.path import path
    import json
    # C:\Users\Proyecto\Desktop\attendance\
    mainPath = path()
    # De donde proviene el archivo
    originalPath = mainPath + 'controller\\config\\config.json'
    # A donde va el archivo
    movePath = mainPath + 'model\\datasets\\attendance_system_dataset\\'+ ficha +'\\config\\config.json'
    # Moviendo el archivo
    shutil.copyfile(originalPath, movePath)
    
    # Cambiando los valores de config
    datasetPath = 'datasets/attendance_system_dataset'
    dbPath = datasetPath + '/' + ficha + '/database/attendance.json'
    encodingsPath = datasetPath + '/' + ficha + '/output/encodings.pickle'
    recognizerPath = datasetPath + '/' + ficha + '/output/recognizer.pickle'
    lePath = datasetPath + '/' + ficha + '/output/le.pickle'
    # que config vamos a abrir y editar
    jsonFile = open(movePath,"r")
    dataJson = json.load(jsonFile)
    jsonFile.close()
    
    jsonFile = open(movePath,"w")
    # Cambiamos los valores del config por los que necesitamos
    dataJson["class"] = ficha
    dataJson["db_path"] = dbPath
    dataJson["encodings_path"] = encodingsPath
    dataJson["recognizer_path"] = recognizerPath
    dataJson["le_path"] = lePath
    
    json.dump(dataJson, jsonFile)
    jsonFile.close()

    

    newPath = mainPath + '\\model'
    # Inicializamos la DB
    os.chdir(newPath)
    os.system('python initialize_database.py --conf datasets/attendance_system_dataset/'+ ficha +'/config/config.json')
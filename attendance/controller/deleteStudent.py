import sys
sys.path.append('../../')
# from path import path

def delete(n,ficha):
    # n = Usuario a buscar
    
    n = n.title()
    showName = n
    n = n.replace(" ","")
    # Importamos la ruta principal
    from controller.path import path
    
    # # Importamos la libreria de Json para que podamos abrir el file.json
    import json

    # Archivo a abrir
    fileJson = path() + f'model\\datasets\\attendance_system_dataset\\{ficha}\\database\\attendance.json'
    # Abriendo el archivo y cargando toda la info en una variable
    with open(fileJson) as f:
        data = json.load(f)
        
    info = []
    counter = 0
    # Recorriendo el diccionario, buscamos en stundent
    for student in data['student'].values():
        # En student buscamos la palabra
        for key , name in student.items():
            
            if name[0] == n:
                counter = 1
                # retornamos la informacion a una lista para hacer uso de ella en el llamado
                info = [key,showName]
                return info
                
    # Validamos que si exista el usuario para proceder a hacer el unenroll
    if counter != 1:
        # retornamos la informacion a una lista para hacer uso de ella en el llamado
        info = [False,showName]
        return info
    

# print(delete('ValentinaRamirezCuesta','01'))
    
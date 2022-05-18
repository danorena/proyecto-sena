def idMaker(nFicha):
        import os
        from controller.path import path
        firstPath = path()
        secondPath = 'model\\datasets\\attendance_system_dataset\\'
        
        # Recibiendo la ficha
        ficha = nFicha 
        lastPath = '\\'
        ficha += lastPath 
        folder = firstPath + secondPath + ficha
        id = '1'
        finalPath = firstPath + secondPath + ficha +  id
        
        # Verificamos la existencia del directorio 1
        existsDir = os.path.isdir(finalPath)
        
        if (existsDir == False):
            os.mkdir(finalPath)
            return id
        else:
            # Busca todos los directorios que hayan, y coge el último
            for file_name in os.listdir(folder):
                if file_name != 'config' and file_name != 'output' and file_name != 'database' and file_name != 'actual.txt' and file_name != 'model.txt':    
                    dir = file_name
    
            id = int(dir)
            id += 1
            id = str(id)
            folder += id
            os.mkdir(folder)

            return id
        
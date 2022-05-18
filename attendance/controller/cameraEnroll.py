import os
# from path import path

def enrollCameraStudent(id,name,ficha):
        from controller.path import path
        # Ruta desde la cual vamos a ejecutar el enroll.py
        firstPath = path()
        secondPath = f'model\\datasets\\attendance_system_dataset\\{ficha}\\actual.txt'
        entirePath = firstPath + secondPath
        
        actual = open(entirePath,"w")
        actual.write(id)
        actual.close()
        
        secondPath = 'model'
        entirePath = firstPath + secondPath
        os.chdir(entirePath)
        
        # Lo que le vamos a mandar a la terminal
        firstExecute = 'python enroll.py --id '
        secondExecute = id
        thirdExecute = ' --name '
        # Juntamos los espacios para que se guarde bien en el .json
        name = name.title()
        name = name.replace(" ","")
        fourthExecute = name
        fifthExecute = ' --conf '
        sixthExecute = 'datasets/attendance_system_dataset/'+ ficha +'/config/config.json'
        finalExecute = firstExecute+secondExecute+thirdExecute+fourthExecute+fifthExecute + sixthExecute
        os.system(finalExecute)

        # print(finalExecute)
        
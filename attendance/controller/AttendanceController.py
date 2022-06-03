import sys
sys.path.append('../../')


class Attendance():

    def attendanceFunction(self):
        from view.Button.Attendance import Attendance
        Attendance()

    def openCamera(self,ficha):
        from controller.path import path
        from threading import Thread
        import os 
        # Valoramos si es posible o no entrenar el modelo
        firstPath = path()
        
        # Abrimos y el archivo de actual.txt que nos dirá si hay un nuevo aprendiz
        secondPath = f'model\\datasets\\attendance_system_dataset\\{ficha}\\actual.txt'
        entirePath = firstPath + secondPath
        
        fActual = open(entirePath,'r')
        dataActual = fActual.read()
        fActual.close()
        
        # Abrimos el archivo model el cual nos dirá si hay que entrenar el modelo o no
        secondPath = f'model\\datasets\\attendance_system_dataset\\{ficha}\\model.txt'
        entirePath = firstPath + secondPath
        
        fModel = open(entirePath,"r")
        dataModel = fModel.read()
        fModel.close()
        
        if dataModel != dataActual:
            
            fModel = open(entirePath,"w")
            fModel.write(dataActual)
            fModel.close()
            
            secondPath = 'model'
            entirePath = firstPath + secondPath
            os.chdir(entirePath)
            
            # Sacar los puntos de la cara
            firstLine = 'python encode_faces.py --conf '
            secondLine = 'datasets/attendance_system_dataset/'+ ficha +'/config/config.json'
            finalLine = firstLine + secondLine
            os.system(finalLine)
        
            # Entrenar el modelo
            firstLine = 'python train_model.py --conf '
            secondLine = 'datasets/attendance_system_dataset/'+ ficha +'/config/config.json'
            finalLine = firstLine + secondLine
            os.system(finalLine)
        
        

        # Iniciar el servidor
        firstLine = 'python server.py --server-port 5555 --conf '
        secondLine = 'datasets/attendance_system_dataset/'+ ficha +'/config/config.json'
        finalLine = firstLine + secondLine
        os.chdir(f'{firstPath}model')
        os.system(f'start cmd /c {finalLine}')
        
        
        # Linea del CMD -- Tomar asistencia
        firstLine = 'python attendance.py --conf '
        secondLine = 'datasets/attendance_system_dataset/'+ ficha +'/config/config.json --server-ip localhost --server-port 5555'
        finalLine = firstLine + secondLine
        os.chdir(f'{firstPath}model')
        os.system(finalLine)
        
        
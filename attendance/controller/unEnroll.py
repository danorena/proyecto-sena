import sys

sys.path.append('../../')
def unEnroll(id,ficha):
    import os
    from controller.path import path
    
    # Ruta desde la cual vamos a ejecutar el enroll.py
    firstPath = path()
    secondPath = f'model\\datasets\\attendance_system_dataset\\{ficha}\\actual.txt'
    entirePath = firstPath + secondPath
    
    actual = open(entirePath,"w")
    actual.write(id)
    actual.close()
    
    # Linea del CMD -- Eliminar Aprendiz
    exc = path() + f'model'
    os.chdir(exc)
    os.system(f'python unenroll.py --id {id} --conf datasets/attendance_system_dataset/{ficha}/config/config.json')
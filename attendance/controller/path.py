import os

def path():

    path = os.getcwd()
    path = path.split('\\')
    entirePath = []
    for p in path:
        if (p == 'attendance'):
            break
        else:
            p += '\\'
            entirePath.append(p)
    entirePath.append('attendance\\')
    letter = ''    
    path = letter.join(entirePath)
    # Ruta que saca:
    # C:\Users\Proyecto\Desktop\attendance\
    return path


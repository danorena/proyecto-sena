from sqlite3 import connect
import sys
sys.path.append('../../')

def log(userV,password):
    from model.conection import Connect
    try:
        c = Connect()
        response = c.login(userV,password)
        return response
    except:
        print ("Error al llamar el login")
    
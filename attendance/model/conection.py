import mysql.connector as sql

class Connect():
    def conn(self):
        connected = sql.connect(
            user='root',
            password = '',
            host = 'localhost',
            database = 'usuarios'
            )
        return connected
    
    def login(self,tkUser,tkPass):
        db = self.conn()
        cursor = db.cursor()
        log = f"CALL `spLogin`('{tkUser}', '{tkPass}');"
        cursor.execute(log)
        valid = tuple(cursor.fetchall())
        if valid == ():
            return False
        else:
            return True
        
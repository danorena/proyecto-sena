import mysql.connector as sql

class Connect():
    def conn(self):
        connected = sql.connect(
            user='uempkk9vesxwg5af',
            password = 'dRzWyHluiDPzEZt68igL',
            host = 'b60lkhh7i47obofeagt8-mysql.services.clever-cloud.com',
            database = 'b60lkhh7i47obofeagt8'
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
        
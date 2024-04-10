import mysql.connector

class DatabaseConnectionManager:
    def __init__(self):
       self.cnx = None

    def connect(self):
        try:
            self.cnx = mysql.connector.connect(
            user='root', password='passW11!', host='127.0.0.1', database='library_management'
            )
        except mysql.connector.Error as err: print("Error connecting to database:", err)
            
    def get_cursor(self):
       if self.cnx is not None and self.cnx.is_connected(): return self.cnx.cursor()
       else: raise Exception("Database connection not established")

    def do_commit(self):
        self.cnx.commit()
       
    def close(self):
        if self.cnx is not None and self.cnx.is_connected(): self.cnx.close()
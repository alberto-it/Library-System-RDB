from connection_manager import DatabaseConnectionManager

class User:
    def __init__(self, name, library_id):
        self.__name = name
        self.__library_id = library_id
    
    def get_name(self):         return self.__name
    def get_library_id(self):   return self.__library_id

    def save_to_db(self):
        cnx = DatabaseConnectionManager()
        cnx.connect()
        cursor = cnx.get_cursor()

        sql = "insert into USERS (name, library_id) values (%s, %s)"
        values = (self.get_name(), self.get_library_id())

        try: cursor.execute(sql, values)
        except Exception as e: print("\nUser", self.get_name(), "Not Added! ERROR:", e)
        else:
            cnx.do_commit()
            print(f"\nThe User", self.get_name(), "has been added")

        cursor.close()
        cnx.close()
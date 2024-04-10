from connection_manager import DatabaseConnectionManager

class Author:
    def __init__(self, name, biography):
        self.__name = name
        self.__biography = biography

    def get_name(self):         return self.__name
    def get_biography(self):    return self.__biography
    
    def save_to_db(self):
        cnx = DatabaseConnectionManager()
        cnx.connect()
        cursor = cnx.get_cursor()

        sql = "insert into AUTHORS (name, biography) values (%s, %s)"
        values = (self.get_name(), self.get_biography())

        try: cursor.execute(sql, values)
        except Exception as e: print("\nAuthor", self.get_name(), "Not Added! ERROR:", e)
        else:
            cnx.do_commit()
            print(f"\nThe Author", self.get_name(), "has been added!")

        cursor.close()
        cnx.close()
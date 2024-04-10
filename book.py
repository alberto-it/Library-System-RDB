from connection_manager import DatabaseConnectionManager
from author import Author

class Book:
    def __init__(self, title, author_id, isbn, pub_dt):
        self.__title = title
        self.__author_id = author_id
        self.__isbn = isbn
        self.__publication_date = pub_dt
        self.__available = True

    def get_title(self):            return self.__title
    def get_author_id(self):        return self.__author_id
    def get_isbn(self):             return self.__isbn
    def get_publication_date(self): return self.__publication_date
    def available(self):            return self.__available
    
    def save_to_db(self):
        cnx = DatabaseConnectionManager()
        cnx.connect()
        cursor = cnx.get_cursor()

        sql = "insert into BOOKS (title, author_id, isbn, publication_date, availability) values (%s, %s, %s, %s, %s)"
        values = (self.get_title(), self.get_author_id(), self.get_isbn(), self.get_publication_date(), self.available())

        try: cursor.execute(sql, values)
        except Exception as e: print("\nBook", self.get_title(), "Not Added! ERROR:", e)
        else:
            cnx.do_commit()
            print("\nThe Book", self.get_title(), "has been added!")

        cursor.close()
        cnx.close()
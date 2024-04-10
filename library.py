from book import Book
from user import User
from author import Author
from connection_manager import DatabaseConnectionManager

import re

class Library:
    def valid_date(self, pub_date): return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", pub_date))

    def book_operations(self):
        print("\nBook Operations:\n 1. Add a new book\n 2. Borrow a book")
        print(" 3. Return a book\n 4. Search for a book\n 5. Display all books")

        choice = input("\nEnter your choice (1-5): ")
        while choice not in ['1','2','3','4','5']: choice = input(f"\nInvalid choice! Please enter a number between 1 and 5: ")

        cnx = DatabaseConnectionManager()
        cnx.connect()
        cursor = cnx.get_cursor()
            
        if choice == '1':
            author_name = input("\nEnter the AUTHOR of the Book to be Added: ")
            cursor.execute("select id from authors where name = %s", [author_name])
            author_id = cursor.fetchone()
            if author_id:
                title = input(f"\nEnter the {author_name} Book Title to be Added: ")
                isbn = input(f"\nEnter the ISBN for {title}: ")

                pub_dt = input("\nEnter the Publication Date (YYYY-MM-DD): ")
                while not self.valid_date(pub_dt): pub_dt = input("\nPlease re-enter using Date Format YYYY-MM-DD: ")

                new_book = Book(title, author_id[0], isbn, pub_dt)
                new_book.save_to_db()

            else: print("\nPlease add author", author_name, "to the library system prior to adding book!")

        elif choice == '2':
            library_id = input("\nEnter the LIBRARY ID of the Borrower/User: ")

            cursor.execute("select id, name from users where LIBRARY_ID = %s", [library_id])
            result = cursor.fetchone()
            if not result: print("\nLIBRARY ID Not Found!")
            else:
                user_id, user_name = result
                title = input("\nEnter the Exact Title of the Book to Borrow: ")
                cursor.execute("select id, availability from books where title = %s", [title])
                result = cursor.fetchone()
                if not result: print(f"\n{title} does Not Exist in the Library System!")
                else:
                    book_id, availabe = result
                    if not availabe: print(f"\n{title} is currently Checked Out!")
                    else:
                        borrow_dt = input("\nEnter the Borrow Date (YYYY-MM-DD): ")
                        while not self.valid_date(borrow_dt): borrow_dt = input("\nPlease re-enter using Date Format YYYY-MM-DD: ")

                        sql = "INSERT INTO borrowed_books (user_id, book_id, borrow_date, return_date) VALUES (%s, %s, %s, %s)"
                        values = (user_id, book_id, borrow_dt, None) # Blank Return Date (will be populated when book is returned)

                        try: cursor.execute(sql, values)
                        except Exception as e: print("\nBook", title, "NOT Checked Out! ERROR:", e)
                        else:
                            cursor.execute("update books set availability = False where id = %s", [book_id])
                            cnx.do_commit()
                            print(f"\nDone! {title} just checked out to {user_name}!")
             
        elif choice == '3':
            title = input("\nEnter the Exact Title of the Book to Return: ")

            cursor.execute("select id, availability from books where title = %s", [title])
            result = cursor.fetchone()
            if not result: print(f"\n{title} was Not Found in our Library System!")
            else:
                book_id, availabe = result
                if availabe: print("\nHmm? Cannot return a book that hasn't been checked out yet!")
                else:
                    return_dt = input("\nEnter the Return Date (YYYY-MM-DD): ")
                    while not self.valid_date(return_dt): return_dt = input("\nPlease re-enter using Date Format YYYY-MM-DD: ")
                    cursor.execute("update borrowed_books set return_date = %s where book_id = %s", [return_dt, book_id])
                    cursor.execute("update books set availability = True where id = %s", [book_id])
                    cnx.do_commit()
                    print(f"\nThanks for returning {title}!")            
        else:
            valid_input = True
            if choice == '4':
                print("\nEnter the Title of the Book to Find...")
                title = input("Partical search using wildcard (%) is allowed: ")
                if title == '%':
                    print("\nCannot enter just '%'. Use Book Operations #5 to Displays ALL Books")
                    valid_input = False
                else: cursor.execute("select title, author_id, isbn, publication_date, availability from books where title like %s", [title])
            else: cursor.execute("select title, author_id, isbn, publication_date, availability from books")
            
            if valid_input: 
                results = cursor.fetchall()
                if results:
                    for title, author_id, isbn, publication_date, availability in results: 
                        cursor.execute("select name from authors where id = %s", [author_id])
                        author = cursor.fetchone()
                        print(f"\nTitle:\t{title} ({['Borrowed','Available'][availability]})\nAuthor:\t{author[0]}\nISBN:\t{isbn}\nPublication Date: {publication_date}")
                else: print("\nNo Books found matching the search criteria." if choice == '4' else "\nThere are currently No Books in the Library System!")
                
        cursor.close()
        cnx.close()
                
    def user_operations(self):
        print("\nUser Operations:\n 1. Add a new user\n 2. View user details\n 3. Display all users")
        choice = input("\nEnter your choice (1-3): ")
        while choice not in ['1','2','3']: choice = input(f"\nInvalid choice! Please enter a number between 1 and 3: ")

        if choice == '1':
            user_name = input("\nEnter User Name: ")
            library_id = input(f"\nEnter Library ID for user {user_name}: ")
            new_user = User(user_name, library_id)
            new_user.save_to_db()

        else:
            cnx = DatabaseConnectionManager()
            cnx.connect()
            cursor = cnx.get_cursor()

            valid_input = True
            if choice == '2':
                print("\nEnter the Name of the User to Find...")
                user_name = input("Partical search using wildcard (%) is allowed: ")
                if user_name == '%':
                    print("\nCannot enter just '%'. Use User Operations #3 to Displays ALL Users")
                    valid_input = False
                else: cursor.execute("select * from users where name like %s", [user_name])
            else: cursor.execute("select * from users")
            
            if valid_input:
                results = cursor.fetchall()
                if results:
                    for user_id, user_name, library_id in results:
                        print(f"\nName: {user_name}\nLibrary ID: {library_id}")
                        select = "select title from books where id in (select book_id from borrowed_books where user_id = %s and return_date is null)"
                        cursor.execute(select, [user_id])
                        results = cursor.fetchall()
                        if not results: print(" * No Books Currently on Loan!")
                        else: print("Borrowed:", ", ".join([title[0] for title in results]))
                else: print("\nNo Users found matching the search criteria." if choice == '2' else "\nThere are currently No Users in the Library System!")
                
            cursor.close()
            cnx.close()
        
    def author_operations(self):
        print("\nAuthor Operations:\n 1. Add a new author\n 2. View author details\n 3. Display all authors")
        choice = input("\nEnter your choice (1-3): ")
        while choice not in ['1','2','3']: choice = input(f"\nInvalid choice! Please enter a number between 1 and 3: ")
        
        if choice == '1':
                name = input("\nEnter Author's Name: ")
                bio = input(f"\nEnter {name}'s Biography: ")
                new_author = Author(name, bio)
                new_author.save_to_db()
                
        else:
            cnx = DatabaseConnectionManager()
            cnx.connect()
            cursor = cnx.get_cursor()

            valid_input = True
            if choice == '2':
                print("\nEnter the Name of the Author to Find...")
                author_name = input("Partical search using wildcard (%) is allowed: ")
                if author_name == '%':
                    print("\nCannot enter just '%'. Use Author Operations #3 to Displays ALL Authors")
                    valid_input = False
                else: cursor.execute("select name, biography from authors where name like %s", [author_name])
            else: cursor.execute("select name, biography from authors")
                
            if valid_input:
                results = cursor.fetchall()
                if results:
                    for name, biography in results: print(f"\nName: {name}\nBiography: {biography}")
                else: print("\nNo Authors found matching the search criteria." if choice == '2' else "\nThere are currently No Authors in the Library System!")

            cursor.close()
            cnx.close()
# Welcome to the Library Management System!
**This library management system utilizes a Relational Database Management System (RDBMS) to store and manage library data.** An RDBMS stores data in a structured format using tables with rows and columns, making it efficient for querying and retrieving information. The system is divided into several classes and python files.

## Classes:

**DatabaseConnectionManager:** This class handles the logic for connecting to the MySQL database.

**Library:** This class represents the library itself. It holds information about books, users, and authors through separate lists. It provides methods to perform operations on these entities.

**Book:** This class represents a book in the library. It stores details like title, author, ISBN, genre, publication date, and availability status. It includes methods to check-out and return books.

**User:** This class represents a user registered with the library. It stores user name and library ID.

**Author:** This class represents an author whose books are in the library. It stores author name and biography.

## Python files:

* **connection_manager.py:** Contains the DatabaseConnectionManager class that handles database connections.

* **main.py:** Creates a Library object and presents a main menu to the user for various operations.

* **library.py:** The primary program that provides the user interface and interacts with other modules to manage library operations.

* **book.py, user.py, author.py:** Define classes (Book, User, Author) representing library attributes and methods to interact with them, including saving them to the database.

## Running the Program:

1. Save all the six files (main.py, connection_manager.py, library.py, book.py, user.py, author.py) in the same directory.
2. Open a terminal or command prompt and navigate to the directory where you saved the files.
3. Run **main.py**

## Explanation of Features:

The program offers a menu-driven interface with functionalities categorized by Books, Users, and Authors. Here's what each section offers:

### Book Operations:

* **Add a new book:** Enter details like title, author, ISBN, genre, and publication date.
* **Borrow a book:** Search for a book by title and borrow it if available (requires the user to be in the system).
* **Return a book:** Search for a borrowed book by title and return it.
* **Search for a book:** Find a book by title and see if it's available.
* **Display all books:** View a list of all books in the library with details and availability status.

### User Operations:

* **Add a new user:** Register a new user with a name and library ID.
* **View user details:** Search for a registered user and see their details like borrowed books.
* **Display all users:** View a list of all registered users with their details.

### Author Operations:

* **Add a new author:** Register a new author with a name and biography.
* **View author details:** Search for a registered author and see their biography.
* **Display all authors:** View a list of all registered authors and their biographies.

## Key Features:

* **Database Connectivity:** Uses a MySQL database to store and manage library data.
* **User Input Validation:** Ensures correct data entry for dates and other fields.
* **Author-Book Relationships:** Connects books with their respective authors.
* **Borrowing and Returning:** Manages book availability and records borrowing history.
* **Search Functionality:** Allows for both exact and **partial** searches for books, users and authors.

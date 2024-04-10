from library import Library
library = Library()

print("\nWelcome to the Library Management System!")

while True:
    
    print("\nMain Menu:\n 1. Book Operations\n 2. User Operations")
    print(" 3. Author Operations\n 4. Quit")

    choice = input("\nEnter your choice (1-4): ")
    if   choice == '1': library.book_operations()
    elif choice == '2': library.user_operations()
    elif choice == '3': library.author_operations()
    elif choice == '4':
        print("\nExiting the Library Management System...\n")
        break
    else: print(f"\nInvalid choice. Please enter a number between 1 and 4!")
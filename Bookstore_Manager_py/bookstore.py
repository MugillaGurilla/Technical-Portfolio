# This is a program for managing stock in a bookstore context.

import sqlite3
from tabulate import tabulate
import spacy 
nlp = spacy.load("en_core_web_md")

db = sqlite3.connect("data/ebookstore")
cursor = db.cursor()

# I'll be printing tables a lot so this makes it easier
def print_whole_table(table):
    cursor.execute(f"SELECT * FROM {table}")
    print(tabulate(cursor.fetchall()))


# This prints a specific row from a table
def print_specific_table_row(table, row):
    cursor.execute(f"SELECT * FROM {table} WHERE id={row}")
    row_header_2d_list = [cursor.fetchone()]
    row_header_2d_list = add_headers(row_header_2d_list)
    print(tabulate(row_header_2d_list))


# This adds headers to any 2D list
def add_headers(data_list):
    headers = ("id", "Title", "Author", "Quantity")
    data_list.insert(0, headers)
    return data_list


# This functions gets the the user to enter and ID, performs some integrity checks and returns the ID
def get_id_from_user(function_type):
    end_prompt = ""
    if function_type == "delete":
        end_prompt = "you'd like to delete"
    elif function_type == "update":
        end_prompt = "you'd like to update"

    while True:
        while True:
            id = input(f"Enter the book ID {end_prompt}, or enter -1 to exit: ")
            if id == -1:
                break
            try:
                id = int(id)
                break
            except:
                print("Invalid data type, please enter an integer")
                continue
        
        if id == -1:
            break

        cursor.execute("""SELECT id FROM books""")
        id_list = cursor.fetchall()
        id_list = [sum(element) for element in id_list]
        if id in id_list:
            break
        else: 
            print("ID not recognised, please try again.")
    return id


# Piece de resistance. This function used Natural Language Processing to search the database for close matches.
# The user enters a search term for a book and the program will print out any relevant matches. 
def nlp_search():
    search_term = input(f"Search for: ")
    close_match_ids = []
    cursor.execute("""SELECT title, author FROM books""")
    term_list = cursor.fetchall()
    close_match_list = []
    
    for term in term_list:
        if nlp(search_term).similarity(nlp(term[0])) > 0.80 or nlp(search_term).similarity(nlp(term[1])) > 0.80:
            cursor.execute(f"""SELECT id FROM books WHERE title=?""", (term[0],))
            close_match_ids.append(cursor.fetchone())

    for id in close_match_ids:
        cursor.execute("""SELECT * FROM books WHERE id=?""", (id[0],))
        close_match_list.append(cursor.fetchone())

    close_match_list = add_headers(close_match_list) 
    print(tabulate(close_match_list)) 
        

# This will initialise a database called ebookstore if it's not there already
# Most likely, this function will functionally be skipped
def initialise_stock():
    # Would like to be able to add books here and not have to delete database...
    initial_stock = [(3001, "A Tale of Two Cities", "Charles Dickens", 30),
                    (3002, "Harry Potter and the Philosopher\'s Stone", "J.K. Rowling", 40),
                    (3003, "The Lion, the Witch and the Wardrobe", "C. S. Lewis", 25),
                    (3004, "The Lord of the Rings", "J.R.R Tolkien", 37),
                    (3005, "Alice in Wonderland", "Lewis Carroll", 12)]

    cursor.execute("""CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY,
                title TEXT, author TEXT, qnty INTEGER)""")           
    try: 
        cursor.executemany("""INSERT INTO books VALUES(?,?,?,?)""", initial_stock)
    except Exception:
        db.rollback()
    finally:
        db.commit()


# This is the main menu
def menu():
    while True:
        menu_choice = int(input("""Choose an option from the following menu.
1 - Enter book
2 - Update book 
3 - Delete book 
4 - Search books
5 - View All Stock 
0 - Exit
: """))

        if menu_choice == 1:
            enter_book()
        elif menu_choice == 2:
            update_book()
        elif menu_choice == 3:
            delete_book()
        elif menu_choice == 4:
            search_book()
        elif menu_choice == 5:
            print_whole_table("books")
        elif menu_choice == 0:
            break
            db.close()
    


# This function enters a new book into the databse and prints the row it's stored at
def enter_book():
    book_name = input("What is the name of the new book? ")
    author_name = input("What is the name of its author? ")
    quantity = input("How many would you like to enter into stock? ")

    # I'm automatically getting the book ID here, this is the default option
    cursor.execute("""SELECT id FROM books ORDER BY id DESC LIMIT 1""")
    nu_id = cursor.fetchone()[0] + 1

    # If there are gaps in the IDs, this will fill them
    cursor.execute("""SELECT id FROM books ORDER BY id DESC""")
    current_id_list = cursor.fetchall()
    current_id_list = [sum(x) for x in current_id_list]
    counter = 0
    for counter, id in enumerate (current_id_list, 0):
        if id == 3001:
            break
        elif (id - current_id_list[counter+1]) != 1:
            nu_id = (current_id_list[counter+1] + 1)
            break
        elif current_id_list[-1] != 3001:
            nu_id = current_id_list[-1] - 1
            break
        else: 
            continue

    cursor.execute("""INSERT INTO books VALUES(?,?,?,?)""", (nu_id, book_name, 
        author_name, quantity))
    db.commit()
    
    print_specific_table_row("books", nu_id)

# This function updates existing books and then prints out the updated row
def update_book():
    print_whole_table("books")
    while True:
        id = get_id_from_user("update")
        if id == -1:
            break

        update_type = input("Would you like to change the title, author or quantity? (title / author / quantity) ")

        while True:
            if update_type.strip().lower() == "title":
                print("What is the corrected title?")
                corrected_title = input()
                cursor.execute("""UPDATE books SET title = ? WHERE id = ?""", (corrected_title, id))
                print_specific_table_row("books", id)
                break

            elif update_type.strip().lower() == "author":
                print("What is the corrected author?")
                corrected_author = input()
                cursor.execute("""UPDATE books SET author = ? WHERE id = ?""", (corrected_author, id))
                print_specific_table_row("books", id)
                break

            elif update_type.strip().lower() == "quantity":
                print("What is the corrected quantity?")
                corrected_quantity = int(input())
                cursor.execute("""UPDATE books SET qnty = ? WHERE id = ?""", (corrected_quantity, id))
                print_specific_table_row("books", id)
                break

            else:
                print("Invalid input, please try again.")
                update_type = input()

        db.commit()
        break


# This function deletes an entire book from the table
def delete_book():
    print_whole_table("books")
    while True:
        id = get_id_from_user("delete")
        cursor.execute("""DELETE FROM books WHERE id = ?""", (id,))
        db.commit()
        break
    print_whole_table("books")


def search_book():
    print(tabulate(nlp_search()))


initialise_stock()
menu()
db.close()
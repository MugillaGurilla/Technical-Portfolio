import sqlite3
import spacy 
nlp = spacy.load("en_core_web_md")
import tkinter as tk
from tkinter.filedialog import askopenfilename
from functools import partial

# This functions connect to the database and created a cursor
db = sqlite3.connect("data/ebookstore")
cursor = db.cursor()

# These five functions are utility functions that I will repeatedly use
def initialise_stock():
    # This will initialise a database called ebookstore if it's not there already
    # Most likely, this function will essentially be skipped
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

# This adds headers to any 2D list
def add_headers(data_list):
    headers = ("id", "Title", "Author", "Quantity")
    data_list.insert(0, headers)
    return data_list

# Clears all widgets from info_frame
def clear_info_frame():
    for widgets in info_frame.winfo_children():
        widgets.destroy()

# Renders body frame. This function is always called after clear_info_frame()
def render_body_frame():
    body_frame = tk.Frame(master=info_frame)
    body_frame.grid()
    return body_frame

# This takes a two list and prints it to screen in a nice, presentable fashion, adding a scrollbar if necessary. 
def tk_print_2d_list(multi_dimensional_list):
    clear_info_frame()
    info_frame.grid(row=1, sticky="news")
    info_frame.grid_columnconfigure(0, weight=1)

    info_canvas_scrb_frame = tk.Frame(master=info_frame)
    info_canvas_scrb_frame.grid()
    info_canvas_scrb_frame.grid_rowconfigure(0, weight=1)
    info_canvas_scrb_frame.grid_columnconfigure(0, weight=1)
    info_canvas_scrb_frame.grid_propagate(False)

    canvas = tk.Canvas(info_canvas_scrb_frame)
    canvas.grid(row=0, column=0, sticky="news")

    vsb = tk.Scrollbar(info_canvas_scrb_frame, orient="vertical", command=canvas.yview)
    vsb.grid(row=0, column=1, sticky="ns")
    canvas.configure(yscrollcommand=vsb.set)

    book_entry_frame = tk.Frame(canvas)
    canvas.create_window((0,0), window=book_entry_frame, anchor="nw")

    row = 0
    col = 0
    for book in multi_dimensional_list:
        for detail in book:
            while col < 4:
                book_attr = tk.Label(master=book_entry_frame, text=detail, height=2)
                book_attr.grid(row=row, column=col, )
                col += 1
                break
            while  col == 4:
                col = 0
                row += 1

    book_entry_frame.update_idletasks()

    # This section determines frame height and whether or not to render the scrollbar
    max_desired_height = 300
    if book_entry_frame.winfo_height() > max_desired_height:
        scrollable_frame_height = max_desired_height
    else: 
        scrollable_frame_height = book_entry_frame.winfo_height()
        vsb.grid_remove()

    info_canvas_scrb_frame.config(width=book_entry_frame.winfo_width() + vsb.winfo_width(), height=scrollable_frame_height)

    canvas.config(scrollregion=canvas.bbox("all"))


# This functions finds the next new ID. It checks for gaps in the IDs and fills them first. 
def find_nu_id():
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

    return nu_id

        # VIEW ALL

# This takes the whole database and returns it as a 2d list
def get_whole_table(table):
    cursor.execute(f"SELECT * FROM {table}")
    whole_table_2d_list = add_headers(cursor.fetchall())
    tk_print_2d_list(whole_table_2d_list)

        # UPDATE AND DELETE

# This functions gets the the user to enter and ID. Used for both updating and deleting.
def get_id_from_user(function_type):
    clear_info_frame()
    body_frame = render_body_frame()


    end_prompt = ""
    if function_type == "delete":
        end_prompt = "you'd like to delete"
    elif function_type == "update":
        end_prompt = "you'd like to update"

    id_prompt = tk.Label(master=body_frame, text=f"Enter the book ID {end_prompt}, or enter -1 to exit: ").grid(row=0, column=0)
    id_field = tk.Entry(master=body_frame)
    id_field.grid(row=0, column=1, sticky="e")
    id_confirm_button = tk.Button(master=body_frame, text=function_type.capitalize(), command=partial(convert_id_field_object_to_id_var, id_field, function_type)).grid(row=0, column=2)
    info_frame.grid()

# This converts the tk.Entry object to a string. Used for both updating and deleting.
def convert_id_field_object_to_id_var(id_field, function_type):
    id = id_field.get()
    check_id_integrity(id, function_type)
    
# This performs some integrity tests and deletes within this function or send to update_entry_func()
# Used for both updating and deleting
def check_id_integrity(id, function_type):
        clear_info_frame()

        body_frame = tk.Frame(master=info_frame)
        body_frame.grid()

        try:
            id = int(id)
        except:
            invalid_data_type = tk.Label(master=body_frame, text = "Invalid data type, please enter an integer").grid(row=1, column=0)
            return

        if id == -1:
            return

        if function_type == "delete":    
            cursor.execute("""SELECT id FROM books""")
            id_list = cursor.fetchall()
            id_list = [sum(element) for element in id_list]
            if id in id_list:
                cursor.execute("""DELETE FROM books WHERE id = ?""", (id,))
                successful_delete = tk.Label(master=body_frame, text="Book deleted successfully").grid(row=1, column=0)
                db.commit()
            else: 
                unrecognised_id = tk.Label(master=body_frame, text="ID not recognised, please try again.").grid(row=1, column=0)
                return
        elif function_type == "update":
            gather_updated_entry_details(id)

# This function gathers details and then uses those details in the nested function to update an entry. Used for updating only.
def gather_updated_entry_details(id):

    def update_entry_details(id, title_field, author_field, quantity_field):
        title = title_field.get()
        author = author_field.get()
        quantity  = quantity_field.get()

        clear_info_frame()
        body_frame = render_body_frame()

        
        save_success_label = tk.Label(master=body_frame, text="Update success!").grid(row=1, column=0)

        cursor.execute(f"""UPDATE books SET title = ?, author = ?, qnty = ? WHERE id = ?""", (title, author, quantity, id))
        db.commit()

    cursor.execute(f"""SELECT * FROM books WHERE id={id}""")
    book_details = cursor.fetchone()

    body_frame = render_body_frame()


    title_label = tk.Label(master=body_frame, text="Title").grid(row=1, column=0)
    title_field = tk.Entry(master=body_frame)
    title_field.insert(0, book_details[1])
    title_field.grid(row=1, column=1)
    author_label = tk.Label(master=body_frame, text="Author").grid(row=2, column=0)
    author_field = tk.Entry(master=body_frame)
    author_field.insert(0, book_details[2])
    author_field.grid(row=2, column=1)
    quantity_label = tk.Label(master=body_frame, text="Quantity").grid(row=3, column=0)
    quantity_field = tk.Entry(master=body_frame)
    quantity_field.insert(0, book_details[3])
    quantity_field.grid(row=3, column=1)

    save_button = tk.Button(master=body_frame, text="Save", command=partial(update_entry_details, id, 
                            title_field, author_field, quantity_field)).grid(row=4, column=1)

        # NLP SEARCH

# This gets a search tyerm from the user, in the form of a tk.Entry object
def get_nlp_search_term():
    clear_info_frame()
    body_frame = render_body_frame()

    prompt = tk.Label(master=body_frame, text="What you would like to search?").grid(row=0, column=0)
    form_field = tk.Entry(master=body_frame)
    form_field.grid(row=0, column=1, sticky="e")
    start_search_button = tk.Button(master=body_frame, text="Search", command=partial(send_nlp_search_term, form_field)).grid(row=0, column=2)
    info_frame.grid()

# This converts the tk.Entry object into a string
def send_nlp_search_term(form_field):
    search_term = form_field.get()
    nlp_search(search_term)

# This searches the search term string using NLP, appends close matches to a 2D lists and 
# sends that to tk_print_2d_list() for printing
def nlp_search(search_term):
    close_match_ids = []
    close_match_list = []
    cursor.execute("""SELECT title, author FROM books""")
    term_list = cursor.fetchall()
    
    for term in term_list:
        if nlp(search_term).similarity(nlp(term[0])) > 0.80 or nlp(search_term).similarity(nlp(term[1])) > 0.80:
            cursor.execute(f"""SELECT id FROM books WHERE title=?""", (term[0],))
            close_match_ids.append(cursor.fetchone())

    for id in close_match_ids:
        cursor.execute("""SELECT * FROM books WHERE id=?""", (id[0],))
        close_match_list.append(cursor.fetchone())

    close_match_list = add_headers(close_match_list) 
    tk_print_2d_list(close_match_list)
        
        # ENTER A NEW BOOK

def enter_book():

    def add_nu_entry(id, title_field, author_field, quantity_field):
        title = title_field.get()
        author = author_field.get()
        quantity  = quantity_field.get()

        clear_info_frame()
        body_frame = render_body_frame()

        save_success_label = tk.Label(master=body_frame, text="Add success!").grid(row=1, column=0)

        cursor.execute("""INSERT INTO books VALUES(?,?,?,?)""", (id, title, 
            author, quantity))
        db.commit()

    clear_info_frame()
    body_frame = render_body_frame()

    title_label = tk.Label(master=body_frame, text="Title").grid(row=1, column=0)
    title_field = tk.Entry(master=body_frame)
    title_field.grid(row=1, column=1)
    author_label = tk.Label(master=body_frame, text="Author").grid(row=2, column=0)
    author_field = tk.Entry(master=body_frame)
    author_field.grid(row=2, column=1)
    quantity_label = tk.Label(master=body_frame, text="Quantity").grid(row=3, column=0)
    quantity_field = tk.Entry(master=body_frame)
    quantity_field.grid(row=3, column=1)
    info_frame.grid()

    id = find_nu_id()

    save_button = tk.Button(master=body_frame, text="Save", command=partial(add_nu_entry, id, 
                            title_field, author_field, quantity_field)).grid(row=4, column=1)

        # UPDATE EXISTING

# This function updates existing books and then prints out the updated row
def update_book():
    clear_info_frame()
    get_id_from_user("update")

        # DELETE EXISTING BOOK

# This function deletes an entire book entry from the table, three functions are used in total
# The first being get_id_from_user()
def delete_book():
    clear_info_frame()
    get_id_from_user("delete")
    
        # BULK ADD BOOKS FROM A CSV FILE.

def bulk_add():

    def open_file():
        filepath = askopenfilename(
            filetypes = [("CSV Files", "*.csv")]
    )
        if not filepath:
            return

        add_book_details(filepath)
    
    def add_book_details(filepath):
        if filepath == None:
            return
    
        with open (filepath, "r", encoding="utf-8") as books_file:
            for line in books_file:
                nu_id = find_nu_id()


                # Cleaning up
                current_line_values_list = line.split(",")
                if current_line_values_list[1].strip() == "The\"" or current_line_values_list[1].strip() == "A\"":
                    current_line_values_list[0] = f"{current_line_values_list[1]} {current_line_values_list[0]}"
                    current_line_values_list.pop(1)
                
                current_line_values_list[1] = f"{current_line_values_list[2]} {current_line_values_list[1]}"
                current_line_values_list.pop(2)

                for counter, value in enumerate (current_line_values_list, 0):
                    value = value.replace("\"", "").strip()
                    current_line_values_list.insert(counter, value)
                    current_line_values_list.pop(counter+1)
                
                current_line_values_list = current_line_values_list[:2]

                cursor.execute("""INSERT INTO books VALUES(?,?,?,?)""", (nu_id, current_line_values_list[0], 
                    current_line_values_list[1], 10,))

        db.commit()
        successful_bulk_add()

    def successful_bulk_add():
        clear_info_frame()
        body_frame = render_body_frame()

        successful_bulk_add_prompt = tk.Label(master=info_frame, text="Bulk add success!").grid(row=1, column=0)
    
    clear_info_frame()
    body_frame = render_body_frame()

    open_button = tk.Button(master=info_frame, text="Open", command=open_file).grid(row=0, column=0)
    info_frame.grid()


window = tk.Tk()
window.title("Bookstore Manager")
window.geometry("1000x350")

tabs_frame = tk.Frame(master=window)
tabs_frame.columnconfigure([0,1,2,3,4,5], weight=1, minsize=150)
tabs_frame.rowconfigure(0, weight=0, minsize=40)
info_frame = tk.Frame(window)


enter_button = tk.Button(master=tabs_frame, text="Enter Book", relief=tk.RAISED, bd=2, command=enter_book).grid(row=0, column=0)
update_button = tk.Button(master=tabs_frame, text="Update Book", relief=tk.RAISED, bd=2, command=update_book).grid(row=0, column=1)
delete_button = tk.Button(master=tabs_frame, text="Delete Book", relief=tk.RAISED, bd=2, command=delete_book).grid(row=0, column=2)
search_button = tk.Button(master=tabs_frame, text="Search Book", relief=tk.RAISED, bd=2, command=get_nlp_search_term).grid(row=0, column=3)
view_all_button = tk.Button(master=tabs_frame, text="View All", relief=tk.RAISED, bd=2, command=partial(get_whole_table, "books")).grid(row=0, column=4)
bulk_add_button = tk.Button(master=tabs_frame, text="Bulk Add", relief=tk.RAISED, bd=2, command=bulk_add).grid(row=0, column=5)
quit_button = tk.Button(master=tabs_frame,  text="Quit", relief=tk.RAISED, bd=2, command=window.destroy).grid(row=0, column=6)
tabs_frame.grid(row=0)


window.mainloop()
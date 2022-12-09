import sqlite3
from tabulate import tabulate

db = sqlite3.connect("data/ebookstore")
cursor = db.cursor()

def get_next_ID():
    # I'm automatically getting the book ID here, this is the default option
    cursor.execute("""SELECT id FROM books ORDER BY id DESC LIMIT 1""")
    nu_id = cursor.fetchone()[0] + 1

    # If there are gaps in the IDs, this will fill them - otherwise the ID will default to as above
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

def bulk_add():
    with open ("books.csv", "r") as books_file:
        for line in books_file:
            nu_id = get_next_ID()

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

    cursor.execute(f"SELECT * FROM books")
    print(tabulate(cursor.fetchall()))

bulk_add()
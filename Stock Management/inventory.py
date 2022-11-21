# This is a program for managing stock across a number of warehouses. 

#========Importing libraries ===========
from tabulate import tabulate
from operator import attrgetter


#========The beginning of the class==========
class Shoes:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return self.cost 

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        str_rep = f"{self.country}, {self.code}, {self.product}, {self.cost}, {self.quantity}"
        return str_rep

    # This function will be used a lot
    # It takes an Shoes object and turn it into a list
    # It's needed for printing 2D lists in a tabulated format
    def __split__(self):
        current_line_list = [self.country, self.code, self.product, self.cost, self.quantity]
        return current_line_list

    def get_value(self):
        value = f"${int(self.cost) * int(self.quantity)}"
        return value

# This is a very important list. Most of the code runs through it in some way. 
# It contains shoe informations stored as 'Shoes' objects. 
shoe_list = []

# This function takes raw data from inventory.txt, turns it into a Shoes object and appends it to shoe_list
def read_shoes_data():
    with open ("inventory.txt", "r") as file:
        line_num = 0
        for line in file:
            try:
                current_line = line.split(",")
                current_object = Shoes(current_line[0], current_line[1], current_line[2], current_line[3], current_line[4])
                shoe_list.append(current_object)                
                line_num += 1
            except:
                print(f"There was an error extracting data from line {line_num}.")

# This function can be called anytime there is an update to shoe_list. It will rewrite updates to inventory.txt.
# In reality, this function is only used in conjunction with re_stock() but could easily be reused
# It doesn't append, it rewrites the entire file. 
def write_updated_shoes_data():
    with open ("inventory.txt", "w") as file:
        for i in range(len(shoe_list)):
            file.write(f"{shoe_list[i].country},{shoe_list[i].code},{shoe_list[i].product},{shoe_list[i].cost},{shoe_list[i].quantity}\n")
            
# This function appends a new Shoes object to inventory.txt and updates shoe_list
def capture_shoes():
    pass
    print("Enter the details for the new product.")
    country = input("Country: ")
    code = input("Code: ")
    product = input("Product: ")
    cost = input("Cost: ")
    quantity = input("Quantity: ")

    # This will add the new shoe object to shoe_list
    nu_product = Shoes(country, code, product, cost, quantity)
    shoe_list.append(nu_product)
    
    # This will write it to inventory.txt
    with open ("inventory.txt", "a") as file:
        file.write("\n")
        file.write(f"{country},{code},{product},{cost},{quantity}")

# This function initialises a new 2D list - view_all_2d_list
# It then uses the __split__() function defined in the Shoes class on every object in shoe_list
# This turns the object element to a sublist and stores that in current_line_sublist.
# current_line_sublist is then appended to view_all_2d_list, which is then tabulates and printed
def view_all():
    view_all_2d_list = []
    for i in range(len(shoe_list)):
        current_line_sublist = shoe_list[i].__split__()
        view_all_2d_list.append(current_line_sublist) 
    print(tabulate(view_all_2d_list))
    
# This function uses the attrgetter module 
# It xtracts the object with the smallest value for quantity from shoe_list and stores than as min_qnty_object
# Headers are then appended to low_qnty_2d_list
# Using __split__() that object is turned into a sublist and appended to low_qnty_2d_list   
def re_stock():
    low_qnty_2d_list = []

    for i in range(1, len(shoe_list)):
        shoe_list[i].quantity = int(shoe_list[i].quantity)
    min_qnty_object = min(shoe_list[1:], key=attrgetter('quantity'))
    
    headers_sublist = shoe_list[0].__split__()
    min_qnty_list = min_qnty_object.__split__()
    low_qnty_2d_list.append(headers_sublist)
    low_qnty_2d_list.append(min_qnty_list)
    print(tabulate(low_qnty_2d_list))

    # This will restock the product on the main shoe_list list
    # It will also write the updates to inventory.txt
    while True:
        restock_prompt = input("Would you like to restock? (yes / no) ")
        if restock_prompt.lower().strip() == "yes":
            added_units = int(input("How many units would you like to add? "))
            updated_qnty = int(min_qnty_object.quantity) + added_units
            min_qnty_object.quantity = updated_qnty
            write_updated_shoes_data()

            # This will print the updated snapshot
            low_qnty_2d_list.pop()
            min_qnty_list = min_qnty_object.__split__()
            low_qnty_2d_list.append(min_qnty_list)
            print(tabulate(low_qnty_2d_list))
            break
        if restock_prompt.lower().strip() == "no":
            break
        else:
            print("Invalid input. Please try again.")
            pass

# This function runs through shoe_list, finds a code match, atbulates and prints
def search_shoe():
    search_2d_list = []
    search_match_sublist = []
    shoe_code = input("Please enter the code for the shoe that you wish to search: ")
    for i in range(len(shoe_list)):
        if shoe_list[i].code == shoe_code.upper():
            search_match_sublist = shoe_list[i].__split__()

    headers_sublist = shoe_list[0].__split__()
    search_2d_list.append(headers_sublist)
    search_2d_list.append(search_match_sublist)

    print(tabulate(search_2d_list))

# This function adds another column of data - "Value" which is populate using the get_value() function
# It then tabulates and prints the last three columns of original data as well as the new value column
def value_per_item():
    values_2d_list = []
    counter = 0
    for i in range(len(shoe_list)):
        value_sublist = shoe_list[i].__split__()
        if counter == 0:
            pass
            value_sublist.append("Value")
        else:
            value_sublist.append(shoe_list[i].get_value())
        values_2d_list.append(value_sublist[2:])
        counter += 1
    print(tabulate(values_2d_list))

# Similar to re_stock(), except this function the object with the greatest value for quantity
# It prints that the product is on sale and then tabulates and prints the product info. 
def highest_qty():
    highest_2d_list = []
    highest_sublist = []

    # This code turns every quantity instance into a sint and then finds the biggest int
    for i in range(1, len(shoe_list)):
        shoe_list[i].quantity = int(shoe_list[i].quantity)
    max_qnty = max(shoe_list[1:], key=attrgetter('quantity'))
    print(f"{max_qnty.product} is for sale!!! Come down, get a bargain!!!")

    # This code puts the info from max_qnty as well as headers into a 2d list
    # and prints it 
    headers_sublist = shoe_list[0].__split__()
    max_qnty = max_qnty.__split__()
    highest_2d_list.append(headers_sublist)
    highest_2d_list.append(max_qnty)
    print(tabulate(highest_2d_list))

# A menu for navigation
# The rest is just calling functions
def choose_menu():
    menu_prompt = input("""Select one of the following options.
c - capture shoes
va - view all
r - restock
s  - search shoes
v - value per item
h - highest quantity product
e - exit
: """)
    return menu_prompt

read_shoes_data()

while True:
    menu_prompt = choose_menu()

    if menu_prompt.strip().lower() == "va":
        view_all()

    elif menu_prompt.strip().lower() == "v":
        value_per_item()

    elif menu_prompt.strip().lower() == "r":
        re_stock() 

    elif menu_prompt.strip().lower() == "c":
        capture_shoes()

    elif menu_prompt.strip().lower() == "s":
        search_shoe()

    elif menu_prompt.strip().lower() == "h":
        highest_qty()

    elif menu_prompt.strip().lower() == "e":
        print('Goodbye!!!')
        exit()

    else:
        print("Invalid input. Please Try again")


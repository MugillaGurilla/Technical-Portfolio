def find_adj_mines(row_pos, col_pos):
    # The continue statements protect against any indices that off-field or out of range
    # The break statements just return a "#" value 
    # If it gets past all that....
    # The code runs down a column checking if the value is '-' or '#' and increments the counter as approrpiate
    # After three runs through a column, it goes onto the next column
    mine_counter = 0

    for i in range(3):                       # Going North
        if minefield[row_pos][col_pos] == "#":
            break
        elif row_pos+i > field_size or col_pos-1 > field_size-1:
            continue
        elif row_pos+i < 0 or col_pos-1 < 0:
            continue
        elif minefield[row_pos+i-1][col_pos-1] == "#":
            mine_counter += 1     

    for i in range(3):                      # Going West and East
        if minefield[row_pos][col_pos] == "#":
            break
        elif row_pos+i > field_size or col_pos > field_size-1:
            continue
        elif row_pos+i < 0 or col_pos < 0:
            continue
        elif minefield[row_pos+i-1][col_pos] == "#":
            mine_counter += 1

    for i in range(3):                       # Going South
        if minefield[row_pos][col_pos] == "#":
            mine_counter = "#"
            break
        elif row_pos+i > field_size or col_pos+1 > field_size-1:
            continue
        elif row_pos+i < 0 or col_pos+1 < 0:
            continue
        elif minefield[row_pos+i-1][col_pos+1] == "#":
            mine_counter += 1

    return mine_counter

minefield =[["-", "-", "-", "#", "#"], 
            ["-", "#", "-", "-", "-"], 
            ["-", "-", "#", "-", "-"], 
            ["-", "#", "#", "-", "-"], 
            ["-", "-", "-", "-", "-"]]

# Instantiating a 5x5 field, I'll use this to write values drawn onto using find_adj_mines
# This can be changed depending on the size of the minefield. 
field_size = 5
empty_minefield = [[None] * field_size for i in range(field_size)]


for i in range(len(empty_minefield)):
    for j in range(len(empty_minefield[i])):
        mine_counter = find_adj_mines(i, j)
        empty_minefield[i].pop(j)
        empty_minefield[i].insert(j, mine_counter)
        j += 1
    i += 1

# Changing the variable name because it's bad to have a variable name suggest the exact opposite of a variable is. 
not_so_empty_minefield = empty_minefield 

for i in range (len(not_so_empty_minefield)):
    print(not_so_empty_minefield[i])



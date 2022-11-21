#===== This is a task management program from keeping track of users and their tasks ====#


#=====importing libraries===========
from datetime import datetime

#====Login Section====

login_success = False

#===== Creating credential list ====#

def get_credentials() :
    in_file = open("user.txt", "r")
    credential_list = in_file.read()
    credential_list = credential_list.replace(",", "").split()
    in_file.close()
    return credential_list

#======== Defining functions =====#

def login() :
    login_success = False
    credential_list = get_credentials()
    username = input("Username: ")
    password = input("Password: ")
    if username in credential_list :                                        # if username is correct
        index = credential_list.index(username)                             # get the username's index
        if password == credential_list[index+1] :                           # if password is also correct, by checkng the value at the username's index + 1 (i.e. password)
            login_success = True
        if password != credential_list[index+1] :                           # if the password isn't correct
            print("The password entered was incorrect.")
    elif username not in credential_list :                                  # if username isn't correct
        print("We don't have anyone with that username on record.")
    return login_success, username 

def choose_menu() :
    if username != "admin" :        # if user is not admin
        menu = input('''\nSelect one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
e - Exit
: ''').lower()

    if username == "admin" :        # if user is admin
        menu = input('''\nSelect one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
gr - generate reports
s - display statistics
e - Exit
: ''').lower()

    return menu

#======== registering new user ===== #

def register_user() :
    register_complete = False           # to keep things looping
    credential_list = get_credentials()
    credential_list = credential_list[::2]
    while register_complete == False :
        # information prompts
        while True :
            nu_user = input("Please enter a username: ")
            if nu_user in credential_list :
                print("That username is already registered. Please try again.")
            else :
                break
        nu_password = input("Please enter a password: ")
        confirm_password = input("Thank you. Could you confirm the password? ")
        #checks
        if nu_password == confirm_password :                                    # if both passwords match
            with open ("user.txt", "a") as f :
                f.write("\n" + nu_user + ", " + nu_password)                    # write to file
            print(f"Registration complete. \'{nu_user}\' is now on record.")
            register_complete = True
        else :
            try_again = input("The passwords don't match. Would you like to try again? (Yes / No) ").lower()
            if try_again == "yes" :
                pass
            if try_again == "no" :
                register_complete = True

#========= This function defines w2hat happens if a non-admin user tries to access an admin section =====#

def error_not_admin() :
    print("Only the admin can acces this section.")  

def add_task() :
    # just getting loads of information here
    credential_list = get_credentials()
    assigned_to = input("Who is this task assigned to? ")
    while True :                         # just making sure the assignee is actually on record.
        if assigned_to in credential_list :
            break
        else :
            assigned_to = input("Assignee is not on record. Please try again. ")
    task_title = input("What is the title of this task? ")
    desc = input("Give a brief description of the task please. ")
    due = input("When is it due? ")
    current_date = datetime.now()
    current_date = current_date.strftime("%d/%m/%Y")
    task_completion = "No"

#============== Appending new task to file =======#

    with open("tasks.txt", "a") as f :
        f.write(f"\n{current_date}_ {task_title}_ {due}_ {assigned_to}_ {desc}_ {task_completion}")  

#========== This will print most 2D lists but it's customised specifically for tasks.txt =====#

def print_tasks(tasks) :
    for j in range(len(tasks)) :

        # This runs through each sublist and prints it on it's own line. 
        # Until it reaches the sixth element of the sublist and then moves onto the next sublist
        while True :
            i = 0
            while i < 3 :
                print(f"{tasks[j][i]}")
                i += 1
            while i == 3 :
                print(f"{tasks[j][i]}")
                i += 1
            while i == 4 :
                print(f"\n{tasks[j][i]}")
                i += 1
            while i == 5 :
                print(f"Completed? {tasks[j][i]}")
                i += 1
            break
        j += 1  

#======= This function takes all tasks from tasks.txt and stores them in a 2D list =============#

def get_all_tasks() :
    with open("tasks.txt", "r") as f :
        task_txt_content = []
        for line in f:
            current_line = line.split("_ ")
            task_txt_content.append(current_line)
    return task_txt_content

#====== This is just a combination of two functions. It's used to view all tasks ============#

def view_all_tasks() :
    print_tasks(get_all_tasks())          

#===== This adds every tasks for a particular username to a list =========#
#===== It then prints it ======#
#===== and then asks the user if they want to edit any tasks =========#

def view_my_tasks() :
    current_line = 0                                    
    assignee_line_list = []                             

    with open("tasks.txt", "r") as f :
        for line in f :                                
            if not username in line :
                current_line += 1
            if username in line :
                current_line += 1
                line = line.split("_ ")
                assignee_line_list.append(line)

        print_tasks(assignee_line_list)

        edit_tasks()

#====== This function gets all tasks and stores them in a 2D list. It asks the user if they want to change anything, 
#====== changes the 2D list as appropriate, puts those changes back into the 2D list and then rewrites the entire
#====== tasks.txt file with the new updates 

def edit_tasks() :
    all_tasks = get_all_tasks()
    print("Would you like to edit one or your tasks or mark it as complete? Enter the task title to procceed, or '-1' to return to the main menu.")
    prompt_title = input("")

    i = 0 
    j = 0
    for j in range(len(all_tasks)) :
        for i in range(len(all_tasks[j])) :
            if prompt_title == all_tasks[j][1] :
                if all_tasks[j][5].strip() == "Yes" :
                    print("This task has already been completed and thus can't be edited.")
                    break
                else:
                    print ("Would you like to edit the task's due date, who it's assigneed to or mark it as complete? (due date / assigned / complete)")
                    edit_type = input("")
                    if edit_type.lower().strip() == "due date" :
                        print("When is the task due?")
                        nu_due_date = input()
                        all_tasks[j].pop(2)
                        all_tasks[j].insert(2, nu_due_date)
                        break
                    elif edit_type.lower().strip() == "assigned" :
                        print("Who is the task assigned to?")
                        nu_assignee = input()
                        all_tasks[j].pop(3)
                        all_tasks[j].insert(3, nu_assignee)
                        break
                    elif edit_type.lower().strip() == "complete" :
                        all_tasks[j].pop(5)
                        all_tasks[j].insert(5, "Yes\n")
                        break
                    break

            elif prompt_title == "-1" :
                break
            else :
                i += 1
    
    with open ("tasks.txt", "w") as f :
            for j in range(len(all_tasks)) :
                f.write(f"{all_tasks[j][0]}_ {all_tasks[j][1]}_ {all_tasks[j][2]}_ {all_tasks[j][3]}_ {all_tasks[j][4]}_ {all_tasks[j][5]}")
                j += 1

#========= this is a simple function to get the current number of users and numbers of tasks ============#

def get_stats() :
    with open("tasks.txt", "r") as f : 
        no_tasks = 0                                    
        for line in f :
                no_tasks += 1
    with open("user.txt", "r") as f :  
        no_users = 0
        for line in f :
            no_users += 1
    return no_tasks, no_users

#====== this reads everything from the overview txt files and prints it out ======#
#====== if there are no overview txt files, it runs the generate report functions and then prints it ======#

def display_stats():
    while True:
        try:
            task_overview_string = ""
            with open ("task_overview.txt", "r") as f:
                for line in f:
                    task_overview_string += line
            print(f"{task_overview_string} \n")
            break
        except FileNotFoundError:
            generate_task_report()


    while True:
        try:
            user_overview_string = ""
            with open ("user_overview.txt", "r") as f:
                for line in f:
                    user_overview_string += line
            print(user_overview_string)
            break
        except FileNotFoundError:
            generate_user_report()

#======== this is the function to generate task reports. It basically just runs through the txt file, extracts info and prints to file ====#

def generate_task_report() :
    with open ("tasks.txt", "r") as f :

        # getting all the necessary information to execute the below code
        all_tasks = get_all_tasks()
        completed_tasks = 0
        uncompleted_tasks = 0
        overdue_tasks = 0
        percent_incomplete = 0
        percent_overdue = 0
        no_tasks = get_stats()

        # these are the indexes for the completion statement (Yes / No) and due date 
        completion_index = 5
        due_date_index =  2

        # this reformats today's date in a YYYYMMDD format and there's an empty list to store task due dates
        today_date = datetime.now()
        today_date = today_date.strftime("%Y%m%d")
        task_due_date_list = []
        
        # this for loop both checks whether a task is complete or not and extracts, refromats and adds its due date to the list
        for i in range(len(all_tasks)) :

            # complete or incomplete 
            if "No" in all_tasks[i][completion_index] :
                uncompleted_tasks += 1
                # reformatting the due date and adding it to the the list 
                current_due_date = all_tasks[i][due_date_index]
                current_due_date = current_due_date.split("/")
                current_due_date = "".join(current_due_date[::-1])
                task_due_date_list.append(current_due_date)
            elif "Yes" in all_tasks[i][completion_index] :
                completed_tasks += 1
        
        # finds out if the incomplete tasks are also overdue
        for i in range(len(task_due_date_list)) :
            if task_due_date_list[i] < today_date :
                overdue_tasks += 1        
        
        # calculates percentages
        percent_incomplete = (uncompleted_tasks / no_tasks[0]) * 100
        percent_overdue = (overdue_tasks / no_tasks[0]) * 100

    # this writes everything to file.
    with open ("task_overview.txt", "w") as f:
        f.write(f"\nTotal number of tasks is {no_tasks[0]}.")
        f.write(f"\nTotal number of incomplete tasks is {uncompleted_tasks}.")
        f.write(f"\nTotal number of complete tasks is {completed_tasks}.")
        f.write(f"\nTotal number of overdue tasks is {overdue_tasks}.")
        f.write(f"\nPercentage of incomplete tasks is {round(percent_incomplete)}%.")
        f.write(f"\nPercentage of overdue tasks is {round(percent_overdue)}%.")

def generate_user_report() :
    # this gets or initialises the necessary information
    no_users_tasks = get_stats()
    no_tasks = no_users_tasks[0]
    no_users = no_users_tasks[1]
    task_info_2d_list = []                      # this is a very important list, it'll store a user's username and their stats
    today_date = datetime.now()
    today_date = today_date.strftime("%Y%m%d")
    all_tasks = get_all_tasks()

    # this for loop runs through every SUBLIST of the all tasks LIST
    for j in range(len(all_tasks)) :
        users_total_tasks = 0
        percent_assigned_to_user = 0
        users_completed_tasks = 0
        users_incomplete_tasks = 0
        users_overdue_tasks = 0

        # this for loop runs through every ELEMENT of the every SUBLIST
        for i in range(len(all_tasks[j])) :
            assigned_to = all_tasks[j][3]                   # this gets the user who the task is assigned too
            users_total_tasks += 1
            percent_assigned_to_user = users_total_tasks / no_tasks * 100

            # this checks is the task is complete
            if all_tasks[j][5].strip() == "Yes" :
                users_completed_tasks += 1

            # this checks if it's incomplete as well as if it's overdue
            elif all_tasks[j][5].strip() == "No" :
                users_incomplete_tasks += 1
                due_date = all_tasks[j][2]
                due_date = due_date.split("/")
                due_date = "".join(due_date[::-1])
                if due_date < today_date :
                    users_overdue_tasks += 1

            # all info about the current task is then put into this list
            current_task_info = []
            current_task_info = [assigned_to, users_total_tasks, percent_assigned_to_user,  users_completed_tasks, users_incomplete_tasks, users_overdue_tasks]
            
            # that info is then added to this 2D list
            if task_info_2d_list == []:                             # this will only run once at the start when the 2D list is still empty
                task_info_2d_list.append(current_task_info)
            else:

                # this checks if the user already has a sublist with the 2D list. If they do, each corresponding element is added
                # if they don't have a sublist, the code skips to the else statement and makes them one. 
                for i in range(len(task_info_2d_list)):
                    if assigned_to in task_info_2d_list[i]:
                        pos = i
                        for counter, number in enumerate(current_task_info):
                            task_info_2d_list[pos].append(number + task_info_2d_list[pos][counter])
                        del task_info_2d_list[pos][1:7]
                        break                       
                    elif (len(task_info_2d_list)-1) == i: 
                        task_info_2d_list.append(current_task_info)
                        break
                    i += 1
            break
        j += 1
        i += 1

    # Everything is written to file using a for loop.
    with open ("user_overview.txt", "w") as f:
        f.write(f"Total number of users is {no_users}.")
        for i in range(len(task_info_2d_list)):
            f.write(f"\n\t{task_info_2d_list[i][0]}")
            f.write(f"\nThe total number of tasks assigned to this user is {task_info_2d_list[i][1]}.")
            f.write(f"\nTheir percentage of total tasks is %{round(task_info_2d_list[i][2])}.")
            f.write(f"\nTheir task completion percentage is %{round((task_info_2d_list[i][3] / task_info_2d_list[i][1] * 100))}.")
            f.write(f"\nThey still have {task_info_2d_list[i][4]} tasks to complete, {task_info_2d_list[i][5]} of which are overdue.")

#===== The rest of the code is just calling fucntions =====#

#====== Logging in ======#

while login_success == False :    
    login_success, username = login()

#====== Choosing tsk type =====#

while login_success == True:
    menu = choose_menu()

#======== registering new user ===== #

    if menu == 'r' and username == "admin":
        register_user()

    elif menu == 'r' and username  != "admin" :
        error_not_admin()

#======= Creating new task ==== #

    elif menu == 'a':
        add_task()

#=============== Viewing all current tasks ========#

    elif menu == 'va':
        view_all_tasks()

#============ Viewing logged-in user's tasks =========#            

    elif menu == 'vm':
        view_my_tasks()

#=========== Generate Reports ===================#

    elif menu == 'gr' and username == "admin":
        while True:
            print("Would you like to generate a task or user report? (Task / User)")
            task_or_user_report = input().lower().strip()
            if task_or_user_report == "task" :
                generate_task_report()
                break
            elif task_or_user_report == "user" :
                generate_user_report()
                break
            else:
                print("Invalid input. Please try again.")

    elif menu == "gr" and username != "admin":
        error_not_admin()


#=========== disaplying statistics for admin ======#

    elif menu == "s" and username == "admin":
        display_stats()

    elif menu == "s" and username != "admin":
        error_not_admin()

#=========== exit =================================#

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
from operations import Operations

system = Operations("inventory.txt") # creating an Operations object
possible_choices = (1, 2, 3, 4) # all possible choices in a tuple
choice = 0 # global choice value
is_continued = True
loop = True

while loop:

    if is_continued:
        print("_"*48)
        print(system.get_company_logo()) # printing the company logo made using ASCII art
        print("\tBecause your skin deserves the best.") # printing slogan
        print("_"*48)
        choice = input("\nWhat do you want to do?\n\n1) View available items\n2) Handle a sale\n3) Restock Products\n4) Exit\n\n-> ")

        try:
            choice = int(choice) # trying to convert choice input into an integer
        
        except:
            print("\n"*4+"_"*48)
            print("\n\t!!!! Please enter a valid number !!!!") # error message
            print("_"*48)
            continue # starting the main loop again since the choice was not an integer
                    
    # if invalid choice is chosen
    if choice not in possible_choices:
        print("\n"*4+"_"*48)
        print("\n\t!!!! Please enter a valid choice !!!!")
        print("_"*48)
        continue

    # if exit is chosen
    elif choice == 4:
        print("_"*48)
        print("\n\tThank you for using this program.\n\t  We hope you had a great time!")
        print("_"*48)
        loop = False
        continue

    system.handle_choice(choice) # handling the remaining 3 valid choices input by user, by calling the system object's method
  
    further_choice = input("\nDo you want to continue using the system? (y/n): ").lower()
    
    # loop to handle further choice
    while True:
        
        # if user decides to continue
        if further_choice == "y" or further_choice == "yes":
            is_continued = True
            break

        # if user decides not to continue
        elif further_choice == "n" or further_choice == "no":
            choice = 4 # manually setting the system choice to 4
            is_continued = False # setting this check variable to false to not ask the user for a system choice again
            break 

        # if user enters invalid choice
        else:
            further_choice = input("Please enter 'yes' or 'no' : ").lower()


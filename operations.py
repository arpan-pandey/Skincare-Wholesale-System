from read import FileReader
from write import FileWriter
from datetime import datetime

class Operations:

    # constructor
    def __init__(self,file_path):
        """
                Description:
                    Initializes an instance of the Operations class.

                Parameters:
                    file_path (str) : stores the file path of the main inventory.txt file

                Operations:
                    Assigns file_path object variable using the file path from the parameter. 
                    Creates objects of the FileReader and FileWriter classes.
        """
            
        self.file_path = file_path
        self.reader = FileReader(file_path)
        self.writer = FileWriter(file_path)
        
    # handling choice given by user
    def handle_choice(self, choice):
        """
                Description:
                    Handles the choice of the user.

                Parameters:
                    choice (int) : stores the choice option input by the user

                Operations:
                    Calls other functions based on the user's choice.
        """
        
        if choice == 1:
            print("\n"+"_"*48)
            print("\nHere are the details of all products our store has to offer:")
            self.display_products(True) # display
            
        elif choice == 2:
            self.handle_sale() # sales
            
        elif choice == 3: 
            self.restock_products() # restock

    # for displaying available products
    def display_products(self, is_restock):
        """
                Description:
                    Retrieves the data of products from inventory file,
                    and displays it.

                Parameters:
                    is_restock (boolean) : stores a value based on if the products are to be displayed for restock or not 

                Operations:
                    Retrieves product data through the reader object,
                    Displays the data in a tabular format,
                    Shows Cost Price / Selling Price of items based on the operation.
        """
        
        products = self.reader.get_products()
        
        print("_"*75)
        print("ID\tName\t\tBrand\t\tQty.\tPrice\tOrigin\tType")
        print("_"*75)

        for key, value in products.items():
            
            if int(value[2]) == 0 and not is_restock:
                continue # not displaying product if it is out of stock
            
            print(key, end="\t")
            
            for attribute in value:
                if attribute == value[3]:
                    
                    if is_restock:
                        print("Rs." + attribute, end="\t") # cost price for restock
                    else:
                        print("Rs." + str(int(attribute)*2), end="\t") # selling price for sales
                        
                else:
                    print(attribute, end="\t")
            print() # moving to next line

        print("\n") # two line gap after the table
        
    # for handling sales
    def handle_sale(self):
        """
                Description:
                    Handles the item sales operation.

                Parameters:
                    <none>

                Operations:
                    Retrieves product data using the reader object,
                    Displays the products using the display_products() method,
                    Asks user for ID and quantity of item sold,
                    Applies the "Buy 3 Get 1 Free" policy if applicable,
                    Updates the inventory.txt file after each sale, through writer object,
                    Creates an invoice using generate_customer_invoice() function.
        """
        
        iterate = True # boolean for the following loop
        purchase = {} # empty dictionary to store the purchase details
        unrewarded_quantity = {} # empty dictionary to store items not apllicable for the policy, if the user want to add more items later
        
        while iterate:
            self.display_products(False)
            products = self.reader.get_products()
            free_products_quantity = 0
            continue_handling = ""

            # loop to deal with non-integer key inputs
            while True:
                key = input("Please enter the ID of the item to be sold (Enter 0 to exit): ")
                
                try:
                    key = int(key)
                    break # breaking out of the loop if no error occurs 

                except:
                    print("_"*48)
                    print("\n!!! The ID must be a number !!!") # trying to convert the input into an integer
                    print("_"*48)
            
            valid_key = False # setting to false because we dont know yet
            
            while not valid_key:

                if key == 0:
                    break # ending the loop
                 
                # checking for negative input
                if key < 0:
                    print("_"*48)
                    print("\n!!! The ID cannot be negative !!!")
                    print("_"*48)
                    key = int(input("\nPlease enter a valid ID of the item to be sold (Enter 0 to exit): "))
                    continue

                # checking if the key maps to an entry in the products dictionary, or if it maps to an out of stock product
                if key not in products or int(products[key][2]) == 0:
                    print("_"*48)
                    print("\n!!! Invalid ID. No such item exists !!!")
                    print("_"*48)
                    key = int(input("\nPlease enter a valid ID of the item purchased (Enter 0 to exit): "))
                    continue

                valid_key = True # setting to true if both above checks are passed
                break

            # if user chooses to exit
            if key == 0:
                
                # if user has already sold some items
                if len(purchase) != 0:
                    name = input("Please enter the name of the customer for the invoice: ") # asking for name of customer
                    self.generate_customer_invoice(name, purchase, products) # calling method to generate invoice

                iterate = False
                break # ending the loop

            # if user chooses not to exit
            else:
                
                # loop to deal with non-integer key inputs
                while True:
                    quantity = int(input("Please enter the quantity of  '"+products[key][0]+"' purchased: "))
                    
                    try:
                        quantity = int(quantity) # trying to convert the input into an integer
                        break # breaking out of the loop if no error occurs 

                    except:
                        print("_"*48)
                        print("\n!!! The quantity must be a number !!!")
                        print("_"*48)
                
                valid_quantity = False # setting to false because we dont know yet
                
                while not valid_quantity:

                    # checking for negative quantity
                    if quantity < 0:
                        print("_"*48)
                        print("\n!!! The quantity cannot be negative !!!")
                        print("_"*48)
                        quantity = int(input("\nPlease enter a valid quanitity of  '"+products[key][0]+"' purchased: "))
                        continue

                    # chceking if quantity needed is greater than the stock
                    if quantity > int(products[key][2]):
                        print("_"*48)
                        print("\n!!! The quantity provided is not available !!!")
                        print("_"*48)
                        quantity = int(input("\nPlease enter a valid quanitity of  '"+products[key][0]+"' purchased: "))
                        continue

                    valid_quantity = True # setting to true if both above checks are passed
                    break

                print("_"*70)

                total_quantity = 0 # variable to store total quantity
                
                # when the quantity is not equal to the stock
                if quantity != int(products[key][2]):

                    # initializing the key if it is the first instance of purchase
                    if key not in unrewarded_quantity:
                        unrewarded_quantity[key] = 0

                    total_for_policy = quantity + unrewarded_quantity[key] # for items that will be considered for policy
                    
                    # applying policy if quantity is greater than 3
                    if total_for_policy >= 3:
                        free_products_quantity = int(total_for_policy/3) # to calculate the number of free items based on policy (Buy 3 get 1 free)
                        unrewarded_quantity[key] = total_for_policy % 3 # saving leftovers
                        total_quantity = quantity + free_products_quantity
                        
                        print('\nDue to our "Buy 3 Get 1 Free" policy, '+str(free_products_quantity)+" extra product(s) will be given.")

                        # if total quantity becomes greater than stock
                        if total_quantity > int(products[key][2]):
                            print("But since we only have "+products[key][2]+" items in stock, all of it will be given instead.")
                            total_quantity = int(products[key][2]) # updating total quantity to the entire stock

                    # printing appropriate message if policy is not applicable
                    else:
                        print('\nThis purchase doesn\'t meet the requirements for our "Buy 3 Get 1 Free" policy.')
                        total_quantity = quantity # setting total quantity to input quantity as no change will occur
                        unrewarded_quantity[key] += quantity # updating items not applicable for the
                        
                    # The following statement updates the newly created purchase dictionary, dynamically.
                    # The .get() function of the dictionary tries to get the value of that dictionary from the specified key, if the entry exists.
                    # If there is no entry of that specific key, the function will return an empty list (with two zeros).

                    # This is helpful in this system as the user can append the purchase if more items of the same product are bought later,
                    # in the same purchase.

                    # This dictionary stores only the key and quantity purchased, because it is all that is required to update the stock in the file.
                    
                    purchase[key] = [purchase.get(key, [0, 0])[0] + quantity, purchase.get(key, [0, 0])[1] + free_products_quantity]
                        
                # when the quantity if equal to the stock
                else:
                    total_quantity = int(products[key][2]) # updating total quantity to the entire stock
                    free_products_quantity = int(total_quantity/3) # to calculate the number of free items based on policy (Buy 3 get 1 free)
                    purchase[key] = [purchase.get(key, [0, 0])[0] + total_quantity-free_products_quantity, purchase.get(key, [0, 0])[1] + free_products_quantity] # same as in above if block, but updated to adjust total cost accordingly
                    
                    print('\nAll the stock was purchased.\nDue to our "Buy 3 Get 1 Free" policy, '+str(free_products_quantity)+" items will be given for free.")
                    
                print("This purchase was successfully noted.") # purchase successful message
                print("_"*70)

                # updating the main products dictionary after each purchase instance, by reducing the quantity
                products[key][2] = str(int(products[key][2]) - total_quantity)

                # calling the set_products method to update the inventory file, with the updated product quantity
                self.writer.set_products(products)
                 
                continue_handling = input("\nAre there other items in the purchase? (y/n): ") # asking if there are more products to be updated
                
                # loop to handle further choice
                while True:
                    # if user decides to continue
                    if continue_handling == "y" or continue_handling == "yes":
                        iterate = True
                        break

                    # if user decides not to continue
                    elif continue_handling == "n" or continue_handling == "no":
                        name = input("Please enter the name of the customer for the invoice: ") # asking for name of customer
                        self.generate_customer_invoice(name, purchase, products) # calling method to generate invoice
                        
                        iterate = False
                        break

                    # if user enters invalid choice
                    else:
                        continue_handling = input("Are there other items in the purchase? (y/n): ").lower()

    # for restocking products 
    def restock_products(self):
        """
                Description:
                    Handles the item restocking operation.

                Parameters:
                    <none>

                Operations:
                    Retrieves product data using the reader object,
                    Displays the products using the display_products() method,
                    Asks user for ID and quantity of item to be restocked,
                    Updates the inventory.txt file after each restock, through writer object,
                    Creates an invoice by using generate_company_invoice() function.
        """
        iterate = True # boolean for the following loop
        restock = {} # empty dictionary to store the restock details
        
        while iterate:
            self.display_products(True)
            products = self.reader.get_products()
            continue_handling = ""

            # loop to deal with non-integer key inputs
            while True:
                key = input("Please enter the ID of the item to be restocked (Enter 0 to exit): ")
                
                try:
                    key = int(key)
                    break # breaking out of the loop if no error occurs 

                except:
                    print("_"*48)
                    print("\n!!! The ID must be a number !!!") # trying to convert the input into an integer
                    print("_"*48)
            
            valid_key = False # setting to false because we dont know yet
            
            while not valid_key:

                if key == 0:
                    break # breaking out of the loop
                
                # checking for negative input
                if key < 0:
                    print("_"*48)
                    print("\n!!! The ID cannot be negative !!!")
                    print("_"*48)
                    key = int(input("\nPlease enter a valid ID of the item to be restocked (Enter 0 to exit): "))
                    continue

                # checking if the key maps to an entry in the products dictionary, or if it maps to an out of stock product
                if key not in products:
                    print("_"*48)
                    print("\n!!! Invalid ID. No such item exists !!!")
                    print("_"*48)
                    key = int(input("\nPlease enter a valid ID of the item restocked (Enter 0 to exit): "))
                    continue

                valid_key = True # setting to true if both above checks are passed
                break

            # if user chooses to exit
            if key == 0:
                
                # if user has already sold some items
                if len(restock) != 0:
                    self.generate_company_invoice(restock, products) # calling method to generate invoice

                iterate = False
                break # ending the loop

            # if user chooses not to exit
            else:
                
                # loop to deal with non-integer key inputs
                while True:
                    quantity = int(input("Please enter the quantity of  '"+products[key][0]+"' you want to restock: "))
                    
                    try:
                        quantity = int(quantity) # trying to convert the input into an integer
                        break # breaking out of the loop if no error occurs 

                    except:
                        print("_"*48)
                        print("\n!!! The quantity must be a number !!!")
                        print("_"*48)
                
                valid_quantity = False # setting to false because we dont know yet
                
                while not valid_quantity:

                    # checking for negative quantity
                    if quantity < 0:
                        print("_"*48)
                        print("\n!!! The quantity cannot be negative !!!")
                        print("_"*48)
                        quantity = int(input("\nPlease enter a valid quanitity of  '"+products[key][0]+"' you want to restock: "))
                        continue

                    valid_quantity = True # setting to true if both above checks are passed
                    break

                print("_"*70)
                print("\n"+str(quantity)+" x '"+products[key][0]+"' successfully restocked!")
                print("_"*70)

                # The following statement updates the newly created restock dictionary, dynamically.
                # The .get() function of the dictionary tries to get the value of that dictionary from the specified key, if the entry exists.
                # If there is no entry of that specific key, the function will return a 0.

                # This is helpful in this system as the user can append the restock if more items of the same product are restocked later,
                # in the same instance.

                # This dictionary stores only the key and quantity restocked, because it is all that is required to update the stock in the file.

                restock[key] = restock.get(key, 0) + quantity

                # updating the main products dictionary after each restock instance, by increasing the quantity
                products[key][2] =  str(int(products[key][2]) + quantity)

                # calling the set_products method to update the inventory file, with the updated product quantity
                self.writer.set_products(products)
                 
                continue_handling = input("\nAre there other items to be restocked? (y/n): ") # asking if there are more products to be restocked
                
                # loop to handle further choice
                while True:
                    # if user decides to continue
                    if continue_handling == "y" or continue_handling == "yes":
                        iterate = True
                        break

                    # if user decides not to continue
                    elif continue_handling == "n" or continue_handling == "no":
                        self.generate_company_invoice(restock, products) # calling method to generate invoice
                        
                        iterate = False
                        break

                    # if user enters invalid choice
                    else:
                        continue_handling = input("Are there other items to be restocked? (y/n): ").lower()
        
    # for generating customer invoice
    def generate_customer_invoice(self, name, purchase, products):
        """
                Description:
                    Generates the invoice for customers.

                Parameters:
                    name (str) : stores the name of the customer
                    purchase (dict) : contains the ID and quantity of items sold
                    products (dict) : contains all the information of products

                Operations:
                    Generates a unique file name using get_invoice_id() function,
                    Creates an .txt invoice file using the writer object's make_customer_invoice() function,
                    Shows success message.
        """
            
        filename = self.get_invoice_id()+"-"+name+".txt"
        
        content = self.writer.make_customer_invoice(name, purchase, products, filename)
        
        print("_"*60)
        print(self.get_company_logo(), end = "")
        print(content)
        print("\n!!! An invoice '"+filename+"' has successfully been created !!!")
        print("_"*60)
        
    # for generating company invoice
    def generate_company_invoice(self, restock, products):
        """
                Description:
                    Generates the invoice for the company.

                Parameters:
                    restock (dict) : contains the ID and quantity of items restocked
                    products (dict) : contains all the information of products

                Operations:
                    Generates a unique file name using get_invoice_id() function,
                    Creates an .txt invoice file using the writer object's make_company_invoice() function,
                    Shows success message.
        """
        
        filename = self.get_invoice_id()+"-"+"restock"+".txt"
        
        content = self.writer.make_company_invoice(restock, products, filename)

        print("_"*60)
        print(self.get_company_logo(), end = "")
        print(content)
        print("\n!!! An invoice '"+filename+"' has successfully been created !!!")
        print("_"*60)

    def get_invoice_id(self):
        """
                Description:
                    Generates the unique file ID using datetime.

                Parameters:
                    <none>

                Operations:
                    Generates a unique file ID using concatenated current year, month, day, hour, minute and second variables,
                    Returns the unique file ID.
        """
        
        year = str(datetime.now().year)
        month = str(datetime.now().month)
        day = str(datetime.now().day)
        hour = str(datetime.now().hour)
        minute = str(datetime.now().minute)
        second = str(datetime.now().second)

        invoice_id = year+month+day+hour+minute+second # unique id based on date and time

        return invoice_id

    # to get logo of company made using ASCII art
    def get_company_logo(self):
        """
                Description:
                    Generates the logo for the company.

                Parameters:
                    <none>

                Operations:
                    Generates individual lines of the big logo using various characters,
                    Returns the concatenated lines as a single string.
        """
        
        # usage of various characters to create an ASCII art of the company name "WeCare".

        # Here, backslashes are written twice to let the interpreter know that it is just a backslash,
        # and not the starting of an escape sequence.
            
        line1 = " __                      __            ______   \n"
        line2 = " \\    \\                 /    /         /     ____|  \n"
        line3 = "   \\    \\    / \\    /    /____  |    |            ____   _   __  ___   ____\n"
        line4 = "     \\    \\/     \\/    //    _    \\     |          /   ___ `  ||    '___//    _    \\\n"
        line5 = "       \\      /\\      //      ___ /    |___ |   (___|   ||   |       |    ___ /\n"
        line6 = "         \\  /    \\  /    \\_____|\\______ \\____ ,_  ||_ ]         \\____ |\n"

        return line1+line2+line3+line4+line5+line6 # returning concatenated lines


from datetime import datetime 

class FileWriter:

    def __init__(self,file_path):
        """
                Description:
                    Initializes an instance of the FileWriter class.

                Parameters:
                    file_path (str) : stores the file path of the main inventory.txt file

                Operations:
                    Assigns the file_path object variable using the file path from parameter.
        """
    
        self.file_path = file_path

    def set_products(self, products):
        """
                Description:
                    Writes data into the inventory.txt file from products dictionary, following a certain format.

                Parameters:
                    products (dict) : contains all the data of the updated items

                Operations:
                    Opens the inventory.txt for write operation, using the file_path object variable,
                    Extracts Lists from the dictionary values and adds the delimeter in between individual values,
                    Writes them into the file line by line.
        """
        
        file = open(self.file_path,"w") # opening file to write
        
        for attributes in products.values():
            line = "" # declaring an empty line to write to the file
            
            for attribute in attributes:

                # for attributes other than the first one
                if attribute != attributes[0]:
                    line = line + "||" # adding '||' as a divider between attributes
                    
                line = line + attribute # adding attribute to the line

            line = line + "\n" # adding a next line escape statement at the end of the line
            file.write(line) # writing line to the file

        file.close() # closing the file after use

    def make_customer_invoice(self, name, purchase, products, invoice_filename):
        """
                Description:
                    Generates a unique customer invoice file (.txt).

                Parameters:
                    name (str) : stores the name of the customer
                    purchase (dict) : contains the key and quantity of items sold
                    products (dict) : contains all the data of the updated items
                    invoice_filename (str) : stores the unique invoice file name, generated using datetime

                Operations:
                    Calls the make_company_logo() function to get the company logo,
                    Opens the invoice file for write operation, using the invoice_filename parameter,
                    Writes the logo, name, date, sale details, and total cost into the file,
                        while highlighting the cost of each sale and amount saved due to the company policy.
        """
        
        logo = self.make_company_logo() # calling own function to get company logo made by ASCII art
        list_index = 1 # setting list index to 1 initially
        item_cost = 0 # setting item cost to 0 initially
        total_cost = 0 # setting total cost to 0 initially
        total_discount = 0 # setting discount to 0 initially
        indent = "" # indentation for better writing to file
        line6 = "" # empty intially
        date = str(datetime.now().year)+"/"+str(datetime.now().month)+"/"+str(datetime.now().day) # current date

        # header
        line1 = logo 
        line2 = "\n\t\tCustomer Invoice/VAT Bill"+"\n"+str("_"*60)+"\n"
        line3 = "\nName: "+name+"\n"
        line4 = "Purchase Date: "+date+"\n\n\n"

        line5 = "Purchase Details:\n"

        # for loop to iterate over purchased items and their details
        for key, details in purchase.items():

            # extra indentation for purchased products less than 10 in quantity
            if details[0] < 10:
                indent="\t"
            
            item_cost = 2*int(products[key][3])*details[0] # using selling price (2xCostPrice)
            discount = 2*int(products[key][3])*details[1]  # using selling price on free items
            
            line6 = line6 + "\n\t"+str(list_index)+") ["+str(details[0])+" + "+str(details[1]) + " free] x "+products[key][0]+" {"+products[key][1]+", "+products[key][5]+"}\t"+indent+"(Rs. "+str(item_cost)+", Rs. "+str(int(products[key][3])*2)+" each)"
            list_index += 1 # updating index
            total_cost += item_cost # updating total cost
            total_discount += discount # updating total discount

        line7=("\n\n\nTotal Cost: Rs. "+str(total_cost)+" (Rs. "+str(total_discount)+" discount)\n")
        line8=("_"*60)

        content = line1+line2+line3+line4+line5+line6+line7+line8

        file = open(invoice_filename,"w") # creating a new unique file for invoice
        file.write(content)
        file.close()

        return line2+line3+line4+line5+line6+line7+line8 # returning everything except the logo

    def make_company_invoice(self, restock, products, invoice_filename):
        """
                Description:
                    Generates a unique comapny invoice file (.txt).

                Parameters:
                    restock (dict) : contains the key and quantity of items restocked
                    products (dict) : contains all the data of the updated items
                    invoice_filename (str) : stores the unique invoice file name, generated using datetime

                Operations:
                    Calls the make_company_logo() function to get the company logo,
                    Opens the invoice file for write operation, using the invoice_filename parameter,
                    Writes the logo, vendor names, date, restock details, and total cost into the file,
                        while highlighting the cost of each sale.
        """
            
        logo = self.make_company_logo() # calling own function to get company logo made by ASCII art
        list_index = 1 # setting list index to 1 initially
        vendor_names = ""
        total_cost = 0 # setting total cost to 0 initially
        line5 = "" # empty initially
        date = str(datetime.now().year)+"/"+str(datetime.now().month)+"/"+str(datetime.now().day) # current date
        
        line1 = logo+"\n"+"\t\tCompany Invoice/VAT Bill"+"\n"+str("_"*60)+"\n"

        is_first = True # check variable for first iteration
        for key in restock:
            
            # adding comma before the names, after first iteration
            if not is_first:
                vendor_names += ", "
                
            vendor_names += products[key][1]
            is_first = False

        line2 = "\nVendor name(s): "+vendor_names+"\n"
        line3 = "Transaction Date: "+date+"\n\n\n"

        line4 = "Transaction Details:\n"

        # for loop to iterate over purchased items and their details
        for key, quantity in restock.items():

            item_cost = int(products[key][3])*quantity # using CostPrice

            line5 = line5 + "\n\t"+str(list_index)+") ["+str(quantity) + "] x "+products[key][0]+" {"+products[key][1]+", "+products[key][5]+"}\t"+"(Rs. "+str(item_cost)+", Rs. "+products[key][3]+" each)"
            list_index += 1 # updating index
            total_cost += item_cost # updating total cost

        line6 = "\n\n\nTotal Cost: Rs. "+str(total_cost)+"\n"
        line7 = "_"*60

        content =  line1+line2+line3+line4+line5+line6+line7
        
        file = open(invoice_filename,"w") # creating a new unique file for invoice
        file.write(content)
        file.close()

        return line2+line3+line4+line5+line6+line7 # returning everything except the logo

    # function to make ASCII art of WeCare, in a form that is understandable in .txt format
    def make_company_logo(self):
        """
                Description:
                    Generates the logo for the company.

                Parameters:
                    <none>

                Operations:
                    Generates individual lines of the big logo using various characters,
                    Returns the concatenated lines as a single string.
        """
        
        line1="888       888           .d8888b.\n"
        line2="888   o   888          d88P  Y88b\n"
        line3="888  d8b  888          888    888\n"
        line4="888 d888b 888  .d88b.  888         8888b.  888d888 .d88b.\n"
        line5='888d88888b888 d8P  Y8b 888            "88b 888P"  d8P  Y8b\n'
        line6="88888P Y88888 88888888 888    888 .d888888 888    88888888\n"
        line7="8888P   Y8888 Y8b.     Y88b  d88P 888  888 888    Y8b.\n"
        line8='888P     Y888  "Y8888   "Y8888P"  "Y888888 888     "Y8888\n'

        return line1+line2+line3+line4+line5+line6+line7+line8 # returning concatenated lines
            

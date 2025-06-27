class FileReader:

    def __init__(self,file_path):
        """
                Description:
                    Initializes an instance of the FileReader class.

                Parameters:
                    file_path (str) : stores the file path of the main inventory.txt file

                Operations:
                    Assigns the file_path object variable using the file path from parameter.
        """
        
        self.file_path = file_path

    def get_products(self):
        """
                Description:
                    Reads the inventory.txt file and retrieves actual data.

                Parameters:
                    <none>

                Operations:
                    Opens the inventory.txt for read operation, using the file_path object variable,
                    Extracts data from the file by splitting the lines  and delimeter,
                    Puts the extracted data into Lists,
                    Puts the Lists into a dictionary, using increasing numeric ID for the keys,
                    Returns the dictionary.
        """
        
        file = open(self.file_path,"r") # opening file to read
        
        products = {} # empty dictionary to store item data in
        product_id = 1 # numeric id of an item (key)
        data = file.readlines()

        # putting the file contents into a dictionary
        for line in data:
            attributes = line.replace("\n","").split("||")
            products[product_id] = attributes
            product_id+=1 # updating item id by 1 after every item
            
        file.close()
        return products

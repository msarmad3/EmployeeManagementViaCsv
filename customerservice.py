from collections import namedtuple
import csv
import os

Customer = namedtuple("Customer", ["cust_id", "name", "postcode", "phone"])

def validatecustomerid(cust_id):
    try:
        return int(cust_id) >= 100000 and int(cust_id) <= 999999
    except ValueError:
        return False


def generatecustid(existing_customers): #producin unique customer ID by checking against all the existing Ids in customers 
   
    customer_ids = [int(c.cust_id) for c in existing_customers] #getting already used ids
    next_id = 100000
    while next_id in customer_ids:
        next_id += 1
    return str(next_id)

def loadcustomers(filename):
    
    customers = []
    try:
        with open(filename, "r") as csvfile:
            next(csvfile) 
            for row in csvfile:
                data = row.strip().split(",")
                if len(data) != 4:
                    print(f"Warning: Invalid customer data format in row: {row}")
                    continue
                cust_id, name, postcode, phone = data
                customers.append(Customer(cust_id, name, postcode, phone))
    except FileNotFoundError:
        print(f"Error: Customer data file '{filename}' not found.")
    return customers

def savecustomers(customers): #for saveing customer data to a CSV file
  if not customers:
    print("There are no customer records to save. Returning to main menu.")
    return

  while True:
    filename = input("Enter the filename to save customer records (or 'cancel' to exit): ")
    if filename.lower() == 'cancel':
      print("Operation cancelled.")
      return

    #check if file exists
    if os.path.isfile(filename):
      confirmation = input(f"File '{filename}' already exists. Overwrite? (y/n): ")
      if confirmation.lower() != 'y':
        print("Operation cancelled. No file saved.")
        continue  # back to prompt for filename
      
    try:
      with open(filename, "r+", newline="") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["cust_id", "name", "postcode", "phone"])
        for customer in customers:
          writer.writerow([customer.cust_id, customer.name, customer.postcode, customer.phone])
        print(f"Customer records saved to '{filename}'.")
        break  

    except FileNotFoundError:
      confirmation = input(f"File '{filename}' does not exist. Create a new file? (y/n): ")
      if confirmation.lower() == 'y':
            with open(filename, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
               
                writer.writerow(["cust_id", "name", "postcode", "phone"])
            
                for customer in customers:
                    writer.writerow([customer.cust_id, customer.name, customer.postcode, customer.phone])
                print(f"Customer records saved to '{filename}'.")
                break  

    print("Operation cancelled. No file created.")
    break 

def addcustomer(customers, name, postcode="", phone=""):
    
    cust_id = generatecustid(customers) #for auto generating customers IDS
    new_customer = Customer(cust_id, name, postcode, phone)
    customers.append(new_customer) #push new customers to customers array
    return new_customer

def searchcustomers(customers, search): #search for customers based on a input search string
  
    search = search.lower()
    matching = []
    for customer in customers:
        if ( #comparing the search with every attribute as per requirements 
            search in customer.cust_id.lower()
            or search in customer.name.lower()
            or search in customer.postcode.lower()
            or search in customer.phone.lower()
        ):
            matching.append(customer)
    return matching

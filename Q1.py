import csv
from collections import namedtuple
import os

Customer = namedtuple("Customer", ["cust_id", "name", "postcode", "phone"])
Sale = namedtuple("Sale", ["date", "trans_id", "cust_id", "category", "value"])


def validatecustomerid(cust_id): #for keeping the valid customers IDS within 6digit value
    try:
        return int(cust_id) >= 100000 and int(cust_id) <= 999999
    except ValueError:
        return False


def validatetransid(trans_id): #for keeping the valid trans IDS within 9digit value
    try:
        return int(trans_id) >= 100000000 and int(trans_id) <= 999999999
    except ValueError:
        return False


def loadcustomers(filename):
    customers = []
    try:
        with open(filename, "r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            next(reader) #skipping header row
            for row in reader:
                cust_id, name = row[0], row[1]  #as zero index has ID and one index has name
                if cust_id and name is not None: #name and id are required
                    if validatecustomerid(cust_id): #validating customers ID
                        postcode = row[2] if len(row) > 2 else ""
                        phone = row[3] if len(row) > 3 else ""
                        customers.append(Customer(cust_id, name, postcode, phone)) #pushing customer to customers array
                    else:
                        print(f"Invalid customer ID: {cust_id} in {filename}")
                else:
                    print("Customer name and ID are required")
    except FileNotFoundError:
        print(f"Error: Customer file {filename} not found.")
    print("Customers data loaded successful")
    return customers


def loadsales(filename):
  sales = []
  try:
    with open(filename, "r", newline="") as csvfile:
      reader = csv.reader(csvfile)
      next(reader)  #skip the header
      for row in reader:
        #skip empty lines
        if not row:
          continue

        if (len(row) != 5  #check if row length is not 5
            or not validatetransid(row[1])  #check transaction ID
            or not validatecustomerid(row[2])  #check customer ID
           ):
          print(f"Invalid data format or invalid IDs in row: {row} ({filename})")
          continue

        try:
          sales.append(Sale(row[0], row[1], row[2], row[3], row[4]))
        except ValueError:
          print(f"Invalid value format in {filename}")
  except FileNotFoundError:
    print(f"Error: Sales file {filename} not found.")
  print("Sales data loaded successful")
  return sales


def savecustomers(customers):
  if not customers: #if customers array is empty just a check to make sure user loads customers before
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
      with open(filename, "r+", newline="") as csvfile: #r+ mode for writing current file and if it doesnt exist it thorws filenotfounderror
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



def savesales(sales):
 
  if not sales:
    print("There are no sales records to save. Returning to main menu.")
    return

  while True:
    filename = input("Enter the filename to save sales records (or 'cancel' to exit): ")
    if filename.lower() == 'cancel':
      print("Operation cancelled.")
      return

    # Check if file exists
    if os.path.isfile(filename):
      confirmation = input(f"File '{filename}' already exists. Overwrite? (y/n): ")
      if confirmation.lower() != 'y':
        print("Operation cancelled. No file saved.")
        continue  # Loop back to prompt for filename

    try:
      
      with open(filename, "r+", newline="") as csvfile:
        writer = csv.writer(csvfile)
        
        writer.writerow(["date", "trans_id", "cust_id", "category", "value"])
        for sale in sales:
          writer.writerow([sale.date, sale.trans_id, sale.cust_id, sale.category, sale.value])
        print(f"Sales records saved to '{filename}'.")
        break  

    except FileNotFoundError:
     
      confirmation = input(f"File '{filename}' does not exist. Create a new file? (y/n): ")
      if confirmation.lower() == 'y':
            with open(filename, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                
                writer.writerow(["date", "trans_id", "cust_id", "category", "value"])
                
                for sale in sales:
                    writer.writerow([sale.date, sale.trans_id, sale.cust_id, sale.category, sale.value])
                print(f"Sales records saved to '{filename}'.")
                break  

    print("Operation cancelled. No file created.")
    break 


customers = []
sales = []
while True:
    print("\nWestern Wholesales Pty Ltd Menu:")
    print("1. Load customer records")
    print("2. Load sales records")
    print("3. Save customer records")
    print("4. Save sales records")
    print("5. Quit")

    choice = input("Enter your choice (1-5): ")

    if choice == "1":
        customer_file = input("Enter customer file name: ")

        customers = loadcustomers(customer_file)
        #print(customers)
    elif choice == "2":

        sales_file = input("Enter sales file name: ")

        sales = loadsales(sales_file)
        #print(sales)
    elif choice == "3":
        if not customers:
            print("No customer data loaded yet.")
            continue
        
        savecustomers(customers)

    elif choice == "4":
        if not sales:
            print("No sales data loaded yet.")
            continue
       
        savesales(sales)

    elif choice == "5":
        
        print("Exiting program........")
        break

    else:
        print("Invalid choice. Please enter a number between 1 and 5.")
        

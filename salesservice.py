from collections import namedtuple
import csv
from datetime import datetime
import os
from customerservice import (
    validatecustomerid
)

Sale = namedtuple("Sale", ["date", "trans_id", "cust_id", "category", "value"])

def validatetransid(trans_id):
    try:
        return int(trans_id) >= 100000000 and int(trans_id) <= 999999999
    except ValueError:
        return False


def generatetransid(existing_sales): #producin unique sales ID by checking against all the existing sales
    
    transaction_ids = [int(s.trans_id) for s in existing_sales]
    next_id = 100000000
    while next_id in transaction_ids:
        next_id += 1
    return str(next_id)

def validatedate(date_string):#verifying date is in given formate or not
   

    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def loadsales(filename):
  sales = []
  try:
    with open(filename, "r", newline="") as csvfile:
      reader = csv.reader(csvfile)
      next(reader)  # skip the header row
      for row in reader:
        #skip empty lines
        if not row:
          continue

        if (len(row) != 5  #check if row length is not 5
            or not validatetransid(row[1])  #validate transaction ID
            or not validatecustomerid(row[2])  # validate customer ID
           ):
          print(f"Invalid data format or invalid IDs in row: {row} ({filename})")
          continue

        try:
          sales.append(Sale(row[0], row[1], row[2], row[3], row[4]))
        except ValueError:
          print(f"Invalid value format in {filename}")
  except FileNotFoundError:
    print(f"Error: Sales file {filename} not found.")
  return sales


def savesales(sales):
 
  if not sales: #when there is no sale record in current session of memory
    print("There are no sales records to save. Returning to main menu.")
    return

  while True:
    filename = input("Enter the filename to save sales records (or 'cancel' to exit): ")
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
      
      with open(filename, "r+", newline="") as csvfile: #r+ for reading and writing a file
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


def addsale(sales, customer_id, date, category, value):
    
    trans_id = generatetransid(sales)
    if not validatedate(date):
        print("Error: Invalid date format. Please enter date in YYYY-MM-DD format.")
        return None
    try:
        value = float(value)
    except ValueError: #if user has typo mistake. for making an efficient code so that it donot break in near future
        print("Error: Invalid value format. Please enter a numeric value for sale amount.")
        return None
    new_sale = Sale(date, trans_id, customer_id, category, value)
    sales.append(new_sale) #pushing new sale to old sales array of nametuples 
    return new_sale


def searchsales(sales, search_string):
    
    search_string = search_string.lower()
    matching_sales = []
    for sale in sales:
        if (
            search_string in sale.date.lower()
            or search_string in sale.trans_id.lower()
            or search_string in sale.cust_id.lower()
            or search_string in sale.category.lower()
            or search_string in str(sale.value)
        ):
            matching_sales.append(sale)
    return matching_sales


def getcustomersales(sales, customer_id): #getting customers from customersiD from sales recrd
   
    customersales = []
    for sale in sales:
        if sale.cust_id == customer_id:
            customersales.append(sale)
    return customersales

def deletesale(sales, trans_id):
  sale_index = -1
  # Iterate through the sales list to find the sale with the matching transaction ID
  for i, sale in enumerate(sales):
    if sale.trans_id == trans_id:
      sale_index = i
      break  # Exit the loop after finding a matching sale

  if sale_index != -1:
    # If a matching sale was found, delete it from the list at the correct index
    del sales[sale_index]
    print(f"Sale with transaction ID '{trans_id}' deleted successfully.")
    return True
  else:
    # If no matching sale was found, print an error message
    print(f"Error: Sale with transaction ID '{trans_id}' not found.")
    return False

def deletecustomer(sales,customers, customer_id):
  
  customerdeleted = False
  salesdeleted = 0
  # Iterate through the sales list
  for i, sale in enumerate(sales):
    if sale.cust_id == customer_id:
      # Delete the sale and increment deletion count
      del sales[i]
      salesdeleted += 1

  for customer in customers:
    if customer.cust_id == customer_id:
      customers.remove(customer)
      customerdeleted = True
      break  # Exit loop after finding the matching customer
  # Check if any sales were deleted (meaning customer exists)
  if ((salesdeleted > 0) | customerdeleted):
    print(f"Customer ID '{customer_id}' deleted successfully. {salesdeleted} sales associated with this customer were also removed.")
    return True
  else:
    print(f"Error: Customer with ID '{customer_id}' not found.")
    return False
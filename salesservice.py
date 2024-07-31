from collections import namedtuple
import csv
from datetime import datetime


Sale = namedtuple("Sale", ["date", "trans_id", "cust_id", "category", "value"])

def generatetransid(existing_sales):
    
    transaction_ids = [int(s.trans_id) for s in existing_sales]
    next_id = 100000000
    while next_id in transaction_ids:
        next_id += 1
    return str(next_id)

def validatedate(date_string):
   

    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def loadsales(filename):
   
    sales = []
    try:
        with open(filename, "r") as csvfile:
            next(csvfile)  
            for row in csvfile:
                data = row.strip().split(",")
                if len(data) != 5:
                    print(f"Warning: Invalid sale data format in row: {row}")
                    continue
                date, trans_id, cust_id, category, value = data
                if not validatedate(date):
                    print(f"Warning: Invalid date format for sale: {row}")
                    continue
                try:
                    value = float(value)
                except ValueError:
                    print(f"Warning: Invalid value format for sale: {row}")
                    continue
                sales.append(Sale(date, trans_id, cust_id, category, value))
    except FileNotFoundError:
        print(f"Error: Sales data file '{filename}' not found.")
    return sales


def savesales(sales):
 
  if not sales:
    print("There are no sales records to save. Returning to main menu.")
    return

  while True:
    filename = input("Enter the filename to save sales records (or 'cancel' to exit): ")
    if filename.lower() == 'cancel':
      print("Operation cancelled.")
      return

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


def addsale(sales, customer_id, date, category, value):
    
    trans_id = generatetransid(sales)
    if not validatedate(date):
        print("Error: Invalid date format. Please enter date in YYYY-MM-DD format.")
        return None
    try:
        value = float(value)
    except ValueError:
        print("Error: Invalid value format. Please enter a numeric value for sale amount.")
        return None
    new_sale = Sale(date, trans_id, customer_id, category, value)
    sales.append(new_sale)
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


def getcustomersales(sales, customer_id):
   
    customer_sales = []
    for sale in sales:
        if sale.cust_id == customer_id:
            customer_sales.append(sale)
    return customer_sales

def deletesale(sales, trans_id):
   
    sale_index = -1
    for i, sale in enumerate(sales):
        if sale.trans_id == trans_id:
            sale_index = i
            break

    if sale_index != -1:
        del sales[sale_index]
        print(f"Sale with transaction ID '{trans_id}' deleted successfully.")
        return True
    else:
        print(f"Error: Sale with transaction ID '{trans_id}' not found.")
        return False

def deletecustomer(sales, customer_id):
    
    customer_index = -1
    sales_deleted = 0
    for i, sale in enumerate(sales):
        if sale.cust_id == customer_id:
            sales_deleted += 1
            del sales[i]
        elif customer_index == -1 and sale.cust_id == customer_id:
            customer_index = i

    if customer_index != -1:
        del sales[customer_index]
        print(f"Customer ID '{customer_id}' deleted successfully. {sales_deleted} sales associated with this customer were also removed.")
        return True
    else:
        print(f"Error: Customer with ID '{customer_id}' not found.")
        return False

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

from customerservice import (
    addcustomer,
    loadcustomers,
    savecustomers,
    searchcustomers
)
from salesservice import (
    addsale,
    loadsales,
    savesales,
    searchsales,
    getcustomersales,
    deletesale,
    deletecustomer
)

# customerdata = ''
# salesdata = ''


def analyzesalesbymonth(sales): # Group sales by month


  monthsales = {}
  for sale in sales:
    sale_date = datetime.strptime(sale.date, "%Y-%m-%d")  #parse date string using built in method of datetime

    month = sale_date.strftime("%Y-%m")  # getting yearmonth string using strftime on datetime object

    if month not in monthsales:
      monthsales[month] = {"total_value": 0, "sale_count": 0}
    monthsales[month]["total_value"] += sale.value
    monthsales[month]["sale_count"] += 1

  # SETTING monthly and sales data into separate Numpy arrays
  months = np.array(list(monthsales.keys()))
  total_sales = np.array([monthsales[m]["total_value"] for m in months], dtype=float)
  sale_counts = np.array([monthsales[m]["sale_count"] for m in months])
  print(months)
  print(total_sales)
  print(sale_counts)
   


  # for graph creation
  plt.figure(figsize=(14, 7))
  plt.plot(months, total_sales, label='Total Sales')
  plt.plot(months, sale_counts, label='Sale Count')
  plt.title('Monthly Sales Performance')
  plt.xlabel('Month')
  plt.ylabel('Sales Value/Count')
  plt.legend()
  plt.grid(True)
  plt.xticks(rotation=45)  #rotatig x-axis labels for 45 degree to be visible clearly

  plt.show()


def analyzesalesbycustomer(sales, customer_id):

  customer_sales = [sale for sale in sales if sale.cust_id == customer_id]

  if not customer_sales:
    print(f"No sales found for customer ID '{customer_id}'.")
    return

  #calculate monthly sales and sale count data
  monthsales = {}
  for sale in customer_sales:
    sale_date = datetime.strptime(sale.date, "%Y-%m-%d")
    month = sale_date.strftime("%Y-%m")

    if month not in monthsales:
      monthsales[month] = {"total_value": 0, "sale_count": 0}
    monthsales[month]["total_value"] += sale.value
    monthsales[month]["sale_count"] += 1

  months = [month for month in monthsales.keys()]  #extract month strings
  total_sales = [monthsales[m]["total_value"] for m in months]
  sale_counts = [monthsales[m]["sale_count"] for m in months]

  #plot the graph with two lines in one axis
  plt.figure(figsize=(14, 7))
  plt.plot(months, total_sales, label='Total Sales')
  plt.plot(months, sale_counts, label='Sale Count')
  plt.title(f'Monthly Sales Trends (Customer ID: {customer_id})')
  plt.xlabel('Month')
  plt.ylabel('Sales Value/Count')
  plt.legend()
  plt.grid(True)
  plt.xticks(rotation=45, ha='right')  #rotate x-axis labels for better visibility
  plt.show()

def analyzesalesbypostcode(sales, customers, postcode):

  postcode_customers = [customer.cust_id for customer in customers if customer.postcode == postcode]
  postcode_sales = [sale for sale in sales if sale.cust_id in postcode_customers]

  if not postcode_sales:
    print(f"No sales found for postcode '{postcode}'.")
    return

  #calculate monthly sales and sale count data
  monthsales = {}
  for sale in postcode_sales:
    sale_date = datetime.strptime(sale.date, "%Y-%m-%d")
    month = sale_date.strftime("%Y-%m")

    if month not in monthsales:
      monthsales[month] = {"total_value": 0, "sale_count": 0}
    monthsales[month]["total_value"] += sale.value
    monthsales[month]["sale_count"] += 1

  months = [month for month in monthsales.keys()]  #extract month strings
  total_sales = [monthsales[m]["total_value"] for m in months]
  sale_counts = [monthsales[m]["sale_count"] for m in months]

  #plot the graph with two lines in one axis
  plt.figure(figsize=(14, 7))
  plt.plot(months, total_sales, label='Total Sales')
  plt.plot(months, sale_counts, label='Sale Count')
  plt.title(f'Monthly Sales Trends (Postcode: {postcode})')
  plt.xlabel('Month')
  plt.ylabel('Sales Value/Count')
  plt.legend()
  plt.grid(True)
  plt.xticks(rotation=45, ha='right')  #rotate x-axis labels for better visibility
  plt.show()

while True:
    print("Western Wholesales Customer and Sales Management Software")
    print("1. Load customer data from CSV")
    print("2. Save customer data to CSV")
    print("3. Add a new customer")
    print("4. Search for customers")
    print("5. Load sales data from CSV")
    print("6. Save sales data to CSV")
    print("7. Add a new sale")
    print("8. Search for sales")
    print("9. Display sales for a customer")
    print("10. Delete a sale")
    print("11. Delete a customer")
    print("12. Monthly sales analysis graph")
    print("13. Monthly sales with customerID analysis graph")
    print("14. Monthly sales analysis on postcode graph")
    print("15. Exit")

    c = input("Choose Option from 1-15: ")




    if c == "1":
        customerdata = input("Enter customer file name: ")
        customers = loadcustomers(customerdata)
        print("Customer data loaded successfully....")

    elif c == "2":
        savecustomers(customers)
        print("Customer data saved successfully.....")

    elif c == "3":
        name = input("Enter customer name: ")
        postcode = input("Enter customer postcode (optional): ")
        phone = input("Enter customer phone number (optional): ")
        newcustomer = addcustomer(customers, name, postcode, phone)
        print(f"Customer added successfully..... Customer ID: {newcustomer.cust_id}")

    elif c == "4":
        searchstring = input("Enter search string: ")
        matchingcustomers = searchcustomers(customers, searchstring)
        if matchingcustomers:
            print("Matching Customers:")
            for customer in matchingcustomers:
                print(f"- Customer ID: {customer.cust_id}, Name: {customer.name}")
        else:
            print("No matching customers found.")

    elif c == "5":
        salesdata = input("Enter sales file name: ")
        sales = loadsales(salesdata)
        print("Sales data loaded successfully.....")

    elif c == "6":
        savesales(sales)
        print("Sales data saved successfully.....")

    elif c == "7":
        customer_id = input("Enter customer ID: ")
        if customer_id not in [c.cust_id for c in customers]:
            print(f"Error: Customer with ID {customer_id} not found.")
            continue
        date = input("Enter sale date (YYYY-MM-DD): ")
        category = input("Enter sale category: ")
        try:
            value = float(input("Enter sale value: "))
        except ValueError:
            print("Error: Invalid value format.")
            continue
        new_sale = addsale(sales, customer_id, date, category, value)
        if new_sale:  
            print(f"Sale added successfully! Transaction ID: {new_sale.trans_id}")
        else:
            print("Error adding sale. Please check data format and try again.")

    elif c == "8":
        searchstring = input("Enter search string: ")
        matchingsales = searchsales(sales, searchstring)
        if matchingsales:
            print("Matching Sales:")
            for sale in matchingsales:
                print(f"- Transaction ID: {sale.trans_id}, Customer ID: {sale.cust_id}, Date: {sale.date}, Category: {sale.category}, Value: ${sale.value:.2f}"
                 )
        else:
            print("No matching sales found.")

    elif c == "9":
        customer_id = input("Enter customer ID: ")
        if customer_id not in [c.cust_id for c in customers]:
            print(f"Error: Customer with ID {customer_id} not found.")
            continue
        customersales = getcustomersales(sales, customer_id)
        if customersales:
            print(f"Sales for customer ID {customer_id}:")
            for sale in customersales:
                print(
                    f"- Transaction ID: {sale.trans_id}, Date: {sale.date}, Category: {sale.category}, Value: ${sale.value:.2f}"
                 )
        else:
            print(f"No sales found for customer ID {customer_id}.")

    elif c == "10":
        trans_id = input("Enter transaction ID of the sale to delete: ")
        deletesale(sales, trans_id)
    elif c == "11":
        customer_id = input("Enter customer ID to delete: ")
        if deletecustomer(sales, customer_id):
            print('Customer deleted')
        else:
            print("Deletion failed.")
    elif c == "12":
        analyzesalesbymonth(sales)
        continue
    elif c == "13":
        customer_id = input("Enter customer ID to analyze: ")
        analyzesalesbycustomer(sales,customer_id)
        continue
    elif c == "14":
        pcode = input("Enter PostCode to analyze: ")
        analyzesalesbypostcode(sales,customers,pcode)
        continue
    elif c == "15":
        print("Exiting program...")
        break

    else:
        print("Invalid choice. Please enter a number between 1 and 12.")

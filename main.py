
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
    print("12. Exit")




    c = input("Enter your choice (1-12): ")




    if c == "1":
        customerdata = input("Enter customer file name: ")
        customers = loadcustomers(customerdata)
        print("Customer data loaded successfully!")



    elif c == "2":
        savecustomers(customers)
        print("Customer data saved successfully!")


    elif c == "3":
        name = input("Enter customer name: ")
        postcode = input("Enter customer postcode (optional): ")
        phone = input("Enter customer phone number (optional): ")
        n = addcustomer(customers, name, postcode, phone)
        print(f"Customer added successfully! Customer ID: {n.cust_id}")


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
        print("Sales data loaded successfully!")


    elif c == "6":
        savesales(sales)
        print("Sales data saved successfully!")


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
                print(f"- Transaction ID: {sale.trans_id}, Customer ID: {sale.cust_id}, Date: {sale.date}, Category: {sale.category}, Value: ${sale.value}")
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
                    f"- Transaction ID: {sale.trans_id}, Date: {sale.date}, Category: {sale.category}, Value: ${sale.value}"
                 )
        else:
            print(f"No sales found for customer ID {customer_id}.")

    elif c == "10":
        trans_id = input("Enter transaction ID of the sale to delete: ")
        deletesale(sales, trans_id)
    elif c == "11":
        customer_id = input("Enter customer ID to delete: ")
        if deletecustomer(sales,customers, customer_id):
            print('Customer deleted')
        else:
            print("Deletion failed.")
    elif c == "12":
        print("Exiting program...")
        break


    else:
        print("Invalid choice. Please enter a number between 1 and 12.")

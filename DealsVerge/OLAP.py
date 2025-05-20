import mysql.connector

mydb=mysql.connector.connect(host="localhost",user="root",passwd="tiger",database="dealsverge")
 
#OLAP 1
mycursor=mydb.cursor(buffered=True)
mycursor.execute('''select State, Count(Customer_ID) as 
                 Number_of_Customers 
                 from customers 
                 GROUP BY State
                 UNION ALL
                 select NULL, Count(Customer_ID) 
                 as Number_of_Customers
                 from customers''')

print("State",'\t',"Number of Customers")
for x in mycursor:
    if(x[0]==None):
        print("Total"," "*(15),x[1])
    else:
        print(x[0]," "*(20-len(x[0])),x[1])
        
print()
#OLAP 2
cur=mydb.cursor(buffered=True)
cur.execute('''select Category_Name ,Count(Manufacturer_ID) as Number_of_Manufacturers 
            from manufacturer 
            GROUP BY Category_Name WITH ROLLUP''')
print("Category Name",'\t',"Number of Manufacturers")
for x in cur:
    if(x[0]==None):
        print("Total"," "*(15),x[1])
    else:
        print(x[0]," "*(20-len(x[0])),x[1])

print()       
#OLAP 3
cur2=mydb.cursor(buffered=True)
cur2.execute('''select Manager_ID ,Count(Seller_ID) as Number_of_Sellers 
             from sellers 
             GROUP BY Manager_ID WITH ROLLUP''')
print("Manager ID",'\t',"Number of seller")
for x in cur2:
    if(x[0]==None):
        print("Total"," "*(15),x[1])
    else:
        print(x[0]," "*(20-len(x[0])),x[1])

print()        
#OLAP 4
cur3=mydb.cursor(buffered=True)
cur3.execute('''select Product_Name,sum(Price) as Amount,Category_Name 
             from products 
             GROUP BY Category_Name,Product_Name WITH ROLLUP''')
print("Product Name",'\t',"    Amount",'\t\t',"Category Name")
for x in cur3:
    if(x[0]==None):
        print("Total"," "*(15),x[1]," "*(20-len(str(x[1]))),x[2])
        print()
    else:
        print(x[0]," "*(20-len(x[0])),x[1]," "*(20-len(str(x[1]))),x[2])

print()
#OLAP 5
cur4=mydb.cursor(buffered=True)
cur4.execute('''SELECT
                orders.Customer_ID,
                products.Category_Name,
                SUM(order_details.Quantity) AS TotalQuantity,
                SUM(order_details.Quantity * order_details.Amount) AS TotalRevenue
            FROM
                orders
                JOIN order_details ON orders.Order_ID = order_details.Order_ID
                JOIN products ON order_details.Product_ID = products.Product_ID
            GROUP BY
                orders.Customer_ID, products.Category_Name with rollup''')
print("Customer ID",'\t\t',"Category Name",'\t\t',"Total Quantity",'\t\t',"Revenue")
for x in cur4:
    print(x[0],'\t\t\t',x[1],'\t\t\t',x[2],'\t\t\t',x[3])
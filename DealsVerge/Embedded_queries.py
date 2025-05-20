import mysql.connector

mydb=mysql.connector.connect(host="localhost",user="root",passwd="tiger",database="dealsverge")


#Query 1
mycursor=mydb.cursor(buffered=True) 
mycursor.execute('''select A.First_Name as Manager_Name, B.Name,B.Category_Name 
                 from Managers A,Manufacturer B 
                 where B.Number_Of_Products between 40000 and 60000 and 
                 A.Manager_ID=B.Manager_ID''')
print("Manager Name",'\t',"     Manufacturer Name",'\t\t\t',"Category Name")
for x in mycursor:
    print(x[0]," "*(20-len(x[0])),x[1]," "*(40-len(x[1])),x[2])

#Query 2
cursor=mydb.cursor(buffered=True)
cursor.execute('''select Product_Name ,Price,Quantity, Price*Quantity as Total_Price 
                 from Products where 
                 Price*Quantity>(Select AVG(Price*Quantity) from Products)''')
print("Product Name",'\t',"   Quantity",'\t\t',"   Price",'\t\t',"Total Amount")
for x in mycursor:
    print(x[0]," "*(20-len(x[0])),x[1]," "*(20-len(str(x[1]))),x[2]," "*(20-len(str(x[2]))),x[3])


#Query 3
mycursor1=mydb.cursor(buffered=True)
mycursor1.execute('''select First_Name from customers 
                 RIGHT JOIN orders on customers.Customer_ID=orders.Customer_ID 
                 where orders.Amount>500''')
print("Customers with Order Value > 500")
for x in mycursor:
    print(x[0])
    
mydb.close()
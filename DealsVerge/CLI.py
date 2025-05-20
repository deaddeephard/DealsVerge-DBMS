import datetime
from datetime import date
import mysql.connector as mydb
db=mydb.connect(host="localhost",user="root",passwd="tiger",database="dealsverge")
 
def calculateAge(birthDate):
    today = date.today()
    age = today.year - birthDate.year -((today.month, today.day) <(birthDate.month, birthDate.day))
    return age

def main_menu():
    n=0
    while n!=5:
        print("**************---DealsVerge---******************")
        print("1) Enter as Customer")
        print("2) Enter as Delivery Partner")
        print("3) Enter as Seller")
        print("4) Enter as Manager")
        print("5) Enter as Admin")
        print("6) Exit")
        print()
        n=int(input("Enter your choice :: "))
        print()
        if n==1:
            customer()
        elif n==2:
            delivery()
        elif n==3:
            seller()
        elif  n==4:
            manager()
        elif n==5:
            admin()
        elif n==6:
            exit()
        else:
            print("Invalid Input")
        
def customer():
    print()
    n=0
    while n!=3:
        print("Welcome to DealsVerge")
        print("1) Sign In")
        print("2) Sign Up")
        print("3) Go Back")
        print()
        n=int(input("Enter your choice :: "))
        print()
        if n==1:
            email=str(input("Enter your email id :: "))
            passwd=str(input("Enter password :: "))
            print()
            cursor=db.cursor(buffered=True)
            cursor.execute("select * from customers")
            f=0
            for x in cursor:
                if x[3]==email and x[5]==passwd:
                    f=1
                    print("Sign In Successful")
                    id=x[0]
                    name=x[1]+" "+x[2]
                    customer_sign(id,name)
            if f==0:
                print("Invalid Data")
                print()
                customer()
                    
        elif n==2:
            print()
            fname=str(input("Enter first name ::"))
            lname=str(input("Enter last name ::"))
            email=str(input("Enter email ::"))
            phno=int(input("Enter phone number ::"))
            passwd=str(input("Enter password ::"))
            gender=str(input("Enter your gender ::"))
            dob=str(input("Enter DOB (YYYY-MM-DD) ::"))
            dob=dob.split('-')
            year=int(dob[0])
            month=int(dob[1])
            dat=int(dob[2])
            now=datetime.date(year,month,dat)
            age=calculateAge(now)
            hno=str(input("Enter house no. ::"))
            street=str(input("Enter street name ::"))
            city=str(input("Enter city name ::"))
            pin=int(input("Enter PINCODE ::"))
            state=str(input("Enter state ::"))
            cursor=db.cursor(buffered=True)
            cursor.execute("select Customer_ID from customers order by Customer_ID desc LIMIT 1")
            strg=""
            for x in cursor:
                strg=x[0]
            s2=int(strg[1:])
            s2+=1
            if(s2<1000):
                s=strg[0]+"0"+str(s2)
            else:
                s=strg[0]+str(s2)
                
            cursor1=db.cursor(buffered=True)
            cursor1.execute("SAVEPOINT add_customer")
            query='insert into customers values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            t=(s,fname,lname,email,phno,passwd,gender,now,age,hno,street,city,pin,state)
            cursor1.execute(query,t)
            
            check_email_query = 'SELECT COUNT(*) FROM customers WHERE Email_ID = %s'
            cursor1.execute(check_email_query,[email])
            num_customers_with_email = cursor1.fetchone()[0]
            
            if num_customers_with_email > 1:
                print()
                print("Email-ID already registered")
                print("Cannot register with this Email-ID")
                # roll back to the savepoint and discard the changes since then
                cursor1.execute("ROLLBACK TO add_customer")
                cursor1.execute("RELEASE SAVEPOINT add_customer")
            else:
                # commit the transaction
                cursor1.execute("COMMIT")
                print()
                print("Registered successfully")
                print("Please Sign In")
                
            print()
            customer()
        elif n==3:
            print()
            main_menu()
        else:
            print()
            print("Invalid Option")
            print()
        
def customer_sign(id,name):
    print("Welcome",name)
    m=0
    while m!=6:
        print("1) Update your Profile")
        print("2) View Categories and browse Products")
        print("3) View / Update Cart")
        print("4) View Orders")
        print("5) Place Order")
        print("6) Log Out")
        print()
        m=int(input("Enter Your Choice:: "))
        if m==1:
            print()
            update(id,name)
        elif m==2:
            print()
            view_products(id,name)
        elif m==3:
            print()
            view_cart(id,name)
        elif m==4:
            print()
            view_orders(id)
        elif m==5:
            print()
            order(id)
        elif m==6:
            customer()
        else:
            print("Invalid Option")

def update(id,name):
    print()
    m=0
    while m!=5:
        print()
        print("What do you want to update ?")
        print("1) Password")
        print("2) Phone Number")
        print("3) Email ID")
        print("4) Address")
        print("5) Go Back")
        print()
        m=int(input("Enter your choice :: "))
        if m==1:
            passwd=str(input("Enter new password ::"))
            cursor = db.cursor(buffered=True)
            update_customer_query = "UPDATE customers SET Password = %s WHERE Customer_ID = %s"
            cursor.execute(update_customer_query, (passwd,id))
            print("Password updated successfully")
            db.commit()
                
        elif m==2:
            phno=int(input("Enter new phone number ::"))
            cursor = db.cursor(buffered=True)
            cursor.execute("SAVEPOINT update_customer_phno")
            update_customer_query = "UPDATE customers SET Phone_Number = %s WHERE Customer_ID = %s"
            cursor.execute(update_customer_query, (phno, id))
            check_email_query = "SELECT COUNT(*) FROM customers WHERE Phone_Number = %s AND Customer_ID != %s"
            cursor.execute(check_email_query, (phno, id))
            num_customers_with_phno = cursor.fetchone()[0]
            if num_customers_with_phno > 0:
                print("Cannot Update phone number")
                print("Phone Number already registered")
                cursor.execute("ROLLBACK TO update_customer_phno")
                cursor.execute("RELEASE SAVEPOINT update_customer_phno")
            else:
                print("Phone Number updates succesfully")
                cursor.execute("COMMIT")
            
        elif m==3:
            email=str(input("Enter new email ::"))
            cursor = db.cursor(buffered=True)
            cursor.execute("SAVEPOINT update_customer_email")
            update_customer_query = "UPDATE customers SET Email_ID = %s WHERE Customer_ID = %s"
            cursor.execute(update_customer_query, (email, id))
            check_email_query = "SELECT COUNT(*) FROM customers WHERE Email_ID = %s AND Customer_ID != %s"
            cursor.execute(check_email_query, (email, id))
            num_customers_with_email = cursor.fetchone()[0]
            if num_customers_with_email > 0:
                print("Cannot updated Email_ID")
                print("Email_ID already registered")
                cursor.execute("ROLLBACK TO update_customer_email")
                cursor.execute("RELEASE SAVEPOINT update_customer_email")
            else:
                print("Email_ID updated succesfully")
                cursor.execute("COMMIT;")
            
            
        elif m==4:
            print("Enter new address")
            hno=str(input("Enter house no. ::"))
            street=str(input("Enter street name ::"))
            city=str(input("Enter city name ::"))
            pin=int(input("Enter PINCODE ::"))
            state=str(input("Enter state ::"))
            cursor = db.cursor(buffered=True)
            update_query = "UPDATE customers SET House_Number = %s, Street = %s, City = %s , PIN = %s , State = %s WHERE Customer_ID = %s;"
            cursor.execute(update_query, (hno,street,city,pin,state))
            db.commit()
            
        elif m==5:
            customer_sign(id,name)
            
        else:
            print("Invalid Option")
             
def view_products(id,name):
    print()
    v=0
    while(v!=5):
        j=1
        cursor1=db.cursor(buffered=True)
        cursor1.execute("select distinct(Category_Name) from products")
        for x in cursor1:
            print(j,") ",x[0])
            j=j+1
        print(j,")  Go Back")
        v=int(input("Enter Category NUmber you wish to browse ::"))
        print()
        if v==1:
            cursor=db.cursor(buffered=True)
            cursor.execute("select Product_ID, Product_Name, Price ,Quantity from products where Category_ID='CT001'")
            print()
            i=1
            print("S.No",'\t',"Product_ID",'\t',"Name",'\t\t'," Price","\t","Stock")
            for x in cursor:
                print(i,")",'\t',x[0],'\t\t',x[1]," " * (20 - len(x[0]) - len(x[1])),x[2]," " * (10 - len(str(x[2]))),x[3])
                i=i+1
            print()
            print("Add products to cart ?")
            y=str(input("Y/N : "))
            if(y=='Y' or y=='y'):
                add_to_cart(id)
        elif v==2:
            cursor=db.cursor(buffered=True)
            cursor.execute("select Product_ID, Product_Name, Price,Quantity from products where Category_ID='CT002'")
            print()
            i=1
            print("S.No",'\t',"Product_ID",'\t',"Name",'\t\t'," Price","\t","Stock")
            for x in cursor:
                print(i,")",'\t',x[0],'\t\t',x[1]," " * (20 - len(x[0]) - len(x[1])),x[2]," " * (10 - len(str(x[2]))),x[3])
                i=i+1
            print()
            print("Add products to cart ?")
            y=str(input("Y/N : "))
            if(y=='Y' or y=='y'):
                add_to_cart(id)
        elif v==3:
            cursor=db.cursor(buffered=True)
            cursor.execute("select Product_ID, Product_Name, Price,Quantity from products where Category_ID='CT003'")
            print()
            i=1
            print("S.No",'\t',"Product_ID",'\t',"Name",'\t\t'," Price","\t","Stock")
            for x in cursor:
                print(i,")",'\t',x[0],'\t\t',x[1]," " * (20 - len(x[0]) - len(x[1])),x[2]," " * (10 - len(str(x[2]))),x[3])
                i=i+1
            print()
            print("Add products to cart ?")
            y=str(input("Y/N : "))
            if(y=='Y' or y=='y'):
                add_to_cart(id)
        elif v==4:
            cursor=db.cursor(buffered=True)
            cursor.execute("select Product_ID, Product_Name, Price ,Quantity from products where Category_ID='CT004'")
            print()
            i=1
            print("S.No",'\t',"Product_ID",'\t',"Name",'\t\t'," Price","\t","Stock")
            for x in cursor:
                print(i,")",'\t',x[0],'\t\t',x[1]," " * (20 - len(x[0]) - len(x[1])),x[2]," " * (10 - len(str(x[2]))),x[3])
                i=i+1
            print()
            print("Add products to cart ?")
            y=str(input("Y/N : "))
            if(y=='Y' or y=='y'):
                add_to_cart(id)
        elif v==5:
            customer_sign(id, name)
        else:
            print("Invalid Option")
            main_menu()
    print()
    print("Cart updated successfully")
    print()
            
def view_cart(id,name):
    print()
    n=0
    while(n!=4):
        print()
        print("1) View Cart")
        print("2) Delete from Cart")
        print("3) Add more products")
        print("4) Go Back")
        print()
        n=int(input("Enter your choice :: "))
        if n==1:
            cur=db.cursor(buffered=True)
            q="select * from cart_items where Customer_ID=%s"
            cur.execute(q,[id])
            i=1
            print("S.No",'\t',"Product_ID",'\t'," Name",'\t',"     Quantity",'\t\t',"Price")
            for x in cur:
                print(i,")",'\t',x[2]," " * (15- len(x[2])),x[3],'\t',x[4],'\t\t',x[5])
                i+=1
            print()
        elif n==2:
            print("Your Cart contains following products::")
            cur=db.cursor(buffered=True)
            q="select * from cart_items where Customer_ID=%s"
            cur.execute(q,[id])
            i=1
            print("S.No",'\t',"Product_ID",'\t'," Name",'\t',"     Quantity",'\t\t',"Price")
            for x in cur:
                print(i,")",'\t',x[2]," " * (15- len(x[2])),x[3],'\t',x[4],'\t\t',x[5])
                i+=1
            print()
            ids=str(input("Enter the Product ID you want to delete  :: "))
            cur7=db.cursor(buffered=True)
            q="select Quantity from cart_items where Product_ID=%s and Customer_ID=%s"
            cur7.execute(q,[ids,id])
            quan=0
            for x in cur7:
                quan=x[0]
            cur1=db.cursor(buffered=True)
            q="delete from cart_items where Product_ID=%s and Customer_ID=%s"
            cur1.execute(q,[ids,id])
            db.commit()
            cur2=db.cursor(buffered=True)
            qu="UPDATE cart SET Number_Of_Items = Number_Of_Items-%s WHERE Customer_ID = %s"
            cur2.execute(qu,[quan,id])
            db.commit()
            print()
            print("Cart updated successfully")
            print()
        elif n==3:
            view_products(id,name)
        elif n==4:
            customer_sign(id, name)
        else:
            print("Invalid Option")
            
def view_orders(id):
    print()
    cur=db.cursor(buffered=True)
    q="select Order_ID,Order_Status,Date,Mode_Of_Payment,Amount,Discount,Amount_with_Discount from orders where Customer_ID=%s"
    cur.execute(q,[id])
    print("Order ID",'\t',"Status",'\t\t',"Date Placed",'\t',"Mode of Payment",'\t',"Total Price",'\t',"Discount",'\t',"Amount Payable")
    for x in cur:
        print(x[0],'\t\t',x[1]," "*(20-len(x[1])),x[2],'\t\t',x[3],'\t\t',x[4],'\t\t',x[5],'\t\t',x[6])
    print()
 
def add_to_cart(id):
    print()
    b=int(input("Enter number of products you want to add ::"))
    lst=[]
    ls=[]
    quan=0
    for i in range (b):
        pid=str(input("Enter Product_ID you wish to add ::"))
        amount=int(input("Enter quantity :: "))
        quan+=amount
        lst.append(pid)
        ls.append(amount)
    cur=db.cursor(buffered=True)
    cur.execute("Select Customer_ID from cart")
    temp=False
    for x in cur:
        if x[0]==id:
            temp=True
    if temp:
        cur1=db.cursor(buffered=True)
        q="select Number_Of_Items from cart where Customer_ID = %s"
        cur1.execute(q,[id])
        o=0
        for x in cur1:
            o=x[0]
        cur2=db.cursor(buffered=True)
        qu="UPDATE cart SET Number_Of_Items = %s WHERE Customer_ID = %s"
        cur2.execute(qu,[o+quan,id])
        db.commit()
    else:
        cur3=db.cursor(buffered=True)
        qu="Insert into cart values(%s,%s)"
        t=(id,quan)
        cur3.execute(qu,t)
        db.commit()
    cart(id,lst,ls)

def cart(id,prodidlist,quanlist):
    print()
    for i in range(0,len(prodidlist)):
        cur=db.cursor(buffered=True)
        cur.execute("SAVEPOINT update_cart")
        q="select Product_Name,Price from products where Product_ID=%s"
        cur.execute(q,[prodidlist[i]])
        nm=""
        pr=""
        for x in cur:
            nm=x[0]
            pr=x[1]
        price=quanlist[i]*int(pr)
        name=nm
        cur.execute("select SNo from cart_items order by SNo desc LIMIT 1")
        sg=""
        st=0
        for x in cur:
            sg=x[0]
        if(sg==""):
            st=1
        else:
            st=int(sg)+1
        q="insert into cart_items values(%s,%s,%s,%s,%s,%s)"
        t=(st,id,prodidlist[i],name,quanlist[i],price)
        cur.execute(q,t)
        q="Select Quantity from products where Product_ID=%s"
        cur.execute(q,[prodidlist[i]])
        quantity = cur.fetchone()[0]
        if(quantity<quanlist[i]):
            print("Cannot add to cart")
            print("Product not in stock")
            cur.execute("ROLLBACK TO update_cart")
            cur.execute("RELEASE SAVEPOINT update_cart")
            cur2=db.cursor(buffered=True)
            qu="UPDATE cart SET Number_Of_Items = Number_Of_Items - %s WHERE Customer_ID = %s"
            cur2.execute(qu,[quanlist[i],id])
            db.commit()
        else:
            cur.execute("COMMIT")
        
def order(id):
    print()
    cursor=db.cursor(buffered=True)
    cursor.execute("select Order_ID from orders order by Order_ID desc LIMIT 1")
    strg=""
    for x in cursor:
        strg=x[0]
    s2=int(strg[2:])
    s2+=1
    s=strg[0:2]+str(s2)
    today = date.today()
    mod=str(input("Enter the mode of payment (COD/Online) :: "))
    cur2=db.cursor(buffered=True)
    q="select * from cart_items where Customer_ID= %s"
    cur2.execute(q,[id])
    for x in cur2:
        prodid=x[2]
        prodname=x[3]
        quan=x[4]
        amount=x[5]
        cursor1=db.cursor(buffered=True)
        cursor1.execute("select SNo from order_details order by SNo desc LIMIT 1")
        sg=""
        st=0
        for x in cursor1:
            sg=x[0]
        if(sg==""):
            st=1
        else:
            st=int(sg)+1
        cur3=db.cursor(buffered=True)
        q="insert into order_details values(%s,%s,%s,%s,%s,%s)"
        t=(st,s,prodid,prodname,quan,amount)
        cur3.execute(q,t)
        db.commit()
        
    cur1=db.cursor(buffered=True)
    
    q="insert into orders values(%s,%s,%s,%s,%s,%s,%s,%s)"
    t=(s,id,"Packed",today,mod,10,0,0)
    cur1.execute(q,t)
    db.commit()
    cur9=db.cursor(buffered=True)
    q="select sum(Amount) from order_details where Order_ID=%s"
    cur9.execute(q,[s])
    amt=0
    for x in cur9:
        amt=x[0]
    cur6=db.cursor(buffered=True)
    q="UPDATE orders set Amount=%s where Order_ID=%s"
    cur6.execute(q,[amt,s])
    db.commit()
    ad=amt-(amt/10)
    cur8=db.cursor(buffered=True)
    q="UPDATE orders set Amount_with_Discount =%s where Order_ID=%s"
    cur8.execute(q,[ad,s])
    db.commit()
    cur9=db.cursor(buffered=True)
    cur11=db.cursor(buffered=True)
    q="delete from orders where Amount=0"
    cur11.execute(q)
    db.commit()
    q="delete from cart where Customer_ID=%s"
    cur9.execute(q,[id])
    db.commit()
    cur10=db.cursor(buffered=True)
    q="delete from cart_items where Customer_ID=%s"
    cur10.execute(q,[id])
    db.commit()
    c=db.cursor(buffered=True)
    q="insert into payments values (%s,%s,%s)"
    t=(s,id,ad)
    c.execute(q,t)
    db.commit()
    cur12=db.cursor(buffered=True)
    q="Update customers set Payment = Payment + %s where Customer_ID=%s"
    t=(ad,id)
    cur12.execute(q,t)
    db.commit()
    print()
    print("Total Amount = ",amt)
    print("Amount to be paid (after discount) = ",ad)
    print("Order Placed Succesfully")
    print()
            
def delivery():
    print("--Login--")
    uname=str(input("Enter first name ::")) 
    passwd=str(input("Enter ID ::"))
    cursor=db.cursor(buffered=True)
    cursor.execute("select * from delivery_partners")
    f=1
    for x in cursor:
        if x[1]==uname and x[0]==passwd:
            f=0
            print("Sign In Successful")
            delivery_func(x[0])
    if f==1:
        print("Invalid Credentials")
        main_menu()

def delivery_func(id):
    print()
    b=0
    while b!=3:
        print()
        print("1) View Orders to deliver")
        print("2) Update Order Status")
        print("3) Exit")
        print()
        b=int(input("Enter your choice:: "))
        
        if b==1:
            cur=db.cursor(buffered=True)
            q="select count(Order_ID) from order_delivery where Delivery_Partner_ID= %s "
            cur.execute(q,[id])
            for x in cur:
                if x[0]==0:
                    print("You do not have any orders to deliver")
                else:
                    cur1=db.cursor(buffered=True)
                    q="select Order_ID,Customer_ID, Customer_Name,Customer_Address from order_delivery where Delivery_Partner_ID= %s "
                    cur1.execute(q,[id])
                    print("Order_ID",'\t',"Customer_ID",'\t',"Customer Name",'\t',"Customer Address")
                    for x in cur1:
                        print(x[0],'\t\t',x[1],'\t\t',x[2],'\t\t',x[3])
                    print()
                        
        elif b==2:
            print()
            order_id=str(input("Enter Order ID :: "))
            cur2=db.cursor(buffered=True)
            cur2.execute("select * from orders")
            flag=0
            for x in cur2:
                if x[0]==order_id:
                    flag=1
            if flag==1:
                status=str(input("Enter status (Packed / Out for delivery / Order Delivered) :: "))
                cur3=db.cursor(buffered=True)
                query="update orders set Order_Status= %s where Order_ID= %s"
                cur3.execute(query,[status,order_id])
                db.commit()
                if status=="Order Delivered":
                    cur1=db.cursor(buffered=True)
                    q="delete from order_delivery where Order_ID=%s"
                    cur1.execute(q,[order_id])
                    db.commit()
                    cur4=db.cursor(buffered=True)
                    q="update delivery_partners set Orders_Delivered=Orders_Delivered+1 where Delivery_Partner_ID = %s"
                    cur4.execute(q,[order_id])
                    db.commit()
                    cur5=db.cursor(buffered=True)
                    q=" update delivery_partners set Orders_Left=Orders_Left-1 where Delivery_Partner_ID = %s"
                    cur5.execute(q,[order_id])
                    db.commit()
            else:
                print()
                print("No such Order")
                delivery_func(id)
                
        elif b==3:
            main_menu()
            
        else:
            print("Invalid Input")

def seller():
    print()
    print("--Login--")
    ids=str(input("Enter ID ::")) 
    passwd=str(input("Enter Phone Number ::"))
    cursor=db.cursor(buffered=True)
    cursor.execute("select * from sellers")
    f=1
    for x in cursor:
        if x[0]==ids and x[4]==passwd:
            f=0
            print()
            print("Sign In Successful")
            seller_func(x[0],x[2],x[8])
    if f==1:
        print()
        print("Invalid Credentials")
        print()
        main_menu()

def seller_func(id,name,cat_id):
    print()
    print("Welcome ",name)
    n=0
    while(n!=4):
        print()
        print("1) Add new product")
        print("2) Delete existing product")
        print("3) Update existing product")
        print("4) LogOut")
        print()
        n=int(input("Enter your choice :: "))
        if(n==1):
            pname=str(input("Enter product name :: "))
            price=int(input("Enter product price :: "))
            quan=int(input("Enter product quantity :: "))
            cursor=db.cursor(buffered=True)
            cursor.execute("select Product_ID from products order by Product_ID desc LIMIT 1")
            strg=""
            for x in cursor:
                strg=x[0]
            s2=int(strg[2:])
            s2+=1
            s=str(strg[:2])+str(s2)
            cat_name=""
            if(cat_id=="CT001"):
                cat_name="Daily Use"
            elif(cat_id=="CT002"):
                cat_name="Clothes"
            elif(cat_id=="CT003"):
                cat_name="Electronics"
            elif(cat_id=="CT004"):
                cat_name="Cosmetics"
            cur1=db.cursor(buffered=True)
            q="Insert into products values (%s,%s,%s,%s,%s,%s)"
            t=(s,pname,price,quan,cat_id,cat_name)
            cur1.execute(q,t)
            db.commit()
            print("Product added succesfully")
            
        elif(n==2):
            cursor=db.cursor(buffered=True)
            q="select Product_ID, Product_Name, Price ,Quantity from products where Category_ID=%s"
            cursor.execute(q,[cat_id])
            print()
            i=1
            print("S.No",'\t',"Product_ID",'\t',"Name",'\t\t'," Price","\t","Stock")
            for x in cursor:
                print(i,")",'\t',x[0],'\t\t',x[1]," " * (20 - len(x[0]) - len(x[1])),x[2]," " * (10 - len(str(x[2]))),x[3])
                i=i+1
            print()         
                
            pid=str(input("Enter the product id you wish to delete :: "))
            cur1=db.cursor(buffered=True)
            q="Delete from products where Product_ID=%s"
            cur1.execute(q,[pid])
            db.commit()
            cur2=db.cursor(buffered=True)
            q="Delete from cart_items where Product_ID=%s"
            cur2.execute(q,[pid])
            db.commit()
            print("Product deleted succesfully")
            
        elif(n==3):
            cursor=db.cursor(buffered=True)
            q="select Product_ID, Product_Name, Price ,Quantity from products where Category_ID=%s"
            cursor.execute(q,[cat_id])
            print()
            i=1
            print("S.No",'\t',"Product_ID",'\t',"Name",'\t\t'," Price","\t","Stock")
            for x in cursor:
                print(i,")",'\t',x[0],'\t\t',x[1]," " * (20 - len(x[0]) - len(x[1])),x[2]," " * (10 - len(str(x[2]))),x[3])
                i=i+1
            print()         
                
            pid=str(input("Enter the product id you wish to update :: "))            
            print("1) Update price ")
            print("2) Update quantity")
            m=int(input("Enter the option :: "))
            if(m==1):
                price=int(input("Enter new price :: "))
                cur2=db.cursor(buffered=True)
                q="Update products set Price=%s where Product_ID=%s"
                t=(price,pid)
                cur2.execute(q,t)
                db.commit()
                cur3=db.cursor(buffered=True)
                q="Update cart_items set Amount=Quantity*%s where Product_ID=%s"
                t=(price,pid)
                cur3.execute(q,t)
                db.commit()                
                print("Price updated succesfully")
            elif(m==2):
                price=int(input("Enter new quantity :: "))
                cur2=db.cursor(buffered=True)
                q="Update products set Quantity=%s where Product_ID=%s"
                t=(price,pid)
                cur2.execute(q,t)
                db.commit()
                print("Quantity updated succesfully")
            else:
                print("Invalid Option")
        
        elif(n==4):
            print()
            print("LogOut Successful")
            main_menu()
        
        else:
            print("Invalid Option")           
                              
def manager():
    print()
    print("--Login--")
    ids=str(input("Enter ID ::")) 
    passwd=str(input("Enter Phone Number ::"))
    cursor=db.cursor(buffered=True)
    cursor.execute("select * from managers")
    f=1
    for x in cursor:
        if x[0]==ids and x[5]==passwd:
            f=0
            print()
            print("Sign In Successful")
            manager_func(x[0],x[2]+" "+x[3])
    if f==1:
        print()
        print("Invalid Credentials")
        print()
        main_menu()
        
def manager_func(id,name):
    print("Welcome ",name)
    h=0
    while h!=6:
        print()
        print("1) View Customers List")
        print("2) View Sellers List")
        print("3) View Delivery Partners List")
        print("4) View Complaints and Feedback")
        print("5) LogOut and Go Back")
        print()
        h=int(input("Enter Your Choice :: "))
        if h==1:
            cur=db.cursor(buffered=True)
            cur.execute("select Customer_ID, First_Name, Last_Name from customers")
            print("Customer_ID",'\t',"Name")
            for x in cur:
                print(x[0],'\t\t',x[1]+" "+x[2])
        elif h==2:
            cur=db.cursor(buffered=True)
            q=" select Seller_ID, Name, Email_ID, Phone_Number from sellers where Manager_ID= %s"
            cur.execute(q,[id])
            print("Seller ID",'\t\t',"Seller Name",'\t\t',"   Email ID",'\t\t\t\t',"    Phone Number")
            for x in cur:
                print(x[0]," "*(23-len(x[0])),x[1]," "*(30-len(x[0])-len(x[1])),x[2]," "*(40-len(x[2])),x[3])
            print()
        elif h==3:
            cur=db.cursor(buffered=True)
            q="select Delivery_Partner_ID, First_Name, Last_Name, Email_ID, Phone_Number from delivery_partners where Manager_ID = %s"
            cur.execute(q,[id])
            print("Delivery Partner ID",'\t',"Delivery Partner Name",'\t\t',"Email ID",'\t\t\t\t',"Phone Number")
            for x in cur:
                print(x[0]," "*(25-len(x[0])),x[1],x[2],'\t\t',x[3]," "*(40-len(x[3])),x[4])
            print()
        elif h==4:
            cur=db.cursor(buffered=True)    
            cur.execute("select * from complaints_and_feedback")
            print("Customer_ID",'\t',"Order_ID",'\t',"FeedBack")
            for x in cur:
                print(x[0]," "*(15-len(x[0])),x[1]," "*(15-len(x[1])),x[2])     
        elif h==5:
            main_menu()
        else:
            print("Invalid Option")
                            
def admin():
    print()
    print("--Login--")
    uname=str(input("Enter User name ::"))
    passwd=str(input("Enter password ::"))
    cursor=db.cursor(buffered=True)
    cursor.execute("select * from admin")
    f=1
    for x in cursor:
        if x[1]==uname and x[2]==passwd:
            f=0
            print("Sign In Successful")
            print()
            admin_func(x[0],x[3]+" "+x[4])
    if f==1:
        print()
        print("Invalid Credentials")
        print()
        main_menu()
        
def admin_func(id,name):
    print("Welcome ",name)
    h=0
    while h!=3:
        print()
        print("1) View Managers List")
        print("2) Appoint New Manager")
        print("3) LogOut and Go Back")
        print()
        h=int(input("Enter your choice:: "))
        if h==1:
            cur=db.cursor(buffered=True)
            q="select Manager_ID,First_Name,Last_Name,Email_ID,Phone_Number from managers where Admin_ID=%s"
            cur.execute(q,[id])
            print("Manager ID",'\t',"Manager Name",'\t\t',"Email ID",'\t\t\t\t  ',"Contact")
            for x in cur:
                print(x[0],'\t\t',x[1],x[2]," "*(20-len(x[1])-len(x[2])),x[3]," "*(40-len(x[3])),x[4])
        elif h==2:
            print()
            fname=str(input("Enter first name ::"))
            lname=str(input("Enter last name ::"))
            email=str(input("Enter email ::"))
            phno=int(input("Enter phone number ::"))
            gender=str(input("Enter your gender ::"))
            age=int(input("Enter Age ::"))
            hno=str(input("Enter Address ::"))
            cursor=db.cursor(buffered=True)
            cursor.execute("select Manager_ID from managers order by Manager_ID desc LIMIT 1")
            strg=""
            for x in cursor:
                strg=x[0]
            s2=int(strg[1:])
            s2+=1
            if(s2<1000):
                s=strg[0]+"00"+str(s2)
            else:
                s=strg[0]+str(s2)
                
            cursor1=db.cursor(buffered=True)
            cursor1.execute("SAVEPOINT add_manager")
            query='insert into managers values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            t=(s,id,fname,lname,email,phno,hno,gender,age,0,0,0)
            cursor1.execute(query,t)
            
            check_phno_query = 'SELECT COUNT(*) FROM managers WHERE Phone_Number = %s'
            cursor1.execute(check_phno_query,[phno])
            num_managers_with_phno = cursor1.fetchone()[0]
            
            if num_managers_with_phno > 1:
                print()
                print("Phone Number already registered")
                print("Cannot appoint with this Phone Number")
                # roll back to the savepoint and discard the changes since then
                cursor1.execute("ROLLBACK TO add_manager")
                cursor1.execute("RELEASE SAVEPOINT add_manager")
            else:
                # commit the transaction
                cursor1.execute("COMMIT")
                print()
                print("Manager added successfully")
        elif h==3:
            print()
            print("LogOut Successful")
            main_menu()
        else:
            print()
            print("Invalid Option")
            print() 
        
main_menu()
db.close()
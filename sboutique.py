import mysql.connector as sql

mydb=sql.connect(
    host='localhost',
    user='root',
    password='moorthy88',
    database='sboutique'
)
mycur=mydb.cursor()

def space():
    for i in range(1):
        print()

def check():
    query=('select cust_id from customer ')
    mycur.execute(query)
    d=mycur.fetchall()
    list_of_ids=[]
    for ids in d:
        list_of_ids.append(ids[0])
    return list_of_ids

def cus_ac():
    ask='Y'
    list_of_ids=check()
    while ask in 'yY':
        custid=int(input("Enter your Customer Id : "))
        if custid in list_of_ids:
            print("This Customer Id already exists... Try creating a new one")
        else:
            c_det=()
            cnam=input("First Name : ")
            clnam=input("Last Name : ")
            cphno=input("Phone Number : ")
            cadrs=input("Address : ")
            c_det=(custid, cnam,clnam,cphno,cadrs)
            query='insert into customer values(%s,%s,%s,%s,%s,NULL)'
            val=c_det
            mycur.execute(query,val)
            mydb.commit()
            print("Customer details entered successfully")
            ask=input("Do you want to continue(Y/N) : ")
            if ask not in ("Yy"):
                space()
                break

def get_bkd_pro(cust_id):
     query='select bkd_pro from customer where cust_id=%s'
     mycur.execute(query,(cust_id,))
     bp=mycur.fetchone()
     bkd_pro=bp[0]
     return bkd_pro

def sign_in():
    try:
        ask=int(input("Enter customer Id to sign in : "))
        list_of_ids=check()
        if ask in list_of_ids:
            while True:
                print(''' Do you want to : 
                1) View Bookings
                2) Book a product
                3) Update Self Details
                4) Cancel booked products
                Enter 'back' to Exit''')
                ccc=input("Enter Choice : ")
                if ccc=='1':
                    s=get_bkd_pro(ask)
                    if s is None or s== ' ':
                        print('you have not booked')
                    else:
                        d=s.split('_')
                        print("Booked products")
                        for bkditems in d:
                            print(bkditems)
                if ccc=='2':
                    query='select pro_id from products'
                    mycur.execute(query)
                    pro_list=mycur.fetchall()
                    list_of_products=[]
                    for i in pro_list:
                        list_of_products.append(i[0])
                    pro_id=input("Enter the product id to book products : ")
                    if pro_id in list_of_products:
                        query='select bkd_pro from customer where cust_id=%s'
                        mycur.execute(query,(ask,))
                        pr=mycur.fetchone()
                        prl=pr[0]
                        if prl is None or prl== ' ':
                            query='update customer set bkd_pro=%s where cust_id=%s'
                            val=(pro_id+'_',ask)
                            mycur.execute(query,val)
                            mydb.commit()
                            print("Your product is booked!")
                        else:
                            prl1=prl+pro_id
                            query2='update customer set bkd_pro=%s where cust_id=%s'
                            val2=(prl1+'_',ask)
                            mycur.execute(query2,val2)
                            mydb.commit()
                            print("Your product is booked!")
                    else:
                        print("This product does not exits. Please write the correct product id!")

                if ccc=='3':
                    query='select cust_id,c_name,c_lname,c_phno,c_adrs from customer where cust_id=%s'
                    mycur.execute(query,(ask,))
                    clist=mycur.fetchone()
                    flds=['Name','Last Name', 'Ph.No','Address']
                    dic={}
                    print("Your existing record is : ")
                    for i in range(4):
                        dic[flds[i]]=clist[i+1]
                        print(i+1,'  ',flds[i],' : ',clist[i+1])
                    for i in range(len(clist)):
                        updtc=int(input("Enter choice to update"))
                        upval=input("Enter"+flds[updtc-1]+'  ')
                        dic[flds[updtc-1]]=upval
                        yn=input("Do You want to update other details? y or n")
                        if yn in 'Nn':
                            break
                    query='update customer set c_name=%s,c_lname=%s,c_phno=%s,c_adrs=%s where cust_id=%s'
                    updt1=tuple(dic.values())+(ask,)
                    val=(updt1)
                    mycur.execute(query,val)
                    mydb.commit()
                    print("Your details are updated")
                if ccc=='4':
                    try:
                        bkd_pro = get_bkd_pro(ask)
                        print('Your Bookings : \n ', bkd_pro)
                        if bkd_pro is None or bkd_pro==' ':
                            print("you have no bookings to cancel")
                        else:
                            cw=input("To cancel all products; enter A \n or enter the product code to cancel: ")
                            if cw in 'Aa':
                                query='update customer set bkd_pro=NULL where cust_id=%s'
                                mycur.execute(query,(ask,))
                                mydb.commit()
                                print("All bookings deleted")
                            elif cw in bkd_pro:
                                x=(bkd_pro[0:-1]).split('_')
                                x.remove(cw)
                                updt_pro=''
                                for item in x:
                                    updt_pro=updt_pro+item+'_'
                                query='update customer set bkd_pro=%s where cust_id=%s'
                                val=(updt_pro,ask)
                                mycur.execute(query,val)
                                mydb.commit()
                                print("Booking Cancelled !")
                    except Exception:
                        print("Some problem in updating details. Try again")
                if ccc.lower()=='back':
                    print("Successfully Logged Out")
                    space()
                    break
        else:
            print("Tis Account does not exits. ")
    except Exception:
        print("Some error occurred. Try Again")

def view_pro():
    query='select * from products'
    mycur.execute(query)
    d=mycur.fetchall()
    dic={}
    for i in d:
        dic[i[0]]=i[1:]
    print('_'*80)
    print("{:<17} {:<22} {:<23} {:<19}".format('Product id','Product name','Price','Stock'))
    print("_"*80)
    for k,v in dic.items():
        a,b,c=v
        print("{:<17} {:<22} {:<23} {:<19}".format(k,a,b,c))
    print('_'*80)

def addpro():
    view_pro()
    n=int(input("Enter no of items to insert : "))
    for j in range(n):
        t=()
        pronum=input("Product No : ")
        proid=input("Product ID : ")
        pprice=int(input("Price : "))
        pstk=int(input("Stock : "))
        t=(pronum,proid,pprice,pstk)
        query='insert into products values(%s,%s,%s,%s)'
        val=t
        mycur.execute(query,val)
        mydb.commit()
        print("Product Added")

def delpro():
    view_pro()
    delt=input("Enter ID of product to be deleted : ")
    query='delete from products where pro_id=%s'
    mycur.execute(query,(delt,))
    mydb.commit()
    print("Product is deleted")

def emp_sign_in():
    try:
        ask=input("Enter id to sign in to the account : ")
        query='select emp_id from employee'
        mycur.execute(query)
        d=mycur.fetchall()
        lis=[]
        for i in d:
            lis.append(i[0])
        if ask not in lis:
            print("Enter the correct id")
        else:
            while True:
                space()
                ccc=input("1. Update delivered records\n 2. Add a New Product \n 3.Delete a product \nEnter 'Back' to logout :  ")
                if ccc=='1':
                    cust_id=input("Enter customer id : ")
                    bkd_pro=get_bkd_pro(cust_id)
                    if bkd_pro is None or bkd_pro==" ":
                        print("This customer has no bookings")
                    else:
                        print("All bookings : ")
                        pro_id=input("Enter product code to remove the delivered product : ")
                        if pro_id in bkd_pro:
                            x=(bkd_pro[0:-1]).split('_')
                            x.remove(pro_id)
                            updt_pro=''
                            for i in x:
                                updt_pro=updt_pro+i+'_'
                            query='update customer set bkd_pro=%s where cust_id=%s'
                            val=(updt_pro,cust_id)
                            mycur.execute(query,val)
                            mydb.commit()
                            print("Delivered product is removed from the database.")
                        else:
                            print("Enter the correct code")
                elif ccc=='2':
                    addpro()
                elif ccc=='3':
                    delpro()
                elif ccc.lower()=='back':
                    print("Successfully logged out")
                    break
    except Exception:
        print("Give the correct input")

def addemp():
    query='select * from employee'
    mycur.execute(query)
    emp_list=mycur.fetchall()
    print("List of Employees")
    for emp in emp_list:
        print("Emp Id :",emp[0],"Name : ",emp[1],"Last Name : ",emp[2],"Phone No : ",emp[3])
    ne=[]
    n=int(input("Enter the no of employees to add : "))
    for i in range(1,n+1):
        t=()
        print("Enter employee id : ")
        idd=int(input(str(i)+')  '))
        print("Name : ")
        nam=input(str(i)+')  ')
        print("Last Name : ")
        lnam = input(str(i) + ')  ')
        print("Contact NO : ")
        conno = int(input(str(i) + ')  '))
        print("Address : ")
        adrs = input(str(i) + ')  ')
        t=(idd,nam,lnam,conno,adrs)
        ne=ne+[t,]
    query='insert into employee values(%s,%s,%s,%s,%s)'
    for i in range(len(ne)):
        val=ne[i]
        mycur.execute(query,val)
        mydb.commit()
    print("All Employee details added. ")
    space()

def employer():
    while True:
        print()
        print('''Enter Your Choice:
        1) View Product Details
        2) Add a New Employee
           Enter back to exit''')
        ccc=input("Enter____ : ")
        if ccc=='1':
            view_pro()
        if ccc=='2':
            addemp()
        if ccc.lower()=='back':
            break

print("Welcome !")
while True:
    print('''Are you a :
    (A). Customer
    (B). Employee
    (C). Employer
    Enter e to Exit''')
    ch=input("Enter :")
    try:
        if ch in 'aA':
            print("1. Create Account\n2. Sign In into existing account")
            choice=input("Enter : ")
            if choice=='1':
                cus_ac()
            elif choice=='2':
                sign_in()
            else:
                print("Enter correct choice")
        if ch in 'bB':
            emp_sign_in()
        if ch in 'cC':
            employer()
        elif ch.lower()=='e':
            print("ThankYou for visiting !")
            break
    except Exception:
        print('Give the right input')
    space()







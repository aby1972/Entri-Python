import sqlite3
import datetime
from time import strftime
from tkinter.constants import INSERT

#import pwinput

conn=sqlite3.connect('Library.db')
cur=conn.cursor()
cur.execute("PRAGMA foreign_keys=ON")
dt=datetime.datetime.now()
tdt=strftime('%d-%m-%Y')


def pas():
    while True:
        p1 = input('Enter the password  : ')
        p2 = input('Confirm password  : ')
        if p1 == p2:
            p = p1
            return p
        else:
            print('The passwords do not match')


#--------Start of Function Add User----------------
def adduser():
    while True:
        n = input('Enter the username : ')
        cur.execute(""" Select * from user where name=?""", (n,));
        if cur.fetchone() == None:
            break
        else:
            print('User name already exists')
    pa=pas()
    fn = input('Enter the First Name  : ')
    ln = input('Enter the Last Name  : ')
    em=input('Enter the Email  : ')
    ph=input('Enter the Phone  : ')
    cur.execute("SELECT * from user")
    if cur.fetchone() == None:
        tp='Admin'
    else:
        tp='User'
    sp=input('Enter the subscription amount paid : ')
    if sp !=0:
        st='Paid'
        stat='Active'
    cur.execute("""
    INSERT INTO user (name,password,fname,lname,email,phone,type,sub_paid,Status) values (?,?,?,?,?,?,?,?,?);
    """, (n, pa, fn, ln,em,ph,tp,st,stat))
    conn.commit()
    print(f'User {n} has been successfully Created')


    if sp!=0:
        cur.execute("""SELECT * FROM user WHERE name=?""", (n,))
        uid = cur.fetchone()
        ud = uid[0]
        if uid != None:
            cur.execute("""
            INSERT INTO subscription (user_id,amt_paid,dop) values (?,?,?);
            """, (ud,sp,tdt))
            conn.commit()
# -----end of Add account---------

#--------Start of Function User Management ----------------
def usr_mgmt():
    n = input('Enter the username : ')
    cur.execute(""" Select * from user where name=?""", (n,));
    udet = cur.fetchone()

    if udet == None:
        print('User name does not exist')
        return
    else:
#        udet = cur.fetchone()
        uid=udet[0]
        print('1. Change Password')
        print('2. Change User Access')
        print('3. Accept Subscription Payment')
        print('4. Cancel Subscription')
        print('5. Exit to Main Menu')
        ch = input('Enter your choice : ')
        if ch == '1':
            pa=pas()
            cur.execute("UPDATE user SET password=? WHERE name=?", (pa,n))
            conn.commit()
        elif ch == '2':
            print('Change User Access')
            print('1. Admin Access')
            print('2. User Access')
            print('3. Exit to Main Menu')
            subch = input('Enter your choice : ')
            if subch == '1':
                cur.execute("UPDATE user SET type=? WHERE id=?", ('Admin',uid))
                conn.commit()
                return
            elif subch == '2':
                cur.execute("UPDATE user SET type=? WHERE id=?", ('User',uid))
                conn.commit()
                return
            else:
                print('Invalid choice')
                return
        elif ch == '3':
            amt=int(input('Enter amount to be paid : '))
            if amt > 0:
                cur.execute("UPDATE user SET sub_paid=? WHERE id=?", ('Paid',uid))
                cur.execute("""
                            INSERT INTO subscription (user_id,amt_paid,dop) values (?,?,?);
                            """, (uid, amt, tdt))
                conn.commit()
                return
            else:
                print('Invalid amount')
                return
        elif ch == '4':
            cs=input('Do you want to Cancel Subscription (y/n) : ')
            if cs == 'y':
                rq=input('Are you sure? (y/n) : ')
                if rq=='y':
                    cur.execute("UPDATE user set Status='DISABLED' where id=?",(uid,))
                    conn.commit()
                    return
                else:
                    return
            else:
                return
        else:
            return

#--------End of Function User Management ----------------


#------Start of Issue Book Function------------
def issue_book():
    un=input('Enter Member Name  : ')
    cur.execute("SELECT * FROM user where name=?",(un,))
    udet=cur.fetchone()
    if  udet == None:
        print('Member not found')
        return
    else:
        uid=udet[0]
    while True:
        bn = input('Enter book name : ')
        cur.execute("SELECT * FROM book where booktitle=?", (bn,))
        tes=cur.fetchone()
        if tes == None:
            print('Book not found')
            return
        else:
#            print("cur.fetchone() != None-Success")
            bketail = cur.fetchone()
            bkid = tes[0]
            cp=tes[7]
            cur.execute("""SELECT * FROM bk_trans where bookid=? and userid=? and return_date IS NULL""", (bkid, uid))
            vtrans = cur.fetchone()
#            print(vtrans)
#        chdt=vtrans[4]
            if vtrans == None:
                j=0
                cur.execute("""SELECT * FROM bk_trans where bookid=?""",(bkid,))
                mat=cur.fetchall()
                for i in mat:
                    if i[4] == None:
                        j+=j
                if cp >= j:
                    print('Book avilable')
                    cur.execute("""
                    INSERT INTO bk_trans (bookid,userid,issue_date) values (?,?,?);
                    """, (bkid,uid,tdt))
                    cur.execute("UPDATE book set copies = copies-1 WHERE bookid=?",(bkid,))
                    conn.commit()
                    print(f'Book {bn} has been successfully Issued to {un}')
                    break
                else:
                    print('Book not available')
                    break
            else:
                print('Book is with the same user. Please return it ASAP')
                break
        # else:
        #     print("Book is with the same user.Please return it ASAP")
        #     return

#---------End of Issue Book Function-------------

# Start of Add Book Function-----------
def addbook():
    while True:
        n = input('Enter the book title  : ')
        cur.execute("SELECT * FROM book where booktitle=?", (n,))
        bketail = cur.fetchone()
        if  bketail== None:
            atn=input('Enter Author Name : ')
            pbn = input('Enter Publisher Name : ')
            ln=input('Enter Language : ')
            pg=input('Enter total pages : ')
            ISBN=input('Enter ISBN Number : ')
            cp=input('Enter no of copies : ')
            cur.execute("""INSERT INTO book  (booktitle,authorname,publishername,langauge,pages,ISBN,copies)
             values(?,?,?,?,?,?,?);""", (n,atn,pbn,ln,pg,ISBN,cp))
            conn.commit()
            print(f"Book {n} has been successfully added to library")
            break
        else:
            q=input('Book exists in list! Do you want to update number of copies? (y/n) : ')
            bid=bketail[0]
            if q=='y':
                cp1=int(input('Enter the copies number : '))
                cur.execute("UPDATE book set copies = copies+? WHERE bookid=?", (cp1,bid))
                conn.commit()
                print(f"Book {n} has been successfully updated")
                break
            else:
                break
#---------End of Add book function------------

# Start of Remove Book from Library Function-----------
def rem_book():
    n = input('Enter the book title  : ')
    cur.execute("SELECT * FROM book where booktitle=?", (n,))
    bketail = cur.fetchone()
    if bketail == None:
        print('Book not found')
        return
    else:
        cp=bketail[6]

        y=input('Do you want to remove all copies ? (y/n) : ')
        if y == 'y':
            cur.execute("DELETE FROM book WHERE bookid=?",(bketail[0],))
            conn.commit()
            print(f"Book {n} has been successfully removed")
            return


        else:
            print('You have ',cp,' in stock.')
            s = int(input('Please enter the number of copies to be deleted : '))
            if s>cp:
                print('Entered number is higher than copies exists')
                return
            else:
                cp=cp-s
                if cp >=0:
                    cur.execute("UPDATE book set copies=? WHERE bookid=?", (cp,bketail[0]))
                    conn.commit()
                    print(f"Book {n} has been successfully updated")
                return
#---------End of Remove a book  function------------



#-------Start of Return Book Function-----------
def return_book():
    n = input('Enter Member Name  : ')
    cur.execute("SELECT * FROM user where name=?", (n,))
    tes=cur.fetchone()
    if tes == None:
        print('Member not found')
        return
    else:
#        udet = cur.fetchone()
        uid = tes[0]
        bn = input('Enter book name : ')
        cur.execute("SELECT * FROM book where booktitle=?", (bn,))
        bkdetail = cur.fetchone()
        if bkdetail == None:
            print('Book not found')
            return
        else:
            bkid = bkdetail[0]
            cp = bkdetail[6]
            print('Book ID = ',bkid," User ID = ",uid)
            cur.execute("SELECT * FROM bk_trans where bookid=? and userid=? and return_date IS NULL", (bkid,uid))
            btetail = cur.fetchone()
            if btetail == None:
                print('Transaction not found')
                return
            else:
                btid = btetail[0]
                cur.execute("UPDATE bk_trans set return_date = ? WHERE transid=?", (tdt, btid))
                cur.execute("UPDATE book set copies = copies + 1 WHERE bookid=?", (bkid,))
                print(f"User {n} has returned the book {bn} successfully")
                conn.commit()

#--------End of Return Book Function

#--------Start of Reports Function-----------
def reports():
    print('1. User Report')
    print('2. Book Report')
    print('3. Transaction Report')
    print('4. Exit')
    choice = input('Enter your choice : ')
    if choice == '1':
        print('1. Active User Report')
        print('2. Disabled User Report')
        print('3. Subscription Defaulter Report')
        print('4. Books Taken by the user')
        print('5. Exit to Previous Menu')
        ch=input('Enter your choice : ')
        if ch == '1':
            cur.execute("SELECT name as Username,fname as FirstName,lname as LastName, Status as Status, sub_paid as Sub_Status FROM user where Status='Active'")
            print('Active User Report')
            print("UserName\tFirstName\tLastName\tStatus\tSubscrption_Status")
            for i in cur.fetchall():
               print(i)
            return
        elif ch == '2':
            cur.execute(
                "SELECT name as Username,fname as FirstName,lname as LastName, Status as Status, sub_paid as Sub_Status FROM user where Status='Disabled'")
            print('Disabled User Report')
            print("UserName\tFirstName\tLastName\tStatus\tSubscrption_Status")
            for i in cur.fetchall():
                print(i)
            return
        elif ch == '3':
            cur.execute(
                "SELECT name as Username,fname as FirstName,lname as LastName, Status as Status, sub_paid as Sub_Status FROM user where Sub_paid='Not Paid'")
            print('Users Not pay the Subscription Report')
            print("UserName\tFirstName\tLastName\tStatus\tSubscrption_Status")
            for i in cur.fetchall():
                print(i)
            return
        elif ch == '4':
            uid=input('Enter User Name : ')
            cur.execute("""
            SELECT u.name,b.booktitle,t.issue_date,
 	        t.return_date FROM bk_trans t JOIN book b ON t.bookid = b.bookid
            JOIN user u ON t.userid = u.id
            WHERE u.name =?""",(uid,))
            print('Book Taken by a User Report')
            print("UserName\tBook Name\tDate Issued\tDate Returned")
            for i in cur.fetchall():
                print(i)
            return
        else:
            print('Invalid choice')
            return
    elif choice == '2':
        print('1. Book Reports')
        print('2. Book by Author')
        print('3. Book by Publisher')
        print('4. Book by Language')
        print('5. Books Available')
        print('6. Exit to Previous Menu')
        ch1=input('Enter your choice : ')
        if ch1 == '1':
            print('1. Books by Author')
            return
        elif ch1 == '2':
            print('2. Books by Publisher')
            return
        elif ch1 == '3':
            print('3. Books by Language')
            return
        elif ch1 == '4':
            print('4. Books Available')
        else:
            print('Exit to main Menu')
            return
    elif choice == '3':
        print('1. Total subscription per month')
        print('2. Total subscription per year')
        print('3. Total subscription per User')
        print('4. Exit to Previous Menu')
        ch2=input('Enter your choice : ')
        if ch2 == '1':
            print('1. Total subscription per month')
            return
        elif ch2 == '2':
            print('2. Total subscription per year')
            return
        elif ch2 == '3':
            print('3. Total subscription per User')
            return
        else:
            print('Exit to main Menu')
            return
    else:
        return

def lmslogin():
    global n
    print('Welcome to LMS Login Page')
    n=input('Please enter your User Name : ')
    p=input('Please enter your Password : ')
    cur.execute("SELECT * FROM user WHERE name=? and password=? and Status='Active'", (n,p))
    if cur.fetchone() == None:
#        print('User Not Exists!')
        return False
    else:
#        print('User Exists!')
        return True

#-------Check Availability of Book-----------
def checkbookAvail():
    bname=input('Please enter the Book Name you need to check : ')
    cur.execute("""
                SELECT booktitle,authorname,pages,copies from
     	        book WHERE booktitle =?""", (bname,))
    sed=cur.fetchone()
    if sed == None:
        print('Book Not Found')
        return
    else:
        if sed[3]>0:
            print(f"{sed[3]} copies of {sed[0]} avalaible.")
            return
        else:
            print('Book Not Available in Library')
            return
#-------End of Check Availability of Book-----------

#---------Write a Review------------
def reviewbk(uid):
    print('Please write your review')
    bn=input('Enter the book name to review : ')
    cur.execute("""SELECT bookid from book WHERE booktitle=?""", (bn,))
    sed=cur.fetchone()
    if sed == None:
        print('Book Not Found')
        return
    else:
        rev=input('Enter the review : ')
        cur.execute("""INSERT INTO review (bookid,userid,reviewtxt,dor) values (?,?,?,?);""",
         (sed[0],n,rev,tdt))
        conn.commit()
        return
#------End of review function

#--------Check Dues Function----------
def checkdues(uid):
    print('User ',uid)
    cur.execute("""SELECT * FROM user WHERE name=? and sub_paid=?""", (uid,'Paid'))
    sed=cur.fetchone()
    if sed == None:
        print('Subscription payment not recieved')
        return
    else:
        print('Subscription payment recieved')
        return
#-----End of Check Dues-----


def MainLMSTrans():
    cur.execute("SELECT * FROM user WHERE name =? and type=?",(n,'Admin'))
    if cur.fetchone() != None:
        while True:
            print('Welcome to Mahathma Library')
            print('1. Issue Book')
            print('2. Return Book')
            print('3. Add Book to library')
            print('4. Remove Book from library')
            print('5. Member Management')
            print('6. Reports')
            print('7. Exit')
            y=input('Select an option to continue  : ')
            if y=='1':
                print('Issue Book')
                issue_book()
            elif y=='2':
                print('Return Book')
                return_book()
            elif y=='3':
                print('Add Book to library')
                addbook()
            elif y=='4':
                print('Delete Book from library')
                rem_book()
            elif y=='5':
                print('Member Management')
                usr_mgmt()
            elif y=='6':
                print('Reports')
                reports()
            else:
                return
    else:
        while True:
            print('Welcome to Mahathma Library')
            print('1. Check Book availability')
            print('2. Review a book')
            print('3. Check Dues')
            print('4. Exit')
            y=input('Select an option to continue  : ')
            if y=='1':
                checkbookAvail()
                return
            elif y=='2':
                reviewbk(n)
                return
            elif y=='3':
                checkdues(n)
                return
            else:
                return




#---------First page------------
#Create the user table
cur.execute("""
CREATE TABLE IF NOT EXISTS user(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT not null,
password TEXT not null,
fname TEXT,
lname TEXT,
email TEXT not null,
phone INTEGER not null,
Type TEXT,
sub_paid TEXT,
Status TEXT);
""")

# Create subcription table
cur.execute("""
CREATE TABLE IF NOT EXISTS subscription(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
amt_paid INTEGER NOT NULL,
dop TEXT NOT NULL,
FOREIGN KEY (user_id) REFERENCES user(id));
""")

#Create the Book table
cur.execute("""
CREATE TABLE IF NOT EXISTS book(
bookid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
booktitle TEXT not null,
authorname TEXT not null,
publishername TEXT not null,
langauge TEXT,
pages INTEGER ,
ISBN TEXT,
copies INTEGER);
""")

#Create Review Table
cur.execute("""
CREATE TABLE IF NOT EXISTS review(
reviewid INTEGER PRIMARY KEY AUTOINCREMENT,
bookid INTEGER not null,
userid INTEGER not null,
reviewtxt TEXT not null,
dor TEXT not null,
FOREIGN KEY(bookid) REFERENCES book(bookid));
""")

#Create table bk_trans
cur.execute("""
CREATE TABLE IF NOT EXISTS bk_trans(
transid INTEGER PRIMARY KEY AUTOINCREMENT not null,
bookid INTEGER not null,
userid INTEGER not null,
issue_date TEXT not null,
return_date TEXT,
FOREIGN KEY(bookid) REFERENCES book(bookid));
""")



while True:
    print(" Library Management System")
    print('1. Login to LMS')
    print('2. New account SignUp')
    print('3. Quit')
    y=input('Select an option to continue  : ')
    if y=='1':
        m=lmslogin()
        if m==False:
            print('User Not Exists!')
            break
        else:
            print('User Exists!')
            MainLMSTrans()
            break
    elif y=='2':
        adduser()
    else:
        break

#----End of First Page-----------




# cur.execute("SELECT * FROM user")
# for i in cur.fetchall():
#     print(i)

# class User:
#     def __init__(self_
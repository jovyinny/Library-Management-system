import sqlite3,time,re
pattern =r"([\w+][(@|%|#|?|&|!|%|©){2,3}])"
#Simple sql library(Books) management system using python....
#Actions that can be performed Create table, add books, borrow, return books
now =time.localtime()
day=now.tm_mday
month=now.tm_mon
year=now.tm_year
hour=now.tm_hour
min=now.tm_min
time_now="on {}/{}/{} at {}:{}". format (day,month,year,hour,min)
  
file="Library.db"
  
 #creating function for creating borrowers table and  borrowing a book...      
def borrow():
    connection=sqlite3.connect(file)
    cursor=connection.cursor()
    
    command="""CREATE TABLE IF NOT EXISTS BORROWER(First_name varchar(50)NOT NULL, Second_name varchar(50) NOT NULL, Book_no_and_name varchar(100) PRIMARY KEY NOT NULL, Passcode varchar(20) NOT NULL, Borrowed date, physical_status varchar(100), Returned date);"""
    cursor.execute(command)
    
    print("Borrower to fill...")
    f_name=input("Enter first name: ")
    s_name=input("Enter second name: ")    
    book_name=input("Enter the name of the book: ").lower()
    book_no=int(input("Enter the book number: "))
    book_no_name=str(book_no)+' '+book_name
    #creating password to be used in returning the book....
    print("\nYou will be required to make your password containing characters from a-z and at least two of these characters,@,#,%,!,&,©,?\n")
    time.sleep(1)
    passcode=input("Enter your passcode: ")
    physical=input("Enter physical status of the book: ")
    returned="Not returned"
    
    #Enter the name of the table where the book belongs....   
    table_name=input("Enter the name of the table where you took the book from: ").upper()
    table_name=table_name.replace(" ","_")
    match=re.search(pattern, passcode)
    if match:
        command="""INSERT INTO BORROWER VALUES ("{}","{}","{}","{}","borrowed {}","{}","{}");""".format(f_name,s_name,book_no_name,passcode,time_now ,physical, returned)
        command1="""UPDATE {} SET status="borrowed" ,Physical_status="{}" WHERE Book_no_and_name="{}" """.format(table_name, physical,book_no_name)
        cursor.execute(command)
        cursor.execute(command1)
        connection.commit()
        connection.close()
    else:
        print("Weak password so you can't borrow.....Try again")

#creating the function for return the book....
def return_book():
    connection=sqlite3.connect(file)
    cursor=connection.cursor()
    print("Borrower to fill....")
    f_name=input("Enter your first name: ")
    s_name=input("Ente your second name: ")
    book_name=input("Enter the name of the book: ").lower()     
    book_no=int(input("Enter the book number: "))    
    book_no_name=str(book_no)+' '+book_name
    physical=input("Enter current book\'s condition: ")
    passcode=input("Enter your passcode: ")
    #Enter name of the table where the book was taken from
    table_name=input("Enter the name of the table where the book is to be returned: ")
    table_name=table_name.upper()
    table_name=table_name.replace(" ","_")
    #sql command to update the particular table
    command="""UPDATE {} SET status="Available", physical_status="{}" WHERE Book_no_and_name= "{}" """.format(table_name, physical,book_no_name)
    #sql command to update  borrower table....
    command1="""UPDATE BORROWER SET Returned="Returned {}" WHERE Book_no_and_name = "{}" AND First_name="{}" AND Second_name="{}" AND Passcode="{}"  """.format(time_now,book_no_name,f_name,s_name, passcode)
    cursor.execute(command)
    cursor.execute(command1)
    connection.commit()
    connection.close()

                
def create_book_table():
    table_name=input("Enter table name: ")
    table_name=table_name.upper()
    table_name=table_name.replace(" ", "_")    
    connection=sqlite3.connect(file)
    cursor=connection.cursor()
    command="""CREATE TABLE {} (Book_no_and_name varchar(100) PRIMARY KEY NOT NULL, Author varchar(100) NOT NULL,  Status varchar(100), physical_status varchar(100), Book_description TEXT);""". format(table_name)
    cursor.execute(command)
    connection.commit()
    connection.close()
        
    
def add_book():
    option=int(input("How many books are you adding: "))
    table_name=input("Enter the  name of the table to add a book: ")
    table_name=table_name.upper()
    table_name=table_name.replace(" ","_")
    for i in range(0, option):
        book_name=input("Enter book name: ").lower()
        book_author=input ("Enter book author: ")    
        book_no=int(input("Enter the book's number:  "))
        book_no_name=str(book_no)+' '+book_name
        book_status=input ("Enter book status(available/not available ): ")
        book_physical=input("Enter book's current physical status: ")
        book_description=input ("Enter other book description: ")
        
        connection=sqlite3.connect(file)
        cursor=connection.cursor()
        command="""INSERT INTO {} VALUES( "{}", "{}", "{}", "{}","{}");""". format(table_name,book_no_name,book_author,book_status,book_physical,book_description)
        cursor.execute(command)
        connection.commit()
        connection.close()
    
#creating function to show all informations   
def show():
    user=input("Enter the table to show: ")
    user=user.upper()
    user=user.replace(" ","_")
    connection=sqlite3.connect(file)
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM {}".format(user))
    ans=cursor.fetchall()
    for i in ans:
        print("\n")
        print(i)
    connection.close()
    
 #showing books that are available in particular table   
def show_available():
    user=input("Enter the table to show: ")
    user=user.upper()
    user=user.replace(" ","_")
    connection=sqlite3.connect(file)
    cursor=connection.cursor()
    cursor.execute("""SELECT Book_no_and_name, Author, physical_status FROM {} WHERE Status="available" OR Status ="Available" """.format(user))
    ans=cursor.fetchall()
    print("AVAILABLE BOOKS ARE:....")
    for i in ans:
        print("\n")
        print(i)
    connection.close()
    
#show book that are borrowed
def show_borrowed():
    user=input("Enter the table to show: ")
    user=user.upper()
    user=user.replace(" ","_")
    connection=sqlite3.connect(file)
    cursor=connection.cursor()
    cursor.execute("""SELECT Book_no_and_name, Author, physical_status FROM {} WHERE Status="Borrowed" OR Status ="borrowed"  """.format(user))
    ans=cursor.fetchall()
    print("BORROWED BOOKS ARE:.....")
    for i in ans:
        print("\n{}".format(i))
    connection.close()

#creating the start function...
def start():
    try:
        print("Enter number: \n[1] - For creating a new book table\n[2] - for adding a book in a table\n[3] - for showing books in particular table\n[4] - For borrowing a book\n[5] - For Returning a book\n[6]- For showing available books in particular table\n[7]- For showing borrowed books from a particular table\n")
        user_option=int(input("Enter operation to be performed: "))
        print("\n")        
        if user_option==1:
            create_book_table()
        elif user_option== 2:
            add_book()
        elif user_option ==3:
            show()
        elif user_option ==4:
            borrow()
        elif user_option== 5:
             return_book()
        elif user_option== 6:
            show_available()
        elif user_option==7:
            show_borrowed()
        else:
            print ("Unknown operation....")
    except ValueError:
        print ("Error occurred")
        
                
user=True  
#creating a while loop that will be ended optionally by the user     
while user:    
    start()
    print("\n")
    option=input("Do you want to perform more actions: ").lower()
    if option=="yes":
        user=True
    else:
        user=False
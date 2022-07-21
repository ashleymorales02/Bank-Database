# Ashley Morales
# Software Project for Bank Database
from tkinter import *
from tkinter import messagebox
from datetime import date
from tkinter import ttk

import mysql.connector

# Establish SQL connection
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Stitch626"
)

# Create Bank database
mycursor = mydb.cursor(buffered=True)
# mycursor.execute("drop database if exists bank")
# mycursor.execute("create database bank")
# mycursor.execute("use bank")

mycursor.execute("SHOW DATABASES like 'bank'")
# don't want to drop the database each time the program ones so all the changes can remain the database
# for example, if we want to log in as another user to see transactions (especially transfer)
if mycursor.rowcount == 0:
    mycursor.execute("create database bank")
    mycursor.execute("use bank")

    # Create all tables
    mycursor.execute(
        "create table BRANCH ("
        "branch_id integer(5), "
        "branch_name varchar(25), "
        "zip varchar(5), "
        "primary key(branch_id));")

    mycursor.execute(
        "create table BRANCH_LOCATION ("
        "zip varchar(5), "
        "street varchar(50), "
        "city varchar(15), "
        "primary key(zip));")

    mycursor.execute(
        "create table ACCOUNTS ("
        "account_no integer(12), "
        "balance numeric(12,2),"
        "date_created date,"
        "branch_id integer(5), "
        "primary key(account_no), "
        "foreign key (branch_id) references BRANCH (branch_id));")

    mycursor.execute(
        "create table CUSTOMERS ("
        "fname varchar(15) NOT NULL, "
        "lname varchar(15) NOT NULL, "
        "Ssn char(9), "
        "address varchar(50), "
        "email varchar(45), "
        "phone varchar(12), "
        "username varchar(45) NOT NULL, "
        "password varchar(12) NOT NULL, "
        "UNIQUE (username), "
        "UNIQUE (password), "
        "primary key(Ssn));")

    mycursor.execute(
        "create table CUST_ACCT ("
        "Ssn char(9), "
        "account_no integer(12), "
        "primary key(Ssn, account_no), "
        "foreign key (Ssn) references CUSTOMERS (Ssn), "
        "foreign key (account_no) references ACCOUNTS (account_no));")

    mycursor.execute(
        "create table TRANSACTIONS ("
        "transaction_id INT, "
        "txn_type varchar(15), "
        "amount numeric(12,2), "
        "date_posted date, "
        "src_acct integer(12), "
        "dest_acct integer(12), "
        "primary key(transaction_id), "
        "UNIQUE (transaction_id), "
        "foreign key (src_acct) references ACCOUNTS (account_no), "
        "foreign key (dest_acct) references ACCOUNTS (account_no));")

    # Insert tuples into tables
    sql1 = "INSERT INTO branch (branch_id, branch_name, zip) VALUES (%s, %s, %s)"
    val1 = [
        ('4590', 'NYB: Bronx', '10471'),
        ('4592', 'NYB: Broadway', '10025'),
        ('4594', 'NYB: Rochester', '13203'),
        ('4596', 'NYB: Buffalo', '14201'),
        ('4598', 'NYB: Albany', '10038')
    ]
    mycursor.executemany(sql1, val1)
    mydb.commit()

    sql2 = "INSERT INTO branch_location (zip, street, city) VALUES (%s, %s, %s)"
    val2 = [
        ('10471', '4513 Manhattan College Pkwy', 'Yonkers'),
        ('10025', '8120 Broadway Ave', 'New York'),
        ('13203', '6792 Columbus Ave', 'Rochester'),
        ('14201', '5983 Gorge Rd', 'Buffalo'),
        ('10038', '2408 Main St', 'Albany')
    ]
    mycursor.executemany(sql2, val2)
    mydb.commit()

    sql4 = "INSERT INTO accounts (account_no, balance, date_created, branch_id) VALUES (%s, %s, %s, %s)"
    val4 = [
        ('1000099', '700000.00', '2022-04-12', '4590'),
        ('6789102', '400000.00', '2022-04-13', '4590'),
        ('1234567', '500000.00', '2022-04-14', '4592'),
        ('1000027', '800000.00', '2022-04-15', '4594'),
        ('0246810', '300000.00', '2022-04-16', '4590'),
        ('1357911', '200000.00', '2022-04-17', '4596')
    ]
    mycursor.executemany(sql4, val4)
    mydb.commit()

    sql3 = "INSERT INTO customers (fname, lname, Ssn, address, email, phone, username, password) VALUES (%s, %s, %s, " \
           "%s, %s, %s, %s, %s) "
    val3 = [
        ('Ashley', 'Morales', '123', '295 College Court Bronx, NY 10456', 'amorales@gmail.com', '800-212-6460',
         'amorales', 'amorales01'),

        ('Giancarlo', 'Stanton', '456', '386 Hillcrest St New York, NY 10040', 'gstanton@gmail.com', '917-646-8000',
         'gstanton', 'gstanton01'),

        ('Aaron', 'Judge', '789', '283 Academy Ave Yonkers, NY 10701', 'gstanton@gmail.com', '347-553-9000', 'ajudge',
         'ajudge01'),

        ('Melanie', 'Row', '654', '393 Greenview Lane, NY 11111', 'mrow@gmail.com', '458-239-4163', 'mrow', 'mrow01'),

        ('Emma', 'Cruz', '321', '52 North Essex St., NY 11532', 'ecruz@gmail.com', '646-199-0000', 'ecruz', 'ecruz01')
    ]
    mycursor.executemany(sql3, val3)
    mydb.commit()

    sql4 = "INSERT INTO cust_acct (Ssn, account_no) VALUES (%s, %s)"
    val4 = [
        ('123', '1234567'),
        ('123', '6789102'),
        ('456', '1000027'),
        ('789', '1000099'),
        ('654', '0246810'),
        ('321', '1357911')
    ]
    mycursor.executemany(sql4, val4)
    mydb.commit()

    sql5 = "INSERT INTO transactions (transaction_id, txn_type, amount, date_posted, src_acct, dest_acct) VALUES " \
           "(%s, %s, %s, %s, %s, %s)"
    val5 = [
        ('1', 'Initial Deposit', '700000.00', '2022-04-12', '1000099', '1000099'),
        ('2', 'Initial Deposit', '400000.00', '2022-04-13', '6789102', '6789102'),
        ('3', 'Initial Deposit', '500000.00', '2022-04-14', '1234567', '1234567'),
        ('4', 'Initial Deposit', '800000.00', '2022-04-15', '1000027', '1000027'),
        ('5', 'Initial Deposit', '300000.00', '2022-04-16', '0246810', '0246810'),
        ('6', 'Initial Deposit', '200000.00', '2022-04-17', '1357911', '1357911')
    ]
    mycursor.executemany(sql5, val5)
    mydb.commit()
else:
    mycursor.execute("use bank")

root = Tk()
root.title("New York Bank")
root.geometry("700x800")
frame1 = Frame(root)
frame2 = Frame(root)
frame3 = Frame(root)
Label(root, text='New York Bank', bd=4, font=('arial', 35, 'bold'), relief="groove", fg="white", bg="blue",
      width=300).pack()
Label(root, text="").pack()


# define some global variables
activeAccounts = set()  # once a user is logged in, hold all their active accounts
user = ""  # keep a global variable of the username
passwd = ""  # keep a global variable of the password to be used in multiple functions
usersname = ""  # keep a global variable of the users name to be used in multiple functions


def CB():
    newWindow = Toplevel(root)
    newWindow.title("Balances")
    newWindow.geometry("500x500")

    Label(newWindow, text='New York Bank', bd=4, font=('arial', 35, 'bold'), relief="groove", fg="white", bg="blue",
          width=300).pack()
    Label(newWindow, text="").pack()

    Label(newWindow, text='Check Balance', fg="black", font=('arial', 20, 'bold', 'underline')).pack()
    Label(newWindow, text="").pack()
    Label(newWindow, text="").pack()

    Label(newWindow, text="Hi {}, here are your active balance(s): \n".format(usersname),
          font=('arial', 16, 'bold')).pack()
    Label(newWindow, text="").pack()

    # create tables of all the users active account and their balances
    t = ttk.Treeview(newWindow, height=5)
    t.pack()

    t['columns'] = ('account#', 'balance')
    t.column("#0", width=0, stretch=NO)
    t.column("account#", anchor=CENTER, width=150)
    t.column("balance", anchor=CENTER, width=200)

    t.heading("#0", text="", anchor=CENTER)
    t.heading("account#", text="Account#", anchor=CENTER)
    t.heading("balance", text="Balance", anchor=CENTER)

    sql8 = "select A.account_no, A.balance " \
           "from CUSTOMERS C, CUST_ACCT CA, ACCOUNTS A " \
           "where C.Ssn = CA.Ssn and CA.account_no = A.account_no and username = %s and password = %s"
    values8 = (user, passwd)
    mycursor.execute(sql8, values8)
    balances = mycursor.fetchall()

    # insert accts and balances into table
    for index, val in enumerate(balances):
        acct, bal = val
        balance = "$" + str(bal)
        t.insert(parent='', index='end', iid=index, text='', values=(acct, balance))


def dep_details(event=None):
    acct = dep_acct.get()
    amount = dep_amount.get()
    flag_amount = FALSE
    date_post = date.today()

    if len(amount) == 0:
        message = "Error. Field cannot be empty."
        messagebox.showinfo('Error', message)
    else:
        try:
            if int(amount) > 0:
                flag_amount = TRUE

            if flag_amount:
                # make deposit
                sql9 = "update ACCOUNTS " \
                       "set balance = balance + %s " \
                       "where account_no = %s"
                values9 = (amount, acct)
                mycursor.execute(sql9, values9)
                mydb.commit()

                # transaction_id counter
                sql10 = "select * from transactions "
                mycursor.execute(sql10)
                T_id = mycursor.rowcount + 1
                sql11 = "INSERT INTO transactions (transaction_id, txn_type, amount, date_posted, src_acct, dest_acct) " \
                        "VALUES (%s, %s, %s, %s, %s, %s)"
                values11 = (T_id, "Deposit", amount, date_post, acct, acct)
                mycursor.execute(sql11, values11)
                mydb.commit()

                message = "You deposited ${} into your account.".format(amount)
                messagebox.showinfo('Deposit Successful', message)
                depWindow.destroy()
            else:
                message = "Error. Make sure you enter a valid amount greater than 0."
                messagebox.showinfo('Error', message)
                dep_amount.set("")
        except:
            messagebox.showinfo('Error', "Invalid amount.")
            dep_amount.set("")


def DEP():
    global dep_acct
    global dep_amount
    global depWindow
    depWindow = Toplevel(root)
    depWindow.title("Deposits")
    depWindow.geometry("450x500")

    dep_acct = IntVar()
    dep_amount = StringVar()

    Label(depWindow, text='New York Bank', bd=4, font=('arial', 35, 'bold'), relief="groove", fg="white", bg="blue",
          width=300).pack()
    Label(depWindow, text="").pack()

    Label(depWindow, text='Make A Deposit', fg="black", font=('arial', 20, 'bold', 'underline')).pack()
    Label(depWindow, text="").pack()
    Label(depWindow, text="").pack()

    Label(depWindow, text="Choose account:", fg="black", font=('arial', 16, 'bold')).pack()
    for index, val in enumerate(activeAccounts):
        Radiobutton(depWindow, text=val, variable=dep_acct, value=val).pack()

    Label(depWindow, text="").pack()
    Label(depWindow, text="Enter Amount:", fg="black", font=('arial', 15, 'bold')).pack()
    Entry(depWindow, textvariable=dep_amount).pack()
    Label(depWindow, text="").pack()

    Button(depWindow, text="Deposit", fg="blue", relief="groove",
           font=('arial', 14, 'bold'), command=dep_details).pack()
    depWindow.bind('<Return>', dep_details)


def with_details(event=None):
    acct = with_acct.get()
    amount = with_amount.get()
    flag_amount = FALSE
    date_post = date.today()

    if len(amount) == 0:
        message = "Error. Field cannot be empty."
        messagebox.showinfo('Error', message)
    else:
        try:
            if int(amount) > 0:
                flag_amount = TRUE

            if flag_amount:
                # make withdrawal
                sql12 = "update ACCOUNTS " \
                        "set balance = balance - %s " \
                        "where account_no = %s"
                values12 = (amount, acct)
                mycursor.execute(sql12, values12)
                mydb.commit()

                # transaction_id counter
                sql10 = "select * from transactions "
                mycursor.execute(sql10)
                T_id = mycursor.rowcount + 1
                # insert into transactions table
                sql13 = "INSERT INTO transactions (transaction_id, txn_type, amount, date_posted, src_acct, dest_acct) " \
                        "VALUES (%s, %s, %s, %s, %s, %s)"
                values13 = (T_id, "Withdrawal", amount, date_post, acct, acct)
                mycursor.execute(sql13, values13)
                mydb.commit()

                message = "You withdrew ${} from your account.".format(amount)
                messagebox.showinfo('Withdrawal Successful', message)
                withWindow.destroy()
            else:
                message = "Error. Make sure you enter a valid amount greater than 0."
                messagebox.showinfo('Error', message)
                with_amount.set("")
        except:
            messagebox.showinfo('Error', "Invalid amount.")
            with_amount.set("")


def WD():
    global with_acct
    global with_amount
    global withWindow
    withWindow = Toplevel(root)
    withWindow.title("Withdraw")
    withWindow.geometry("450x500")

    with_acct = IntVar()
    with_amount = StringVar()

    Label(withWindow, text='New York Bank', bd=4, font=('arial', 35, 'bold'), relief="groove", fg="white", bg="blue",
          width=300).pack()
    Label(withWindow, text="").pack()

    Label(withWindow, text='Make A Withdrawal', fg="black", font=('arial', 20, 'bold', 'underline')).pack()
    Label(withWindow, text="").pack()
    Label(withWindow, text="").pack()

    Label(withWindow, text="Choose account:", fg="black", font=('arial', 16, 'bold')).pack()
    for index, val in enumerate(activeAccounts):
        Radiobutton(withWindow, text=val, variable=with_acct, value=val).pack()

    Label(withWindow, text="").pack()
    Label(withWindow, text="Enter Amount:", fg="black", font=('arial', 15, 'bold')).pack()
    Entry(withWindow, textvariable=with_amount).pack()
    Label(withWindow, text="").pack()

    Button(withWindow, text="Withdraw", fg="blue", relief="groove",
           font=('arial', 14, 'bold'), command=with_details).pack()
    withWindow.bind('<Return>', with_details)


def makeTransfer(event=None):
    otherAccounts = set()
    from_acct = srcAcct.get()
    to_acct = destAcct.get()
    amount = tfs_amount.get()
    flag_amount = FALSE
    date_post = date.today()

    # get other existing accounts not belonging to the user
    sql14 = "select account_no " \
            "from ACCOUNTS where account_no <> %s"
    values14 = (from_acct,)
    mycursor.execute(sql14, values14)
    results = mycursor.fetchall()
    for line in results:
        otherAccounts.add(line[0])

    if len(amount) == 0:
        message = "Error. Field cannot be empty."
        messagebox.showinfo('Error', message)
    else:
        try:
            if int(amount) > 0:
                flag_amount = TRUE

            if int(to_acct) in otherAccounts and flag_amount:
                # withdraw from source acct
                sql15 = "update ACCOUNTS " \
                        "set balance = balance - %s " \
                        "where account_no = %s"
                values15 = (amount, from_acct)
                mycursor.execute(sql15, values15)
                mydb.commit()

                # deposit into destination account
                sql16 = "update ACCOUNTS " \
                        "set balance = balance + %s " \
                        "where account_no = %s"
                values16 = (amount, to_acct)
                mycursor.execute(sql16, values16)
                mydb.commit()

                # transaction_id counter
                sql10 = "select * from transactions "
                mycursor.execute(sql10)
                T_id = mycursor.rowcount + 1

                # insert into transactions table
                sql17 = "INSERT INTO transactions (transaction_id, txn_type, amount, date_posted, src_acct, dest_acct) " \
                        "VALUES (%s, %s, %s, %s, %s, %s)"
                values17 = (T_id, 'Transfer', amount, date_post, int(from_acct), int(to_acct))
                mycursor.execute(sql17, values17)
                mydb.commit()

                message = "Your transfer was successful."
                messagebox.showinfo('Transfer successful.', message)
                tfsWindow.destroy()
            else:
                if int(to_acct) not in otherAccounts:
                    message = "Error. Make sure you enter the correct account #."
                    destAcct.set("")
                if not flag_amount:
                    message = "Error. Make sure you enter a valid amount greater than 0."
                    tfs_amount.set("")
                messagebox.showinfo('Error', message)
        except:
            messagebox.showinfo('Error', "Invalid amount.")
            tfs_amount.set("")


def TFS():
    global srcAcct
    global destAcct
    global tfs_amount
    global tfsWindow

    tfsWindow = Toplevel(root)
    tfsWindow.title("Transfers")
    tfsWindow.geometry("450x600")

    srcAcct = IntVar()
    destAcct = StringVar()
    tfs_amount = StringVar()

    Label(tfsWindow, text='New York Bank', bd=4, font=('arial', 35, 'bold'), relief="groove", fg="white", bg="blue",
          width=300).pack()
    Label(tfsWindow, text="").pack()

    Label(tfsWindow, text='Make A Transfer', fg="black", font=('arial', 20, 'bold', 'underline')).pack()
    Label(tfsWindow, text="").pack()
    Label(tfsWindow, text="").pack()

    Label(tfsWindow, text="From account:", fg="black", font=('arial', 16, 'bold')).pack()
    for index, val in enumerate(activeAccounts):
        Radiobutton(tfsWindow, text=val, variable=srcAcct, value=val).pack()

    Label(tfsWindow, text="").pack()
    Label(tfsWindow, text="Transfer to (account #):", fg="black", font=('arial', 15, 'bold')).pack()
    Entry(tfsWindow, textvariable=destAcct).pack()
    Label(tfsWindow, text="").pack()

    Label(tfsWindow, text="Enter Amount:", fg="black", font=('arial', 15, 'bold')).pack()
    Entry(tfsWindow, textvariable=tfs_amount).pack()
    Label(tfsWindow, text="").pack()

    Button(tfsWindow, text="Transfer", fg="blue", relief="groove",
           font=('arial', 14, 'bold'), command=makeTransfer).pack()
    tfsWindow.bind('<Return>', makeTransfer)


def viewTXNS():
    acct = src_acct.get()
    # get all transactions (user either initiated a deposit/withdraw/transfer or received a transfer)
    sql18 = "select T.* " \
            "from transactions T, cust_acct CA, customers C " \
            "where T.src_acct = CA.account_no and CA.Ssn = C.Ssn and T.src_acct = %s " \
            "union " \
            "select T.* " \
            "from transactions T, cust_acct CA, customers C " \
            "where T.src_acct = CA.account_no and CA.Ssn = C.Ssn and T.dest_acct = %s"
    val18 = (acct, acct)
    mycursor.execute(sql18, val18)
    txns = mycursor.fetchall()
    if mycursor.rowcount > 0:
        # delete transactions from table if user wants to use a different account
        txn_tbl.delete(*txn_tbl.get_children())
        txn_tbl.pack()

        for index, val in enumerate(txns):
            # get transactions where user is the source
            txn_id, txn_type, amount, date_posted, src, dest = val
            sql19 = "select fname, lname, account_no " \
                    "from cust_acct natural join customers " \
                    "where cust_acct.account_no = %s"
            val19 = (src,)
            mycursor.execute(sql19, val19)
            result = mycursor.fetchone()
            sender_name = "{} {}".format(result[0], result[1])
            sender_acct = " ..." + str(result[2])[-4:]
            # if you are the src acct, then just display last 4 acct numbers, else display the name of person
            if src in activeAccounts:
                sender = sender_acct
            else:
                sender = sender_name

            # get transactions where user is on the receiving end
            sql20 = "select fname, lname, account_no " \
                    "from cust_acct natural join customers " \
                    "where cust_acct.account_no = %s"
            val20 = (dest,)
            mycursor.execute(sql20, val20)
            result = mycursor.fetchone()
            receiver_name = "{} {}".format(result[0], result[1])
            receiver_acct = " ..." + str(result[2])[-4:]
            # if you are the dest acct, then just display last 4 acct numbers, else display the name of person
            if dest in activeAccounts:
                receiver = receiver_acct
            else:
                receiver = receiver_name

            # add transaction to table
            txn_tbl.insert(parent='', index='end', iid=index, text='',
                           values=(txn_id, txn_type, amount, date_posted, sender, receiver))


def TXN():
    global src_acct
    global txnWindow
    global txn_tbl
    txnWindow = Toplevel(root)
    txnWindow.title("Transactions")
    txnWindow.geometry("900x500")

    src_acct = IntVar()

    Label(txnWindow, text='New York Bank', bd=4, font=('arial', 35, 'bold'), relief="groove", fg="white", bg="blue",
          width=300).pack()
    Label(txnWindow, text="").pack()

    Label(txnWindow, text='View Transactions', fg="black", font=('arial', 20, 'bold', 'underline')).pack()
    Label(txnWindow, text="").pack()
    Label(txnWindow, text="").pack()

    Label(txnWindow, text="Choose account:", fg="black", font=('arial', 16, 'bold')).pack()
    for index, val in enumerate(activeAccounts):
        Radiobutton(txnWindow, text=val, variable=src_acct, value=val, command=viewTXNS).pack()
    Label(txnWindow, text="").pack()

    txn_tbl = ttk.Treeview(txnWindow, height=5)
    txn_tbl['columns'] = ('txnID', 'type', 'amount', 'dateposted', 'from', 'to')
    txn_tbl.column("#0", width=0, stretch=NO)
    txn_tbl.column("txnID", anchor=CENTER, width=75)
    txn_tbl.column("type", anchor=CENTER, width=100)
    txn_tbl.column("amount", anchor=CENTER, width=150)
    txn_tbl.column("dateposted", anchor=CENTER, width=150)
    txn_tbl.column("from", anchor=CENTER, width=200)
    txn_tbl.column("to", anchor=CENTER, width=200)

    txn_tbl.heading("#0", text="", anchor=CENTER)
    txn_tbl.heading("txnID", text="TXN ID", anchor=CENTER)
    txn_tbl.heading("type", text="Type", anchor=CENTER)
    txn_tbl.heading("amount", text="Amount", anchor=CENTER)
    txn_tbl.heading("dateposted", text="Date posted", anchor=CENTER)
    txn_tbl.heading("from", text="Source", anchor=CENTER)
    txn_tbl.heading("to", text="Destination", anchor=CENTER)
    txn_tbl.pack_forget()


def update(event=None):
    global newPasswd

    new_passwd = newPasswd.get()
    sql21 = "update customers " \
            "set password = %s " \
            "where username = %s and password = %s"
    values21 = (new_passwd, user, passwd)
    mycursor.execute(sql21, values21)
    mydb.commit()
    messagebox.showinfo('Update Saved', 'You have successfully changed your password. You can now log back in.')

    # Once the user changes their password, log them out by resetting the connection to the database
    mydb.cmd_reset_connection()

    # destroy this frame and hide it
    for widget in frame3.winfo_children():
        widget.destroy()
    frame3.pack_forget()

    # Go back to login page to login again with the new password
    login_page()


def CP():
    global newPasswd
    frame3.pack()
    # destroy widgets in frame2 to show new frame instead of opening another window
    for widget in frame2.winfo_children():
        widget.destroy()
    frame2.pack_forget()

    newPasswd = StringVar()

    Label(frame3, text="Hello " + usersname + ".", fg="black", font=('arial', 20, 'bold')).pack()
    Label(frame3, text="").pack()
    Label(frame3, text="Enter new password :", fg="black", font=('arial', 16, 'bold')).pack()
    Entry(frame3, textvariable=newPasswd, show='*').pack(pady=15)

    Button(frame3, text="Update", fg="blue", relief="groove", font=('arial', 14, 'bold'), command=update).pack()
    root.bind('<Return>', update)


def getLocations(event=None):
    city = locate.get().lower()

    if city == "new york city":
        city = "new york"
    # retrieve branch locations
    sql22 = "select * " \
            "from branch natural join branch_location " \
            "where city = %s"
    val22 = (city,)
    mycursor.execute(sql22, val22)
    branches = mycursor.fetchall()
    if mycursor.rowcount > 0:
        # delete branch locations from table if user wants to search for new location
        br_tbl.delete(*br_tbl.get_children())
        br_tbl.pack()

        # get values to insert into table
        for index, val in enumerate(branches):
            zip, b_id, br_name, st, city = val
            address = "{}\n{}, {} {}\n".format(st, city, "NY", zip)
            br_tbl.insert(parent='', index='end', iid=index, text='', values=(br_name, address))
    else:
        messagebox.showinfo('Error', 'No branches found')

    locate.set("")


def FB():
    global locate
    global brWindow
    global br_tbl

    # create new window
    brWindow = Toplevel(root)
    brWindow.title("Branch Locations")
    brWindow.geometry("900x500")

    locate = StringVar()

    Label(brWindow, text='New York Bank', bd=5, font=('arial', 36, 'bold'), relief="groove", fg="white", bg="blue",
          width=300).pack()
    Label(brWindow, text="").pack()

    Label(brWindow, text='Find A Branch', fg="black", font=('arial', 20, 'bold', 'underline')).pack()
    Label(brWindow, text="").pack()

    Label(brWindow, text="Enter city", fg="black", font=('arial', 15, 'bold')).pack()
    Entry(brWindow, textvariable=locate).pack()

    Button(brWindow, text="Go", fg="blue", relief="groove", font=('arial', 14, 'bold'), command=getLocations).pack()
    brWindow.bind('<Return>', getLocations)
    Label(brWindow, text="").pack()

    # create table to display the branch locations and then hide it
    br_tbl = ttk.Treeview(brWindow, height=5)
    br_tbl['columns'] = ('branch', 'address')
    br_tbl.column("#0", width=0, stretch=NO)
    br_tbl.column("branch", anchor=CENTER, width=250)
    br_tbl.column("address", anchor=CENTER, width=575)

    br_tbl.heading("#0", text="", anchor=CENTER)
    br_tbl.heading("branch", text="Branch name", anchor=CENTER)
    br_tbl.heading("address", text="Address", anchor=CENTER)
    br_tbl.pack_forget()


def logoff():
    # display logoff pop up window and terminate main page
    messagebox.showinfo('Logout', 'Thank you for choosing\n New York Bank.')
    mydb.close()
    root.destroy()


def optionPage():

    Label(frame2, text="Hello " + usersname + ".", fg="black", font=('arial', 20, 'bold')).pack()
    Label(frame2, text="What can we do for you today?", fg="black", font=('arial', 20, 'bold')).pack()
    Label(frame2, text="").pack()
    checkBal = Button(frame2, text="Check Balance", width=15, height=2, fg="blue", relief="groove",
                      font=('arial', 14, 'bold'), command=CB)
    checkBal.pack()
    Label(frame2, text="").pack()

    deposit = Button(frame2, text="Deposit", width=15, height=2, fg="blue", relief="groove",
                     font=('arial', 14, 'bold'), command=DEP)
    deposit.pack()
    Label(frame2, text="").pack()

    withdraw = Button(frame2, text="Withdrawal", width=15, height=2, fg="blue", relief="groove",
                      font=('arial', 14, 'bold'), command=WD)
    withdraw.pack()
    Label(frame2, text="").pack()

    transfer = Button(frame2, text="Money Transfer", width=15, height=2, fg="blue", relief="groove",
                      font=('arial', 14, 'bold'), command=TFS)
    transfer.pack()
    Label(frame2, text="").pack()

    transactions = Button(frame2, text="View Transactions", width=15, height=2, fg="blue", relief="groove",
                          font=('arial', 14, 'bold'), command=TXN)
    transactions.pack()
    Label(frame2, text="").pack()

    changePass = Button(frame2, text="Change password", width=15, height=2, fg="blue", relief="groove",
                        font=('arial', 14, 'bold'), command=CP)
    changePass.pack()
    Label(frame2, text="").pack()

    findBR = Button(frame2, text="Find a Branch", width=15, height=2, fg="blue", relief="groove",
                    font=('arial', 14, 'bold'), command=FB)
    findBR.pack()
    Label(frame2, text="").pack()

    logout = Button(frame2, text="Logout", width=15, height=2, fg="blue", relief="groove",
                    font=('arial', 14, 'bold'), command=logoff)
    logout.pack()


def login(event=None):
    global usersname
    global user
    global passwd
    global activeAccounts

    user = username.get()
    passwd = password.get()

    # verify the users information and get their name
    sql6 = "select * from CUSTOMERS where username = %s and password = %s"
    values6 = (user, passwd)
    mycursor.execute(sql6, values6)
    result = mycursor.fetchone()
    if mycursor.rowcount > 0:
        # show new frame for main page and option widgets
        frame2.pack()
        # destroy existing widgets in frame if user has to log back in with new password
        for widget in frame1.winfo_children():
            widget.destroy()

        # hide frame to go into option page
        frame1.pack_forget()
        usersname = result[0]

        # retrieve all the users accounts and add them into a set so they can be displayed
        sql7 = "select account_no " \
               "from CUSTOMERS natural join CUST_ACCT " \
               "where username = %s and password = %s"
        values7 = (user, passwd)
        mycursor.execute(sql7, values7)
        results = mycursor.fetchall()
        for line in results:
            activeAccounts.add(line[0])
        optionPage()
    else:
        # pop up alert error message
        messagebox.showinfo('Error', 'Incorrect username or password. Try again.')
        username.set("")
        password.set("")


def login_page():
    global username
    global password

    frame1.pack()

    username = StringVar()
    password = StringVar()

    welcome_label = Label(frame1, text='Welcome User!', font=('arial', 32, 'bold'), fg="black", width=300)
    welcome_label.pack()
    Label(frame1, text="").pack()

    Label(frame1, text="Username :", fg="black", font=('arial', 16, 'bold')).pack()
    Entry(frame1, textvariable=username).pack(pady=15)

    Label(frame1, text="Password :", fg="black", font=('arial', 16, 'bold')).pack()
    Entry(frame1, textvariable=password, show='*').pack(pady=15)

    Button(frame1, text="Login", fg="blue", relief="groove", font=('arial', 14, 'bold'), command=login).pack()
    root.bind('<Return>', login)
    root.mainloop()


def main():
    login_page()


if __name__ == "__main__":
    main()

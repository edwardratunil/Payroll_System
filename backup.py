# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 14:00:44 2023

@author: Edward Ratunil
"""

from tkinter import *
import tkinter.ttk as ttk
import sqlite3
import tkinter.messagebox as tkMessageBox


def database():
    conn = sqlite3.connect("backup_system.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS 'TblPassword' (employee_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, Email TEXT)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS 'TblEmployees' (employee_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, employee_no TEXT, firstname TEXT, lastname TEXT, middlename TEXT, address TEXT, age INTEGER , contact INTEGER, rate_per_hour NUMERIC)")
    cursor.close()
    conn.close()

    print("Database Connected")


def submit_reg():
    if EMPLOYEE_NO.get() == "" or FIRSTNAME.get() == "" or LASTNAME.get() == "" or MIDDLENAME.get() == "" or ADDRESS.get() == "" or AGE.get() == "" or CONTACT.get() == "" or RATE.get() == "":
        result = tkMessageBox.showwarning('', 'Please Complete The Required Field', icon="warning")
    else:
        try:
            employee_no = EMPLOYEE_NO.get()
            firstname = FIRSTNAME.get()
            lastname = LASTNAME.get()
            middlename = MIDDLENAME.get()
            address = ADDRESS.get()
            age = int(AGE.get())
            contact = int(CONTACT.get())
            rate_per_hour = int(RATE.get())

            # lastname contain only alphabetic characters
            if not lastname.isalpha():
                raise ValueError

        except ValueError:
            result = tkMessageBox.showwarning('', 'Invalid Input', icon="warning")
        else:
            conn = sqlite3.connect("payroll_system.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO 'TblEmployees' (employee_no, firstname, lastname, middlename, address, age, contact, rate_per_hour) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (employee_no, firstname, lastname, middlename, address, age, contact, rate_per_hour))
            conn.commit()
            cursor.close()
            conn.close()
            result = tkMessageBox.showinfo("", "Registered Successfully!")
            EMPLOYEE_NO.set("")
            FIRSTNAME.set("")
            LASTNAME.set("")
            MIDDLENAME.set("")
            ADDRESS.set("")
            AGE.set("")
            CONTACT.set("")
            RATE.set("")
            RegWindow.destroy()


def select_menu():
    def selection2():
        def submit():
            print("Register")

        # SELECTION AREA FOR REGISTRATION PROFILE, EMPLOYEE`S LIST, PASSWORD MANAGEMENT AND LOGIN PASSWORD

        selection = SELECTION.get()
        if selection == "  Employee`s Registration Profile":
            print("Employee`s Registration Profile")

            global RegWindow
            RegWindow = Toplevel()
            RegWindow.title("SignUp Payroll Management System")
            RegWindow.configure(bg='#253342')
            width = 760
            height = 320
            screen_width = RegWindow.winfo_screenwidth()
            screen_height = RegWindow.winfo_screenheight()
            x = (screen_width / 2) - (width / 2)
            y = (screen_height / 2) - (height / 2)
            RegWindow.resizable(False, False)
            RegWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))

            signup_frame = Frame(RegWindow, bg='#253342')
            signup_frame.pack()

            # Saving User Info
            user_info_frame = LabelFrame(signup_frame, text="User Registration", foreground='white', bg='#253342')
            user_info_frame.grid(row=0, column=0, sticky="news", padx=20, pady=10)

            employee_no_label = Label(user_info_frame, text="Employee No :", foreground='white', bg='#253342')
            employee_no_label.grid(row=0, column=0)
            employee_no_entry = Entry(user_info_frame, textvariable=EMPLOYEE_NO, width=23)
            employee_no_entry.grid(row=0, column=1, padx=10, pady=10)

            first_name_label = Label(user_info_frame, text="First Name :", foreground='white', bg='#253342')
            first_name_label.grid(row=1, column=0)
            first_name_entry = Entry(user_info_frame, textvariable=FIRSTNAME, width=23)
            first_name_entry.grid(row=1, column=1, padx=10, pady=10)

            last_name_label = Label(user_info_frame, text="Last Name :", foreground='white', bg='#253342')
            last_name_label.grid(row=1, column=2)
            last_name_entry = Entry(user_info_frame, textvariable=LASTNAME, width=23)
            last_name_entry.grid(row=1, column=3, padx=10, pady=10)

            middle_name_label = Label(user_info_frame, text="Middle Name :", foreground='white', bg='#253342')
            middle_name_label.grid(row=1, column=4)
            middle_name_entry = Entry(user_info_frame, textvariable=MIDDLENAME, width=23)
            middle_name_entry.grid(row=1, column=5, padx=10, pady=10)

            address_label = Label(user_info_frame, text="Address :", foreground='white', bg='#253342')
            address_label.grid(row=2, column=0)
            address_entry = Entry(user_info_frame, textvariable=ADDRESS, width=23)
            address_entry.grid(row=2, column=1, columnspan=3, sticky="we", padx=10, pady=10)

            age_label = Label(user_info_frame, text="Age :", foreground='white', bg='#253342')
            age_label.grid(row=2, column=4)
            age_spinbox = Spinbox(user_info_frame, textvariable=AGE, from_=18, to=110, width=21)
            age_spinbox.grid(row=2, column=5, padx=10, pady=10)

            contact_label = Label(user_info_frame, text="Contact: ", foreground='white', bg='#253342')
            contact_label.grid(row=4, column=0)
            contact_entry = Entry(user_info_frame, textvariable=CONTACT)
            contact_entry.grid(row=4, column=1, sticky="we", padx=10, pady=10)

            rate_per_hour_label = Label(user_info_frame, text="Rate/Hour :", foreground='white', bg='#253342')
            rate_per_hour_label.grid(row=5, column=0)
            rate_per_hour_entry = Entry(user_info_frame, textvariable=RATE)
            rate_per_hour_entry.grid(row=5, column=1, sticky="we", padx=10, pady=10)

            # Button

            signup_button = Button(signup_frame, text="Confirm", foreground='white', bg='#3C6E71', command=submit_reg)
            signup_button.grid(row=2, column=0, sticky="news", padx=20, pady=5)
            exit_button = Button(signup_frame, text="Exit", foreground='#253342', bg='#D9D9D9',
                                 command=RegWindow.destroy)
            exit_button.grid(row=3, column=0, sticky="news", padx=20, pady=10)

        elif selection == "  Employee`s List":
            def update_list(tree):
                conn = sqlite3.connect("payroll_system.db")
                cursor = conn.cursor()
                # Retrieve all columns from TblEmployees and only 'username' and 'password' columns from TblPassword
                cursor.execute(
                    "SELECT TblEmployees.*, TblPassword.username, TblPassword.password, TblPassword.email FROM TblEmployees JOIN TblPassword ON TblEmployees.employee_id = TblPassword.employee_id ORDER BY TblEmployees.lastname ASC")
                fetch = cursor.fetchall()
                for data in fetch:
                    tree.insert('', 'end', values=data)

                cursor.close()
                conn.close()

            def search_callback(*args):
                search_term = search_var.get()
                conn = sqlite3.connect("payroll_system.db")
                cursor = conn.cursor()
                tree.delete(*tree.get_children())
                cursor.execute(
                    "SELECT TblEmployees.*, TblPassword.username, TblPassword.password, TblPassword.email FROM TblEmployees JOIN TblPassword ON TblEmployees.employee_id = TblPassword.employee_id WHERE lastname LIKE ?",
                    (f'%{search_term}%',)
                )
                for row in cursor.fetchall():
                    tree.insert("", "end", values=row)

            print("Register")
            global List_Window
            List_Window = Toplevel()
            List_Window.title("Menu Payroll Management System")
            List_Window.configure(bg='#253342')
            width = 1230
            height = 400
            screen_width = List_Window.winfo_screenwidth()
            screen_height = List_Window.winfo_screenheight()
            x = (screen_width / 2) - (width / 2)
            y = (screen_height / 2) - (height / 2)
            List_Window.resizable(False, False)
            List_Window.geometry("%dx%d+%d+%d" % (width, height, x, y))

            Main = Frame(List_Window, bg='#253342')
            Main.pack()

            frame1 = LabelFrame(Main, bg='#253342')
            frame1.grid(row=0, column=0, sticky="news", padx=20, pady=10)

            # LABEL (MAIN)
            search_label = Label(frame1, text="Employee`s List", font=("Courier", 14), foreground='white', bg='#253342')
            search_label.grid(row=0, column=0, sticky="news", padx=20, pady=10)

            TableMargin = Frame(List_Window, width=500)
            TableMargin.pack(side=TOP)

            # TABLES (MAIN)
            scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
            scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
            tree = ttk.Treeview(TableMargin,
                                columns=(
                                    "Employee_No", "Employee_Type", "Employee_Name", "Last_Name", "Middle_Name", "Age",
                                    "Gender",
                                    "Address", "Contact", "Username", "Password", "Email"),
                                height=400, selectmode="extended", yscrollcommand=scrollbary.set,
                                xscrollcommand=scrollbarx.set)
            scrollbary.config(command=tree.yview)
            scrollbary.pack(side=RIGHT, fill=Y)
            scrollbarx.config(command=tree.xview)
            scrollbarx.pack(side=BOTTOM, fill=X)
            tree.heading('Employee_No', text="Employee No.", anchor=W)
            tree.heading('Employee_Type', text="Employee Type", anchor=W)
            tree.heading('Employee_Name', text="Employee Name", anchor=W)
            tree.heading('Last_Name', text="Last_Name", anchor=W)
            tree.heading('Middle_Name', text="Middle_Name", anchor=W)
            tree.heading('Age', text="Age", anchor=W)
            tree.heading('Gender', text="Gender", anchor=W)
            tree.heading('Address', text="Address", anchor=W)
            tree.heading('Contact', text="Contact", anchor=W)
            tree.heading('Username', text="Username", anchor=W)
            tree.heading('Password', text="Password", anchor=W)
            tree.heading('Email', text="Email", anchor=W)
            tree.column('#0', stretch=NO, minwidth=0, width=0)
            tree.column('#1', stretch=NO, minwidth=0, width=0)
            tree.column('#2', stretch=NO, minwidth=0, width=100)
            tree.column('#3', stretch=NO, minwidth=0, width=110)
            tree.column('#4', stretch=NO, minwidth=0, width=110)
            tree.column('#5', stretch=NO, minwidth=0, width=90)
            tree.column('#6', stretch=NO, minwidth=0, width=50)
            tree.column('#7', stretch=NO, minwidth=0, width=70)
            tree.column('#8', stretch=NO, minwidth=0, width=120)
            tree.column('#9', stretch=NO, minwidth=0, width=100)
            tree.column('#10', stretch=NO, minwidth=0, width=100)
            tree.column('#11', stretch=NO, minwidth=0, width=100)
            tree.pack()

        elif selection == "  Password Management":
            Password_Window = Toplevel()
            Password_Window.title("Password Management")
            Password_Window.configure(bg='#253342')
            width = 760
            height = 450
            screen_width = Password_Window.winfo_screenwidth()
            screen_height = Password_Window.winfo_screenheight()
            x = (screen_width / 2) - (width / 2)
            y = (screen_height / 2) - (height / 2)
            Password_Window.resizable(False, False)
            Password_Window.geometry("%dx%d+%d+%d" % (width, height, x, y))

        elif selection == "  Login Password":
            Password_Window2 = Toplevel()
            Password_Window2.title("Login Password")
            Password_Window2.configure(bg='#253342')
            width = 760
            height = 450
            screen_width = Password_Window2.winfo_screenwidth()
            screen_height = Password_Window2.winfo_screenheight()
            x = (screen_width / 2) - (width / 2)
            y = (screen_height / 2) - (height / 2)
            Password_Window2.resizable(False, False)
            Password_Window2.geometry("%dx%d+%d+%d" % (width, height, x, y))


    select_window = Tk()
    select_window.title("Payroll Management System")
    select_window.configure(bg='#253342')
    width = 450
    height = 260
    screen_width = select_window.winfo_screenwidth()
    screen_height = select_window.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    select_window.geometry("%dx%d+%d+%d" % (width, height, x, y))

    SELECTION = StringVar()

    select_window_frame = Frame(select_window, bg='#253342')
    select_window_frame.pack(side=TOP, pady=10)

    # Saving User Info
    system_frame = LabelFrame(select_window_frame, text=" Select Menu: ", foreground='white', bg='#253342')
    system_frame.grid(row=0, column=0, sticky="news", padx=20, pady=20)

    system_label = Label(system_frame, foreground='white', bg='#253342')
    system_label.grid(row=0, column=0)
    system_combobox = ttk.Combobox(system_frame, width=30,
                                   values=["== System Task ==", "  Employee`s Registration Profile", "  Employee`s List", "", "== System Maintenance ==", "  Password Management", "  Login Password"],
                                   textvariable=SELECTION)
    system_combobox.grid(row=0, column=1, padx=10, pady=10)

    selection_button1 = Button(select_window_frame, text="Confirm", command=selection2, width=10)
    selection_button1.grid(row=2, column=0, sticky="news",padx=20, pady=5)

    selection_button2 = Button(select_window_frame, text="Exit", command=select_window.destroy, width=10)
    selection_button2.grid(row=3, column=0, sticky="news", padx=20, pady=5)


failure_max = 3


def check_login(username, password):
    # Connect to the database
    conn = sqlite3.connect("backup_system.db")
    c = conn.cursor()
    # Execute a query to check if the username and password are correct
    c.execute("SELECT * FROM TblPassword WHERE username=? AND password=?", (username, password))
    result = c.fetchone()

    # Close the database connection
    conn.close()

    return result


def enter(event):
    check_password()


def check_password():
    """ Collect 1's for every failure and quit program in case of failure_max failures """
    username = login_user.get()
    password = login_password.get()
    if result := check_login(username, password):
        check_password.user = username
        print('Logged in')
        root.destroy()
        select_menu()
    else:
        check_password.failures += 1
        if check_password.failures == failure_max:
            root.destroy()
            raise SystemExit(tkMessageBox.showwarning('', 'Unauthorized login attempt', icon="warning"))
        else:
            root.title('Try again. Attempt')
            result = tkMessageBox.showwarning('', 'Invalid, Account & Password', icon="warning")
            login_user.delete(0, END)
            login_password.delete(0, END)


check_password.failures = 0

if __name__ == '__main__':

    root = Tk()
    root.title("Payroll Management System")
    width = 330
    height = 230
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.resizable(False, False)
    root.config(bg="#253342")

    # Variable
    EMPLOYEE_NO = StringVar()
    FIRSTNAME = StringVar()
    LASTNAME = StringVar()
    MIDDLENAME = StringVar()
    ADDRESS = StringVar()
    AGE = StringVar()
    CONTACT = StringVar()
    RATE = StringVar()
    USERNAME = StringVar()
    PASSWORD = StringVar()
    EMAIL = StringVar()
    RPH = StringVar()
    NHW = StringVar()
    SSS = StringVar()
    PHILHEALTH = StringVar()
    PAGIBIG = StringVar()
    CASHADVANCE = StringVar()
    NETPAY = StringVar()
    search_var = StringVar()

    frame = Frame(root, bg='#253342')
    frame.pack()

    parent = LabelFrame(frame, text="Login", foreground='white', bg='#253342')
    parent.grid(row=0, column=0, sticky="news", padx=10, pady=10)

    login_user = Label(parent, text="Username", foreground='white', bg='#253342')
    login_user.grid(row=1, column=0)
    login_user = Entry(parent, width=23)
    login_user.grid(row=1, column=1, padx=10, pady=10)

    login_password = Label(parent, text="Password", foreground='white', bg='#253342')
    login_password.grid(row=2, column=0)
    login_password = Entry(parent, width=23, show="*")
    login_password.grid(row=2, column=1, padx=10, pady=10)

    # Button
    button = Button(frame, text="Login", foreground='#253342', bg='white', command=check_password)
    button.grid(row=1, column=0, sticky="news", padx=10, pady=2)
    login_password.bind('<Return>', enter)

    database()
    root.focus_set()
    root.mainloop()

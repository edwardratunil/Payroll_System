# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 14:00:44 2023

@author: Edward Ratunil
"""

from tkinter import *
import tkinter.ttk as ttk
import sqlite3
import tkinter.messagebox as tkMessageBox


# print("TEST CODE PRESS")


def database():
    conn = sqlite3.connect("payroll_system.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS 'TblPassword' (employee_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, email TEXT)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS 'TblEmployees' (employee_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, employee_no INTEGER, firstname TEXT, lastname TEXT, middlename TEXT, address TEXT, age INTEGER , contact INTEGER, rate_per_hour NUMERIC)")
    cursor.close()
    conn.close()

    print("Database Connected")


def menu_password_management():
    # Variable
    USERNAME_INFO = StringVar()
    PASSWORD_INFO = StringVar()
    EMAIL_INFO = StringVar()

    def password_update_registration():
        password = PASSWORD_INFO.get()
        email = EMAIL_INFO.get()
        if not tree.selection():
            result = tkMessageBox.showwarning('', 'Please Select Something First!', icon="warning")
            return

        if PASSWORD_INFO.get() == "" or EMAIL_INFO.get() == "":
            result = tkMessageBox.showwarning('', 'Please Complete The Required Field', icon="warning")

        elif len(PASSWORD_INFO.get()) > 14:
            result = tkMessageBox.showwarning('', 'Username and password should not exceed 14 characters',
                                              icon="warning")

        else:
            conn = sqlite3.connect("payroll_system.db")
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE TblPassword SET password=?, email=? WHERE employee_id = ?",
                (password, email, employee_id))
            conn.commit()
            cursor.close()
            conn.close()
            result = tkMessageBox.showinfo("", "Account Updated Successfully!")
            USERNAME_INFO.set("")
            PASSWORD_INFO.set("")
            EMAIL_INFO.set("")
            menu_reg_search_callback()

    def menu_login_reg():
        username = USERNAME_INFO.get()
        password = PASSWORD_INFO.get()
        email = EMAIL_INFO.get()

        if USERNAME_INFO.get() == "" or PASSWORD_INFO.get() == "" or EMAIL_INFO.get() == "":
            result = tkMessageBox.showwarning('', 'Please Complete The Required Field', icon="warning")

        elif len(USERNAME_INFO.get()) > 14 or len(PASSWORD_INFO.get()) > 14:
            result = tkMessageBox.showwarning('', 'Username and password should not exceed 14 characters',
                                              icon="warning")

        else:
            conn = sqlite3.connect("payroll_system.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM TblPassword WHERE username=?", (username,))
            result1 = cursor.fetchone()
            if result1:
                tkMessageBox.showwarning('', 'Username Already Exist!', icon="warning")
            else:
                cursor.execute(
                    "INSERT INTO 'TblPassword' (username, password, email) VALUES (?, ?, ?)",
                    (username, password, email))
                conn.commit()
                cursor.close()
                conn.close()
                result = tkMessageBox.showinfo("", "Account Registered Successfully!")
                USERNAME_INFO.set("")
                PASSWORD_INFO.set("")
                EMAIL_INFO.set("")
                menu_reg_search_callback()

    menu_reg_search_var = StringVar()

    def menu_reg_search_callback(*args):
        search_term = menu_reg_search_var.get()
        conn = sqlite3.connect("payroll_system.db")
        cursor = conn.cursor()
        tree.delete(*tree.get_children())
        cursor.execute(
            "SELECT * FROM 'TblPassword' WHERE username LIKE ? ORDER BY employee_id",
            (f'%{search_term}%',)
        )
        for row in cursor.fetchall():
            item_values = list(row)
            item_values[2] = "*" * len(str(item_values[2]))
            tree.insert("", "end", values=item_values)

    def Selected(event):
        global employee_id
        curItem = tree.focus()
        contents = tree.item(curItem)
        selectedItem = contents['values']
        employee_id = selectedItem[0]
        USERNAME_INFO.set(selectedItem[1])
        PASSWORD_INFO.set(selectedItem[2])
        EMAIL_INFO.set(selectedItem[3])

        conn = sqlite3.connect("payroll_system.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM 'TblPassword' ORDER BY 'username' ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            if data[0] == employee_id:
                USERNAME_INFO.set(data[1])
                PASSWORD_INFO.set(data[2])
                EMAIL_INFO.set(data[3])
        cursor.close()
        conn.close()

    def clear_field():
        USERNAME_INFO.set("")
        PASSWORD_INFO.set("")
        EMAIL_INFO.set("")

    def password_delete_data():
        if not tree.selection():
            result = tkMessageBox.showwarning('', 'Please Select Something First!', icon="warning")
        else:
            result = tkMessageBox.askquestion('', 'Are you sure you want to delete this record?', icon="warning")
            if result == 'yes':
                curItem = tree.focus()
                contents = (tree.item(curItem))
                selectedItem = contents['values']
                tree.delete(curItem)
                conn = sqlite3.connect("payroll_system.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM TblPassword WHERE employee_id = ?", (selectedItem[0],))
                conn.commit()
                cursor.close()
                conn.close()

    def checkbox_password():
        if password_info_entry.cget('show') == '':
            password_info_entry.configure(show='*')
        else:
            password_info_entry.configure(show='')

    menu_password_window = Toplevel()
    menu_password_window.title("Password Management")
    menu_password_window.configure(bg='#185C37')
    width = 685
    height = 450
    screen_width = menu_password_window.winfo_screenwidth()
    screen_height = menu_password_window.winfo_screenheight()
    x = ((screen_width / 2) - 500) - (width / 2)
    y = ((screen_height / 2) + 20) - (height / 2)
    menu_password_window.geometry("%dx%d+%d+%d" % (width, height, x, y))
    menu_password_window.resizable(False, False)

    password_management_frame = Frame(menu_password_window, bg='#185C37')
    password_management_frame.pack()

    # Saving User Info
    password_management_info_frame = LabelFrame(password_management_frame, text="Account Register Information",
                                                foreground='white',
                                                bg='#185C37')
    password_management_info_frame.grid(row=0, column=0, sticky="news", padx=20, pady=10)

    username_info_label = Label(password_management_info_frame, text="Username :", foreground='white', bg='#185C37')
    username_info_label.grid(row=0, column=0)
    username_info_entry = Entry(password_management_info_frame, textvariable=USERNAME_INFO, width=23)
    username_info_entry.grid(row=0, column=1, sticky="news", padx=10, pady=10)

    password_info_label = Label(password_management_info_frame, text="Password :", foreground='white', bg='#185C37')
    password_info_label.grid(row=0, column=2)
    password_info_entry = Entry(password_management_info_frame, textvariable=PASSWORD_INFO, width=23, show="*")
    password_info_entry.grid(row=0, column=3, sticky="news", padx=10, pady=10)

    show_password = Checkbutton(password_management_info_frame, command=checkbox_password, activebackground='#185C37',
                                bg='#185C37')
    show_password.grid(row=0, column=4, sticky="w")

    email_info_label = Label(password_management_info_frame, text="Email :", foreground='white', bg='#185C37')
    email_info_label.grid(row=1, column=0)
    email_info_entry = Entry(password_management_info_frame, textvariable=EMAIL_INFO, width=23)
    email_info_entry.grid(row=1, column=1, sticky="news", padx=10, pady=10)

    # Button
    button_management_frame = LabelFrame(password_management_frame, text="", foreground='white', bg='#185C37')
    button_management_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

    menu_reg_clearfield_button = Button(button_management_frame, text="Clear Field", foreground='black', bg='white',
                                        command=clear_field, width=20)
    menu_reg_clearfield_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    menu_reg_register_button = Button(button_management_frame, text="Register", foreground='black', bg='white',
                                      command=menu_login_reg, width=20)
    menu_reg_register_button.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

    menu_reg_update_button = Button(button_management_frame, text="Update", foreground='black', bg='white',
                                    command=password_update_registration,
                                    width=20)
    menu_reg_update_button.grid(row=0, column=2, sticky="ew", padx=5, pady=5)
    menu_reg_delete_button = Button(button_management_frame, text="Delete", foreground='black', bg='white',
                                    command=password_delete_data,
                                    width=20)
    menu_reg_delete_button.grid(row=0, column=3, sticky="ew", padx=5, pady=5)

    # Search

    search_info_frame = LabelFrame(password_management_frame, text="", foreground='white', bg='#185C37')
    search_info_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)

    menu_reg_search_label = Label(search_info_frame, text="Search by Username :", foreground='white', bg='#185C37')
    menu_reg_search_label.grid(row=0, column=0, padx=20, pady=10)
    menu_reg_search_var.trace("w", menu_reg_search_callback)
    menu_reg_search_entry = Entry(search_info_frame, textvariable=menu_reg_search_var, width=30)
    menu_reg_search_entry.grid(row=0, column=1, padx=10, pady=10)

    TableMargin = Frame(password_management_frame)
    TableMargin.grid(row=3, column=0, sticky="news", padx=20, pady=10)

    # TABLES (MAIN)
    scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
    scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
    tree = ttk.Treeview(TableMargin,
                        columns=(
                            "Employee_Id", "Username", "Password", "Email"), height=5, selectmode="extended",
                        yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('Employee_Id', text="Employee Id.", anchor=W)
    tree.heading('Username', text="Username", anchor=W)
    tree.heading('Password', text="Password", anchor=W)
    tree.heading('Email', text="Email", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=0)
    tree.column('#2', stretch=NO, minwidth=0, width=200)
    tree.column('#3', stretch=NO, minwidth=0, width=200)
    tree.column('#4', stretch=NO, minwidth=0, width=210)
    tree.pack()
    tree.bind('<Double-Button-1>', Selected)
    menu_reg_search_callback()

    exit_management_button = Button(password_management_frame, text="Exit", foreground='black', bg='white',
                                    command=menu_password_window.destroy, width=20)
    exit_management_button.grid(row=4, column=0, padx=20, pady=10)


def menu_login_password():
    # Variable
    USERNAME = StringVar()
    PASSWORD = StringVar()

    def menu_login_reg():
        username = USERNAME.get()

        if USERNAME.get() == "" or PASSWORD.get() == "":
            result = tkMessageBox.showwarning('', 'Please Complete The Required Field', icon="warning")

        elif len(USERNAME.get()) > 14 or len(PASSWORD.get()) > 14:
            result = tkMessageBox.showwarning('', 'Username and Password should not exceed 14 characters',
                                              icon="warning")
        else:
            conn = sqlite3.connect("payroll_system.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM TblPassword WHERE username=?", (username,))
            result1 = cursor.fetchone()
            if result1:
                tkMessageBox.showwarning('', 'Username Already Exist!', icon="info")
            else:
                conn.commit()
                cursor.close()
                conn.close()
                tkMessageBox.showinfo("", "Account does not Exist!", icon="error")
                USERNAME.set("")
                PASSWORD.set("")
                return

    def checkbox_password():
        if password_entry.cget('show') == '':
            password_entry.configure(show='*')
        else:
            password_entry.configure(show='')

    menu_login_window = Toplevel()
    menu_login_window.title("Password Management")
    menu_login_window.configure(bg='#185C37')
    width = 300
    height = 210
    screen_width = menu_login_window.winfo_screenwidth()
    screen_height = menu_login_window.winfo_screenheight()
    x = ((screen_width / 2) - 500) - (width / 2)
    y = ((screen_height / 2) + 20) - (height / 2)
    menu_login_window.geometry("%dx%d+%d+%d" % (width, height, x, y))
    menu_login_window.resizable(False, False)

    password_management_frame = Frame(menu_login_window, bg='#185C37')
    password_management_frame.pack()

    # Saving Password Info

    pass_management_info_frame = LabelFrame(password_management_frame, text="Account Checker", foreground='white',
                                            bg='#185C37')
    pass_management_info_frame.grid(row=0, column=0, sticky="news", padx=20, pady=10)

    username_label = Label(pass_management_info_frame, text="Username :", foreground='white', bg='#185C37')
    username_label.grid(row=0, column=0)
    username_entry = Entry(pass_management_info_frame, textvariable=USERNAME, width=23)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    password_label = Label(pass_management_info_frame, text="Password :", foreground='white', bg='#185C37')
    password_label.grid(row=1, column=0)
    password_entry = Entry(pass_management_info_frame, textvariable=PASSWORD, width=23, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    show_password = Checkbutton(pass_management_info_frame, command=checkbox_password, activebackground='#185C37',
                                bg='#185C37')
    show_password.grid(row=1, column=2, sticky="w")

    # Button

    signup_button = Button(password_management_frame, text="Confirm", foreground='black', bg='white',
                           command=menu_login_reg)
    signup_button.grid(row=2, column=0, sticky="news", padx=20, pady=5)
    exit_button = Button(password_management_frame, text="Exit", foreground='black', bg='white',
                         command=menu_login_window.destroy)
    exit_button.grid(row=3, column=0, sticky="news", padx=20, pady=10)


def menu_list():
    search_var = StringVar()

    def search_callback(*args):
        search_term = search_var.get()
        conn = sqlite3.connect("payroll_system.db")
        cursor = conn.cursor()
        tree.delete(*tree.get_children())
        cursor.execute(
            "SELECT * FROM 'TblEmployees' WHERE lastname LIKE ? ORDER BY employee_no",
            (f'%{search_term}%',)
        )
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    list_window = Toplevel()
    list_window.title("Employee`s List")
    list_window.configure(bg='#185C37')
    width = 780
    height = 680
    screen_width = list_window.winfo_screenwidth()
    screen_height = list_window.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    list_window.geometry("%dx%d+%d+%d" % (width, height, x, y))
    list_window.resizable(False, False)

    Main = Frame(list_window, bg='#185C37')
    Main.pack()

    frame1 = LabelFrame(Main, text="", foreground='white', bg='#185C37')
    frame1.grid(row=0, column=0, sticky="news", padx=20, pady=10)

    # Search
    search_label = Label(frame1, text="Search by Lastname :", foreground='white', bg='#185C37')
    search_label.grid(row=0, column=0, sticky="news", padx=20, pady=10)
    search_var.trace("w", search_callback)
    search_entry = Entry(frame1, textvariable=search_var, width=30)
    search_entry.grid(row=0, column=1, padx=10, pady=10)

    TableMargin = Frame(Main)
    TableMargin.grid(row=1, column=0, sticky="news", padx=20, pady=10)

    # TABLES (MAIN)
    scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
    scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
    tree = ttk.Treeview(TableMargin,
                        columns=(
                            "Employee_Id", "Employee_No", "Employee_Name", "Last_Name", "Middle_Name", "Address",
                            "Age", "Contact", "Rate_per_Hour"),
                        height=25, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('Employee_Id', text="Employee Id.", anchor=W)
    tree.heading('Employee_No', text="Employee No.", anchor=W)
    tree.heading('Employee_Name', text="Employee Name", anchor=W)
    tree.heading('Last_Name', text="Last Name", anchor=W)
    tree.heading('Middle_Name', text="Middle Name", anchor=W)
    tree.heading('Address', text="Address", anchor=W)
    tree.heading('Age', text="Age", anchor=W)
    tree.heading('Contact', text="Contact", anchor=W)
    tree.heading('Rate_per_Hour', text="Rate/Hour", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=0)
    tree.column('#2', stretch=NO, minwidth=0, width=90)
    tree.column('#3', stretch=NO, minwidth=0, width=110)
    tree.column('#4', stretch=NO, minwidth=0, width=110)
    tree.column('#5', stretch=NO, minwidth=0, width=80)
    tree.column('#6', stretch=NO, minwidth=0, width=110)
    tree.column('#7', stretch=NO, minwidth=0, width=50)
    tree.column('#8', stretch=NO, minwidth=0, width=100)
    tree.column('#9', stretch=NO, minwidth=0, width=70)
    tree.pack()
    search_callback()

    exit_reg_delete_button = Button(Main, text="Exit", foreground='black', bg='white', command=list_window.destroy,
                                    width=20)
    exit_reg_delete_button.grid(row=2, column=0, padx=20, pady=10)


def menu_registration():
    # Variable
    EMPLOYEE_NO = StringVar()
    FIRSTNAME = StringVar()
    LASTNAME = StringVar()
    MIDDLENAME = StringVar()
    ADDRESS = StringVar()
    AGE = StringVar()
    CONTACT = StringVar()
    RATE_PER_HOUR = StringVar()

    def update_registration():
        if not tree.selection():
            result = tkMessageBox.showwarning('', 'Please Select Something First!', icon="warning")
            return

        if EMPLOYEE_NO.get() == "" or FIRSTNAME.get() == "" or LASTNAME.get() == "" or MIDDLENAME.get() == "" or ADDRESS.get() == "" or AGE.get() == "" or CONTACT.get() == "" or RATE_PER_HOUR.get == "":
            result = tkMessageBox.showwarning('', 'Please Complete The Required Field', icon="warning")
        else:
            try:
                employee_no = int(EMPLOYEE_NO.get())
                firstname = FIRSTNAME.get()
                lastname = LASTNAME.get()
                middlename = MIDDLENAME.get()
                address = ADDRESS.get()
                age = int(AGE.get())
                contact = int(CONTACT.get())
                rate_per_hour = int(RATE_PER_HOUR.get())
            except (ValueError, TypeError):
                result = tkMessageBox.showwarning('', 'Invalid Input', icon="warning")

            else:
                conn = sqlite3.connect("payroll_system.db")
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE TblEmployees SET employee_no=?, firstname=?, lastname=?, middlename=?, address=?, age=?, contact=?, rate_per_hour=? WHERE employee_id = ?",
                    (employee_no, firstname, lastname, middlename, address, age, contact, rate_per_hour, employee_id))

                conn.commit()
                cursor.close()
                conn.close()
                result = tkMessageBox.showinfo("", "Update Successfully!")
                EMPLOYEE_NO.set("")
                FIRSTNAME.set("")
                LASTNAME.set("")
                MIDDLENAME.set("")
                ADDRESS.set("")
                AGE.set("")
                CONTACT.set("")
                RATE_PER_HOUR.set("")
                reg_search_callback()

    def submit_registration():  # sourcery skip: extract-method
        if EMPLOYEE_NO.get() == "" or FIRSTNAME.get() == "" or LASTNAME.get() == "" or MIDDLENAME.get() == "" or ADDRESS.get() == "" or AGE.get() == "" or CONTACT.get() == "" or RATE_PER_HOUR.get == "":
            result = tkMessageBox.showwarning('', 'Please Complete The Required Field', icon="warning")
        else:
            try:
                employee_no = int(EMPLOYEE_NO.get())
                firstname = FIRSTNAME.get()
                lastname = LASTNAME.get()
                middlename = MIDDLENAME.get()
                address = ADDRESS.get()
                age = int(AGE.get())
                contact = int(CONTACT.get())
                rate_per_hour = int(RATE_PER_HOUR.get())
            except (ValueError, TypeError):
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
                RATE_PER_HOUR.set("")
                reg_search_callback()

    def OnSelected(event):
        global employee_id
        curItem = tree.focus()
        contents = (tree.item(curItem))
        selectedItem = contents['values']
        employee_id = selectedItem[0]
        EMPLOYEE_NO.set("")
        FIRSTNAME.set("")
        LASTNAME.set("")
        MIDDLENAME.set("")
        ADDRESS.set("")
        AGE.set("")
        CONTACT.set("")
        RATE_PER_HOUR.set("")
        EMPLOYEE_NO.set(selectedItem[1])
        FIRSTNAME.set(selectedItem[2])
        LASTNAME.set(selectedItem[3])
        MIDDLENAME.set(selectedItem[4])
        ADDRESS.set(selectedItem[5])
        AGE.set(selectedItem[6])
        CONTACT.set(selectedItem[7])
        RATE_PER_HOUR.set(selectedItem[8])

    def ClearField():
        EMPLOYEE_NO.set("")
        FIRSTNAME.set("")
        LASTNAME.set("")
        MIDDLENAME.set("")
        ADDRESS.set("")
        AGE.set("")
        CONTACT.set("")
        RATE_PER_HOUR.set("")

    def deletedata():
        if not tree.selection():
            result = tkMessageBox.showwarning('', 'Please Select Something First!', icon="warning")
        else:
            result = tkMessageBox.askquestion('', 'Are you sure you want to delete this record?', icon="warning")
            if result == 'yes':
                curItem = tree.focus()
                contents = (tree.item(curItem))
                selectedItem = contents['values']
                tree.delete(curItem)
                conn = sqlite3.connect("payroll_system.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM TblEmployees WHERE employee_id = ?", (selectedItem[0],))
                conn.commit()
                cursor.close()
                conn.close()

    reg_window = Toplevel()
    reg_window.title("Employee`s Registration Profile")
    reg_window.configure(bg='#185C37')
    width = 800
    height = 580
    screen_width = reg_window.winfo_screenwidth()
    screen_height = reg_window.winfo_screenheight()
    x = ((screen_width / 2) - 150) - (width / 2)
    y = ((screen_height / 2) + 20) - (height / 2)
    reg_window.geometry("%dx%d+%d+%d" % (width, height, x, y))
    reg_window.resizable(False, False)

    signup_frame = Frame(reg_window, bg='#185C37')
    signup_frame.pack()

    # Saving User Info
    user_info_frame = LabelFrame(signup_frame, text="Registration", foreground='white', bg='#185C37')
    user_info_frame.grid(row=0, column=0, sticky="news", padx=20, pady=10)

    employee_no_label = Label(user_info_frame, text="Employee No :", foreground='white', bg='#185C37')
    employee_no_label.grid(row=0, column=0)
    employee_no_entry = Entry(user_info_frame, textvariable=EMPLOYEE_NO, width=23)
    employee_no_entry.grid(row=0, column=1, padx=10, pady=10)

    first_name_label = Label(user_info_frame, text="First Name :", foreground='white', bg='#185C37')
    first_name_label.grid(row=1, column=0)
    first_name_entry = Entry(user_info_frame, textvariable=FIRSTNAME, width=23)
    first_name_entry.grid(row=1, column=1, padx=10, pady=10)

    last_name_label = Label(user_info_frame, text="Last Name :", foreground='white', bg='#185C37')
    last_name_label.grid(row=1, column=2)
    last_name_entry = Entry(user_info_frame, textvariable=LASTNAME, width=23)
    last_name_entry.grid(row=1, column=3, padx=10, pady=10)

    middle_name_label = Label(user_info_frame, text="Middle Name :", foreground='white', bg='#185C37')
    middle_name_label.grid(row=1, column=4)
    middle_name_entry = Entry(user_info_frame, textvariable=MIDDLENAME, width=23)
    middle_name_entry.grid(row=1, column=5, padx=10, pady=10)

    address_label = Label(user_info_frame, text="Address :", foreground='white', bg='#185C37')
    address_label.grid(row=2, column=0)
    address_entry = Entry(user_info_frame, textvariable=ADDRESS)
    address_entry.grid(row=2, column=1, columnspan=3, sticky="we", padx=10, pady=10)

    age_label = Label(user_info_frame, text="Age :", foreground='white', bg='#185C37')
    age_label.grid(row=2, column=4)
    age_spinbox = Spinbox(user_info_frame, textvariable=AGE, from_=18, to=110, width=21)
    age_spinbox.grid(row=2, column=5, padx=10, pady=10)

    contact_label = Label(user_info_frame, text="Contact :", foreground='white', bg='#185C37')
    contact_label.grid(row=3, column=0)
    contact_entry = Entry(user_info_frame, textvariable=CONTACT)
    contact_entry.grid(row=3, column=1, sticky="we", padx=10, pady=10)

    rate_label = Label(user_info_frame, text="Rate/Hour :", foreground='white', bg='#185C37')
    rate_label.grid(row=4, column=0)
    rate_entry = Entry(user_info_frame, textvariable=RATE_PER_HOUR)
    rate_entry.grid(row=4, column=1, sticky="we", padx=10, pady=10)

    # BUTTON
    reg_button_info_frame = LabelFrame(signup_frame, text="", foreground='white', bg='#185C37')
    reg_button_info_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

    reg_clear_button = Button(reg_button_info_frame, text="Clear Field", foreground='black', bg='white',
                              command=ClearField, width=20)
    reg_clear_button.grid(row=0, column=0, sticky="news", pady=10, padx=20)
    reg_confirm_button = Button(reg_button_info_frame, text="Register", foreground='black', bg='white',
                                command=submit_registration, width=20)
    reg_confirm_button.grid(row=0, column=1, sticky="news", pady=10, padx=20)

    reg_update_button = Button(reg_button_info_frame, text="Update", foreground='black', bg='white',
                               command=update_registration, width=20)
    reg_update_button.grid(row=0, column=2, sticky="news", pady=10, padx=20)

    reg_delete_button = Button(reg_button_info_frame, text="Delete", foreground='black', bg='white', command=deletedata,
                               width=20)
    reg_delete_button.grid(row=0, column=3, sticky="news", pady=10, padx=20)

    # Search

    reg_search_var = StringVar()

    def reg_search_callback(*args):
        search_term = reg_search_var.get()
        conn = sqlite3.connect("payroll_system.db")
        cursor = conn.cursor()
        tree.delete(*tree.get_children())
        cursor.execute(
            "SELECT * FROM 'TblEmployees' WHERE lastname LIKE ? ORDER BY employee_no",
            (f'%{search_term}%',)
        )
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    search_info_frame = LabelFrame(signup_frame, text="", foreground='white', bg='#185C37')
    search_info_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)

    reg_search_label = Label(search_info_frame, text="Search by Lastname :", foreground='white', bg='#185C37')
    reg_search_label.grid(row=0, column=0, padx=20, pady=10)
    reg_search_var.trace("w", reg_search_callback)
    reg_search_entry = Entry(search_info_frame, textvariable=reg_search_var, width=30)
    reg_search_entry.grid(row=0, column=1, padx=10, pady=10)

    TableMargin = Frame(signup_frame)
    TableMargin.grid(row=4, column=0, sticky="news", padx=20, pady=10)

    # TABLES (MAIN)
    scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
    scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
    tree = ttk.Treeview(TableMargin,
                        columns=(
                            "Employee_Id", "Employee_No", "Employee_Name", "Last_Name", "Middle_Name", "Address",
                            "Age", "Contact", "Rate_per_Hour"), height=5, selectmode="extended",
                        yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('Employee_Id', text="Employee Id.", anchor=W)
    tree.heading('Employee_No', text="Employee No.", anchor=W)
    tree.heading('Employee_Name', text="Employee Name", anchor=W)
    tree.heading('Last_Name', text="Last Name", anchor=W)
    tree.heading('Middle_Name', text="Middle Name", anchor=W)
    tree.heading('Address', text="Address", anchor=W)
    tree.heading('Age', text="Age", anchor=W)
    tree.heading('Contact', text="Contact", anchor=W)
    tree.heading('Rate_per_Hour', text="Rate/Hour", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=0)
    tree.column('#2', stretch=NO, minwidth=0, width=90)
    tree.column('#3', stretch=NO, minwidth=0, width=110)
    tree.column('#4', stretch=NO, minwidth=0, width=110)
    tree.column('#5', stretch=NO, minwidth=0, width=80)
    tree.column('#6', stretch=NO, minwidth=0, width=110)
    tree.column('#7', stretch=NO, minwidth=0, width=50)
    tree.column('#8', stretch=NO, minwidth=0, width=100)
    tree.column('#9', stretch=NO, minwidth=0, width=90)
    tree.pack()
    tree.bind('<Double-Button-1>', OnSelected)
    reg_search_callback()

    exit_reg_delete_button = Button(signup_frame, text="Exit", foreground='black', bg='white',
                                    command=reg_window.destroy, width=20)
    exit_reg_delete_button.grid(row=5, column=0, padx=20, pady=10)


def main_menu():  # sourcery skip: extract-duplicate-method
    main_window = Tk()
    main_window.title("Payroll Management System")
    main_window.configure(bg='#185C37')
    width = 640
    height = 480
    screen_width = main_window.winfo_screenwidth()
    screen_height = main_window.winfo_screenheight()
    x = ((screen_width / 2) + 600) - (width / 2)
    y = ((screen_height / 2) + 20) - (height / 2)
    main_window.geometry("%dx%d+%d+%d" % (width, height, x, y))
    main_window.resizable(False, False)

    menubar = Menu(main_window)

    menu_file = Menu(menubar, bg='white', activebackground='#185C37', tearoff=0)
    menubar.add_cascade(label="System Task", menu=menu_file)
    menu_file.add_command(label="Employee`s Registration Profile", command=menu_registration)
    menu_file.add_command(label="Employee`s List", command=menu_list)
    menu_file.add_separator()
    menu_file.add_command(label="Exit", command=main_window.destroy)

    menu_edit = Menu(menubar, bg='white', activebackground='#185C37', tearoff=0)
    menubar.add_cascade(label="System Maintenance", menu=menu_edit)
    menu_edit.add_command(label="Password Management", command=menu_password_management)
    menu_edit.add_command(label="Login Password", command=login)

    menu_help = Menu(menubar, bg='white', activebackground='#185C37', tearoff=0)
    menubar.add_cascade(label="Help", menu=menu_help)
    menu_help.add_command(label="About", command="")

    main_window.config(menu=menubar)


def login():
    failure_max = 3

    def check_login(username, password):
        # Connect to the database
        conn = sqlite3.connect("payroll_system.db")
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
            login.destroy()
            main_menu()
        else:
            check_password.failures += 1
            if check_password.failures == failure_max:
                login.destroy()
                raise SystemExit(tkMessageBox.showwarning('', 'Unauthorized login attempt', icon="warning"))
            else:
                login.title('Try again. Attempt')
                result = tkMessageBox.showwarning('', 'Invalid, Account & Password', icon="warning")
                login_user.delete(0, END)
                login_password.delete(0, END)

    check_password.failures = 0

    def checkbox_password():
        if login_password.cget('show') == '':
            login_password.configure(show='*')
        else:
            login_password.configure(show='')

    login = Tk()
    login.title("Payroll Management System")
    width = 330
    height = 200
    screen_width = login.winfo_screenwidth()
    screen_height = login.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    login.geometry("%dx%d+%d+%d" % (width, height, x, y))
    login.resizable(False, False)
    login.config(bg="#185C37")

    frame = Frame(login, bg='#185C37')
    frame.pack()

    parent = LabelFrame(frame, text="Login", foreground='white', bg='#185C37')
    parent.grid(row=0, column=0, sticky="news", padx=10, pady=20)

    login_user = Label(parent, text="Username", foreground='white', bg='#185C37')
    login_user.grid(row=1, column=0)
    login_user = Entry(parent, width=23)
    login_user.grid(row=1, column=1, padx=10, pady=10)

    login_password = Label(parent, text="Password", foreground='white', bg='#185C37')
    login_password.grid(row=2, column=0)
    login_password = Entry(parent, width=23, show="*")
    login_password.grid(row=2, column=1, padx=10, pady=10)

    show_password = Checkbutton(parent, command=checkbox_password, activebackground='#185C37', bg='#185C37')
    show_password.grid(row=2, column=2, sticky="w")

    # Button
    button = Button(frame, text="Login", foreground='#253342', bg='white', command=check_password)
    button.grid(row=1, column=0, sticky="news", padx=10, pady=2)
    login_password.bind('<Return>', enter)

    login.mainloop()


if __name__ == '__main__':
    database()
    login()

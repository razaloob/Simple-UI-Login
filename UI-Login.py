import sqlite3
import tkinter as tk
from tkinter import messagebox
from time import sleep
import re

# Connect to the database
conn = sqlite3.connect("D:\logins.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                    )""")
conn.commit()

logged_in = 0
check_user = ""

class LoginApp(tk.Tk):

    # window propreties
    def __init__(self):
        super().__init__()
        self.attributes("-topmost", 1)
        self.geometry("300x200")
        self.title("Login App")
        self.resizable(False, False)
        
        self.username = tk.StringVar()
        self.password = tk.StringVar()

        self.create_widgets()

    #
    def create_widgets(self):
        tk.Label(self, text="Username").place(x=30, y=20)
        tk.Label(self, text="Password").place(x=30, y=50)

        tk.Entry(self, textvariable=self.username).place(x=110, y=20)
        tk.Entry(self, textvariable=self.password, show="*").place(x=110, y=50)

        tk.Button(self, text="Login", command=self.login).place(x=30, y=100)
        tk.Button(self, text="Signup", command=self.signup).place(x=110, y=100)

    def login(self):
        # Get the user input
        username = self.username.get()
        password = self.password.get()

        # Check if the user input is valid
        if not username or not password:
            messagebox.showerror("Error", "Please enter a username and password.")
            return

        # Check if the username and password exist in the database
        cursor.execute("SELECT * FROM users WHERE user=? AND password=?", (username, password))
        user = cursor.fetchone()
        
        if user:
            messagebox.showinfo("Info", "Welcome, {}!".format(username))
            global logged_in
            logged_in = logged_in + 1
            sleep(2)
            tk.Tk.destroy(self)

        else:
            messagebox.showerror("Error", "Invalid username or password.")

        global check_user
        check_user = username

    def signup(self):
        username = self.username.get()
        password = self.password.get()

        # check if the user input is valid
        if not username or not password:
            messagebox.showerror("Error", "Please enter a username and password.")
            return
        if len(username) < 6:
            messagebox.showerror("Error", "Username must be at least 8 characters long.")
            return
            # check that username contains only letters and numbers
        if not re.match("^[a-zA-Z0-9]+$", username):
            messagebox.showerror("Error", "Username can only contain letters and numbers.")
            return
            # check that username doesn't contain only numbers
        if username.isnumeric():
            messagebox.showerror("Error", "Username can't be only numbers.")
            return

        cursor.execute("SELECT * FROM users WHERE user=?", (username,))
        user = cursor.fetchone()
        if user:
            messagebox.showerror("Error", "Username already exists.")
            return

        # insert the new credentials into the database
        cursor.execute("INSERT INTO users (user, password) VALUES (?,?)", (username, password))
        conn.commit()
        # confirm signup
        messagebox.showinfo("Info", "Signup successful! Please login.")


#main loop
if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
    if logged_in != 0 and check_user=="admin":
        print("Admin logged in!")
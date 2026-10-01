import tkinter as tk
from tkinter import messagebox
import re

try:
    import mysql.connector
except ImportError:
    mysql = None

def valid_email(email):
    return re.fullmatch(r"[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", email) is not None

def connect_db():
    return mysql.connector.connect(
        host=host.get(),
        user=user.get(),
        password=password.get(),
        database=database.get()
    )

def add_contact():
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()
    category = category_entry.get().strip()
    notes = notes_entry.get("1.0", tk.END).strip()

    if not name or not valid_email(email):
        messagebox.showerror("Error", "Enter valid name and email")
        return

    try:
        db = connect_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO Contact(name,email,phone,category,notes) VALUES(%s,%s,%s,%s,%s)",
            (name, email, phone, category, notes)
        )
        db.commit()
        db.close()
        messagebox.showinfo("Success", "Record inserted")
        show_contacts()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def show_contacts():
    listbox.delete(0, tk.END)
    try:
        db = connect_db()
        cur = db.cursor()
        cur.execute("SELECT id,name,email,phone,category FROM Contact ORDER BY name")
        for row in cur.fetchall():
            listbox.insert(tk.END, str(row))
        db.close()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def create_table():
    try:
        db = connect_db()
        cur = db.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Contact(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(150) UNIQUE,
            phone VARCHAR(30),
            category VARCHAR(50),
            notes TEXT
        )
        """)
        db.commit()
        db.close()
        messagebox.showinfo("Success", "Table is ready")
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

root = tk.Tk()
root.title("Contact Manager")
root.geometry("700x600")

tk.Label(root, text="Host").pack()
host = tk.Entry(root)
host.pack()

tk.Label(root, text="User").pack()
user = tk.Entry(root)
user.pack()

tk.Label(root, text="Password").pack()
password = tk.Entry(root, show="*")
password.pack()

tk.Label(root, text="Database").pack()
database = tk.Entry(root)
database.pack()

tk.Label(root, text="Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Email").pack()
email_entry = tk.Entry(root)
email_entry.pack()

tk.Label(root, text="Phone").pack()
phone_entry = tk.Entry(root)
phone_entry.pack()

tk.Label(root, text="Category").pack()
category_entry = tk.Entry(root)
category_entry.pack()

tk.Label(root, text="Notes").pack()
notes_entry = tk.Text(root, height=4, width=40)
notes_entry.pack()

tk.Button(root, text="Create Table", command=create_table).pack(pady=5)
tk.Button(root, text="Add Contact", command=add_contact).pack(pady=5)
tk.Button(root, text="Show Contacts", command=show_contacts).pack(pady=5)

listbox = tk.Listbox(root, width=90, height=12)
listbox.pack(pady=10)

root.mainloop()

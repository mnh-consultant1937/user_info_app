import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from db import users_collection
from models import User

# ----------------- Functions -----------------

def add_user():
    username = username_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    info = info_entry.get()

    if not username or not email or not password:
        messagebox.showerror("Error", "Username, Email, and Password are required!")
        return

    user = User(username=username, email=email, password=password, info=info)
    users_collection.insert_one(user.dict())
    messagebox.showinfo("Success", f"User {username} added successfully!")
    refresh_users()
    clear_fields()


def update_user():
    selected = user_list.focus()
    if not selected:
        messagebox.showerror("Error", "Select a user to update!")
        return

    username = user_list.item(selected)['values'][0]
    user = users_collection.find_one({"username": username})
    if not user:
        messagebox.showerror("Error", "User not found!")
        return

    new_email = simpledialog.askstring("Update Email", f"Current: {user['email']}")
    new_password = simpledialog.askstring("Update Password", f"Current: {user['password']}")
    new_info = simpledialog.askstring("Update Info", f"Current: {user.get('info','')}")

    users_collection.update_one(
        {"username": username},
        {"$set": {
            "email": new_email or user['email'],
            "password": new_password or user['password'],
            "info": new_info or user.get('info','')
        }}
    )
    messagebox.showinfo("Success", f"User {username} updated successfully!")
    refresh_users()


def delete_user():
    selected = user_list.focus()
    if not selected:
        messagebox.showerror("Error", "Select a user to delete!")
        return

    username = user_list.item(selected)['values'][0]
    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {username}?")
    if confirm:
        users_collection.delete_one({"username": username})
        messagebox.showinfo("Deleted", f"User {username} deleted successfully!")
        refresh_users()


def refresh_users():
    for i in user_list.get_children():
        user_list.delete(i)
    users = users_collection.find()
    for user in users:
        user_list.insert("", "end", values=(user['username'], user['email'], user.get('info','')))


def clear_fields():
    username_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    info_entry.delete(0, tk.END)

# ----------------- GUI -----------------
root = tk.Tk()
root.title("User Info App")
root.geometry("600x500")

# Form
tk.Label(root, text="Username").grid(row=0, column=0, padx=10, pady=5)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Email").grid(row=1, column=0, padx=10, pady=5)
email_entry = tk.Entry(root)
email_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Password").grid(row=2, column=0, padx=10, pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Other Info").grid(row=3, column=0, padx=10, pady=5)
info_entry = tk.Entry(root)
info_entry.grid(row=3, column=1, padx=10, pady=5)

# Buttons
tk.Button(root, text="Add User", command=add_user, width=15).grid(row=4, column=0, pady=10)
tk.Button(root, text="Update User", command=update_user, width=15).grid(row=4, column=1, pady=10)
tk.Button(root, text="Delete User", command=delete_user, width=15).grid(row=4, column=2, pady=10)
tk.Button(root, text="Clear Fields", command=clear_fields, width=15).grid(row=4, column=3, pady=10)

# User List
user_list = ttk.Treeview(root, columns=("Username", "Email", "Info"), show='headings')
user_list.heading("Username", text="Username")
user_list.heading("Email", text="Email")
user_list.heading("Info", text="Info")
user_list.grid(row=5, column=0, columnspan=4, padx=10, pady=20, sticky="nsew")

refresh_users()
root.mainloop()

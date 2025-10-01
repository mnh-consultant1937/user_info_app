import os
from db import users_collection
from models import User

def git_commit_push(message: str):
    """Automatically commit and push changes to GitHub"""
    os.system("git add .")
    os.system(f'git commit -m "{message}"')
    os.system("git push origin main")

def add_user():
    """Add a new user to the database"""
    print("\nEnter user information:")
    username = input("Username: ")
    email = input("Email: ")
    password = input("Password: ")
    info = input("Other info (optional): ")

    user = User(username=username, email=email, password=password, info=info)
    users_collection.insert_one(user.dict())
    print(f"✅ User {username} saved successfully!")

    git_commit_push(f"Add user {username}")


def view_users():
    """View all users stored in the database"""
    print("\n📋 User List:")
    users = users_collection.find()
    count = 0
    for user in users:
        count += 1
        print(f"{count}. Username: {user['username']}, Email: {user['email']}, Info: {user.get('info', '')}")
    if count == 0:
        print("⚠️ No users found.")


def update_user():
    """Update user details"""
    username = input("\nEnter the username of the user you want to update: ")
    user = users_collection.find_one({"username": username})

    if not user:
        print("❌ User not found.")
        return

    print("Leave field blank to keep current value.")
    new_email = input(f"New email (current: {user['email']}): ") or user['email']
    new_password = input(f"New password (current hidden): ") or user['password']
    new_info = input(f"New info (current: {user.get('info', '')}): ") or user.get('info', '')

    users_collection.update_one(
        {"username": username},
        {"$set": {"email": new_email, "password": new_password, "info": new_info}}
    )
    print(f"✅ User {username} updated successfully!")

    git_commit_push(f"Update user {username}")


def delete_user():
    """Delete a user from the database"""
    username = input("\nEnter the username of the user you want to delete: ")
    result = users_collection.delete_one({"username": username})

    if result.deleted_count > 0:
        print(f"🗑️ User {username} deleted successfully!")
        git_commit_push(f"Delete user {username}")
    else:
        print("❌ User not found.")


def menu():
    """Main menu loop"""
    while True:
        print("\n====== User Info App ======")
        print("1. Add User")
        print("2. View Users")
        print("3. Update User")
        print("4. Delete User")
        print("5. Exit")

        choice = input("Choose an option (1-5): ")

        if choice == "1":
            add_user()
        elif choice == "2":
            view_users()
        elif choice == "3":
            update_user()
        elif choice == "4":
            delete_user()
        elif choice == "5":
            print("👋 Exiting program. Goodbye!")
            break
        else:
            print("❌ Invalid choice, please try again.")


if __name__ == "__main__":
    menu()


import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import os

# CSV file paths
USER_FILE = "users.csv"
STUDENT_FILE = "students.csv"
ACTIVITY_FILE = "activities.csv"
PHOTO_FILE = "photos.csv"

# Ensure CSV files exist
def initialize_files():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["username", "password"])
            writer.writerow(["admin", "admin123"])

    for file_path, headers in [
        (STUDENT_FILE, ["name", "roll_no"]),
        (ACTIVITY_FILE, ["activity"]),
        (PHOTO_FILE, ["photo_path"])
    ]:
        if not os.path.exists(file_path):
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(headers)

initialize_files()

# Functionality for the login page
def toggle_password(entry, button):
    if entry.cget("show") == "*":
        entry.config(show="")
        button.config(text="Hide Password")
    else:
        entry.config(show="*")
        button.config(text="Show Password")

def login():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Login Failed", "Please enter both username and password.")
        return

    try:
        with open(USER_FILE, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username and row["password"] == password:
                    messagebox.showinfo("Login Successful", f"Welcome {username}!")
                    open_dashboard()
                    return
        messagebox.showerror("Login Failed", "Invalid username or password.")
    except FileNotFoundError:
        messagebox.showerror("Error", "User file not found! Please try signing up first.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def sign_up():
    new_username = new_username_entry.get()
    new_password = new_password_entry.get()

    if not new_username or not new_password:
        messagebox.showerror("Sign-Up Failed", "Please fill all fields!")
        return

    try:
        with open(USER_FILE, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == new_username:
                    messagebox.showerror("Sign-Up Failed", "Username already exists!")
                    return
    except FileNotFoundError:
        initialize_files()

    with open(USER_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([new_username, new_password])
    messagebox.showinfo("Sign-Up Successful", "Account created successfully!")
    open_login()

# Open Login Page
def open_login():
    clear_frame()

    tk.Label(root, text="National Service Scheme", font=("Arial", 24, "bold"), bg="#4CAF50", fg="white").pack(pady=20)
    tk.Label(root, text="Login Page", font=("Arial", 18), bg="#4CAF50", fg="white").pack(pady=10)

    global username_entry, password_entry
    tk.Label(root, text="Username", bg="#4CAF50", fg="white").pack()
    username_entry = tk.Entry(root, bg="#f0f0f0", relief="solid")
    username_entry.pack(pady=5)

    tk.Label(root, text="Password", bg="#4CAF50", fg="white").pack()
    password_entry = tk.Entry(root, show="*", bg="#f0f0f0", relief="solid")
    password_entry.pack(pady=5)

    show_password_btn = tk.Button(root, text="Show Password", bg="#2196F3", fg="white", command=lambda: toggle_password(password_entry, show_password_btn))
    show_password_btn.pack(pady=10)

    login_btn = tk.Button(root, text="Login", bg="#4CAF50", fg="white", command=login)
    login_btn.pack(pady=10)

    signup_btn = tk.Button(root, text="Sign Up", bg="#FF9800", fg="white", command=open_sign_up)
    signup_btn.pack(pady=10)

# Open Sign-Up Page
def open_sign_up():
    clear_frame()

    tk.Label(root, text="National Service Scheme", font=("Arial", 24, "bold"), bg="#4CAF50", fg="white").pack(pady=20)
    tk.Label(root, text="Sign-Up Page", font=("Arial", 18), bg="#4CAF50", fg="white").pack(pady=10)

    global new_username_entry, new_password_entry
    tk.Label(root, text="New Username", bg="#4CAF50", fg="white").pack()
    new_username_entry = tk.Entry(root, bg="#f0f0f0", relief="solid")
    new_username_entry.pack(pady=5)

    tk.Label(root, text="New Password", bg="#4CAF50", fg="white").pack()
    new_password_entry = tk.Entry(root, show="*", bg="#f0f0f0", relief="solid")
    new_password_entry.pack(pady=5)

    show_password_btn = tk.Button(root, text="Show Password", bg="#2196F3", fg="white", command=lambda: toggle_password(new_password_entry, show_password_btn))
    show_password_btn.pack(pady=10)

    create_account_btn = tk.Button(root, text="Create Account", bg="#4CAF50", fg="white", command=sign_up)
    create_account_btn.pack(pady=10)

    back_to_login_btn = tk.Button(root, text="Back to Login", bg="#FF9800", fg="white", command=open_login)
    back_to_login_btn.pack(pady=10)

# Open Dashboard
def open_dashboard():
    clear_frame()

    tk.Label(root, text="National Service Scheme", font=("Arial", 24, "bold"), bg="#4CAF50", fg="white").pack(pady=20)
    tk.Label(root, text="NSS Camp Dashboard", font=("Arial", 18), bg="#4CAF50", fg="white").pack(pady=20)

    ttk.Button(root, text="Student Details", command=manage_students).pack(pady=10)
    ttk.Button(root, text="Activities", command=manage_activities).pack(pady=10)
    ttk.Button(root, text="Photos", command=manage_photos).pack(pady=10)
    ttk.Button(root, text="Logout", command=open_login).pack(pady=10)

# Manage Photos Page
def manage_photos():
    clear_frame()

    tk.Label(root, text="National Service Scheme", font=("Arial", 24, "bold"), bg="#4CAF50", fg="white").pack(pady=20)
    tk.Label(root, text="Manage Photos", font=("Arial", 18), bg="#4CAF50", fg="white").pack(pady=20)

    def upload_photo():
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            with open(PHOTO_FILE, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([file_path])
            messagebox.showinfo("Upload Successful", "Photo uploaded successfully!")

    def view_photos():
        with open(PHOTO_FILE, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            photo_window = tk.Toplevel(root)
            photo_window.title("Camp Photos")
            for row in reader:
                photo_frame = tk.Frame(photo_window)
                photo_frame.pack(pady=5)
                tk.Label(photo_frame, text=os.path.basename(row[0])).pack(side="left")
                tk.Button(photo_frame, text="Open", bg="#4CAF50", fg="white", command=lambda path=row[0]: os.startfile(path)).pack(side="right")

    ttk.Button(root, text="Upload Photo", command=upload_photo).pack(pady=10)
    ttk.Button(root, text="View Photos", command=view_photos).pack(pady=10)
    ttk.Button(root, text="Back to Dashboard", command=open_dashboard).pack(pady=10)

# Manage Activities Page
def manage_activities():
    clear_frame()

    tk.Label(root, text="National Service Scheme", font=("Arial", 24, "bold"), bg="#4CAF50", fg="white").pack(pady=20)
    tk.Label(root, text="Manage Activities", font=("Arial", 18), bg="#4CAF50", fg="white").pack(pady=20)

    def add_activity():
        activity = activity_entry.get()
        if activity:
            with open(ACTIVITY_FILE, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([activity])
            messagebox.showinfo("Success", "Activity added successfully!")
            activity_entry.delete(0, tk.END)

    def view_activities():
        with open(ACTIVITY_FILE, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            activity_window = tk.Toplevel(root)
            activity_window.title("Camp Activities")
            for row in reader:
                tk.Label(activity_window, text=row[0]).pack()

    tk.Label(root, text="Activity", bg="#4CAF50", fg="white").pack()
    activity_entry = tk.Entry(root, bg="#f0f0f0", relief="solid")
    activity_entry.pack(pady=5)

    ttk.Button(root, text="Add Activity", command=add_activity).pack(pady=10)
    ttk.Button(root, text="View Activities", command=view_activities).pack(pady=10)
    ttk.Button(root, text="Back to Dashboard", command=open_dashboard).pack(pady=10)

# Manage Student Details Page
def manage_students():
    clear_frame()

    tk.Label(root, text="National Service Scheme", font=("Arial", 24, "bold"), bg="#4CAF50", fg="white").pack(pady=20)
    tk.Label(root, text="Manage Student Details", font=("Arial", 18), bg="#4CAF50", fg="white").pack(pady=20)

    def add_student():
        name = student_name_entry.get()
        roll_no = student_roll_entry.get()
        if name and roll_no:
            with open(STUDENT_FILE, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([name, roll_no])
            messagebox.showinfo("Success", "Student added successfully!")
            student_name_entry.delete(0, tk.END)
            student_roll_entry.delete(0, tk.END)

    def view_students():
        with open(STUDENT_FILE, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            student_window = tk.Toplevel(root)
            student_window.title("Student Details")
            for row in reader:
                tk.Label(student_window, text=f"Name: {row[0]}, Roll No: {row[1]}").pack()

    tk.Label(root, text="Student Name", bg="#4CAF50", fg="white").pack()
    student_name_entry = tk.Entry(root, bg="#f0f0f0", relief="solid")
    student_name_entry.pack(pady=5)

    tk.Label(root, text="Roll Number", bg="#4CAF50", fg="white").pack()
    student_roll_entry = tk.Entry(root, bg="#f0f0f0", relief="solid")
    student_roll_entry.pack(pady=5)

    ttk.Button(root, text="Add Student", command=add_student).pack(pady=10)
    ttk.Button(root, text="View Students", command=view_students).pack(pady=10)
    ttk.Button(root, text="Back to Dashboard", command=open_dashboard).pack(pady=10)

# Clear current frame content
def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

# Main Application
root = tk.Tk()
root.title("NSS Camp Management")
root.geometry("400x500")
root.configure(bg="#4CAF50")

open_login()

root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
from client import Client
from activite import Activite
import database


class SportCenterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sport Center")
        self.geometry("400x300")
        self.current_user = None  

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.initialize_ui()

    def initialize_ui(self):
        """Initialize the UI with buttons to access different functionalities."""
        ttk.Label(self.main_frame, text="Welcome to the Sport Center!", font=("Arial", 16)).pack(pady=20)
        ttk.Button(self.main_frame, text="Login", command=self.show_login_window).pack(fill=tk.X, padx=50, pady=5)
        ttk.Button(self.main_frame, text="Register User", command=self.register_user).pack(fill=tk.X, padx=50, pady=5)
        ttk.Button(self.main_frame, text="Sign Up for Activity", command=self.sign_up_for_activity).pack(fill=tk.X, padx=50, pady=5)
        ttk.Button(self.main_frame, text="Make Payment", command=self.make_payment).pack(fill=tk.X, padx=50, pady=5)

    def show_login_window(self):
        login_win = tk.Toplevel(self)
        login_win.title("Login")

        ttk.Label(login_win, text="Username:").grid(row=0, column=0, padx=10, pady=10)
        username_entry = ttk.Entry(login_win)
        username_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(login_win, text="Password:").grid(row=1, column=0, padx=10, pady=10)
        password_entry = ttk.Entry(login_win, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(login_win, text="Login", command=lambda: self.verify_login(
            username_entry.get(), password_entry.get(), login_win)).grid(row=2, column=0, columnspan=2, pady=10)

    def verify_login(self, username, password, window):
        user_id = Client.verify_user(username, password)
        if user_id:
            self.current_user = Client(user_id=user_id)  
            window.destroy()
            messagebox.showinfo("Login Success", "You are now logged in.")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def register_user(self):
        """Open a new window to register a new user."""
        reg_win = tk.Toplevel(self)
        reg_win.title("Register User")

        ttk.Label(reg_win, text="Username:").grid(row=0, column=0, padx=10, pady=10)
        username_entry = ttk.Entry(reg_win)
        username_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(reg_win, text="Password:").grid(row=1, column=0, padx=10, pady=10)
        password_entry = ttk.Entry(reg_win, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(reg_win, text="Email:").grid(row=2, column=0, padx=10, pady=10)
        email_entry = ttk.Entry(reg_win)
        email_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(reg_win, text="Role:").grid(row=3, column=0, padx=10, pady=10)
        role_combo = ttk.Combobox(reg_win, values=["member", "instructor", "admin"])
        role_combo.grid(row=3, column=1, padx=10, pady=10)
        role_combo.current(0)  

        ttk.Button(reg_win, text="Register", command=lambda: self.submit_registration(
            username_entry.get(),
            password_entry.get(),
            email_entry.get(),
            role_combo.get(),
            reg_win)).grid(row=4, column=0, columnspan=2, pady=10)

    def submit_registration(self, username, password, email, role, window):
        """Submit the user registration details to the database."""
        if not username or not password or not email or not role:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            database.add_user(username, password, email, role)
            window.destroy()
            messagebox.showinfo("Success", "User registered successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to register user. Error: {e}")

    def sign_up_for_activity(self):
        activity_win = tk.Toplevel(self)
        activity_win.title("Sign Up for Activity")

        ttk.Label(activity_win, text="Choose an activity:").grid(row=0, column=0, padx=10, pady=10)
        activities = Activite.get_activities()
        activity_names = [activity[1] for activity in activities]
        selected_activity = tk.StringVar()
        activity_combo = ttk.Combobox(activity_win, textvariable=selected_activity, values=activity_names)
        activity_combo.grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(activity_win, text="Sign Up", command=lambda: self.submit_activity_signup(
            activities[activity_names.index(selected_activity.get())][0], activity_win)).grid(row=1, column=0, columnspan=2, pady=10)

    def submit_activity_signup(self, activity_id, window):
        if self.current_user:
            self.current_user.register_activity(activity_id)
            messagebox.showinfo("Success", "Successfully signed up for the activity.")
            window.destroy()
        else:
            messagebox.showerror("Error", "You must be logged in to sign up for an activity.")

    def make_payment(self):
        messagebox.showinfo("Make Payment", "Payment functionality goes here.")

if __name__ == "__main__":
    app = SportCenterApp()
    app.mainloop()

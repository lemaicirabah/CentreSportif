import tkinter as tk
from tkinter import ttk, messagebox
from client import Client
from activite import Activities
from accueil import Accueil
import database


class SportCenterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sport Center")
        self.geometry("400x300")
        self.current_user = None
        self.configure(bg='#333333')
        self.main_frame = ttk.Frame(self)
        style = ttk.Style(self)
        style.configure('My.TFrame', background='#333333')
        self.main_frame = ttk.Frame(self, style='My.TFrame')
        self.main_frame.pack()
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        style = ttk.Style()
        style.configure('My.TButton', font=('Helvetica', 12, 'bold'), padding=10)

        self.initialize_ui()

    def initialize_ui(self):
        style = ttk.Style(self)
        style.configure('My.TLabel', background='#333333', foreground='#FFFFFF')
        ttk.Label(self.main_frame, style='My.TLabel', text="Welcome to the Sport Center!", font=("Arial", 16)).grid(
            row=0, column=0, pady=20)
        ttk.Button(self.main_frame, text="Login", command=self.show_login_window, style="My.TButton").grid(
            sticky="news", row=1, column=0, padx=50, pady=5)
        ttk.Button(self.main_frame, text="Register User", command=self.register_user, style="My.TButton").grid(
            sticky="news", row=2, column=0, padx=50, pady=5)


    def show_login_window(self):
        login_win = tk.Toplevel(self)
        Frame = ttk.Frame(login_win)
        login_win.title("Login")
        ttk.Label(Frame, text="Login", font=("Arial", 20)).grid(row=0, column=1, padx=10, pady=10)
        login_win.geometry("600x600")

        ttk.Label(Frame, text="Username:", font=("Arial", 16)).grid(row=1, column=0, padx=10, pady=10)
        username_entry = ttk.Entry(Frame, font=("Arial", 16))
        username_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(Frame, text="Password:", font=("Arial", 16)).grid(row=2, column=0, padx=10, pady=10)
        password_entry = ttk.Entry(Frame, show="*", font=("Arial", 16))
        password_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Button(Frame, text="Login", command=lambda: self.verify_login(
            username_entry.get(), password_entry.get(), login_win, self), style="My.TButton").grid(row=3, column=1,
                                                                                                   columnspan=2,
                                                                                                   pady=10)
        Frame.pack()

    def verify_login(self, username, password, window, window1):
        user_id = Client.verify_user(username, password)
        if user_id:
            self.current_user = Client(master=None,
                                       user_id=user_id)  # Passer None ou une instance appropriée à la place de `None`
            window.destroy()
            messagebox.showinfo("Login Success", "You are now logged in.")
            Accueil.open_main_window(self,user_id)  # Ouvrir la fenêtre principale après le login réussi
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

    
    def make_payment(self):
        pass  # Cette méthode reste inchangée

    def logout(self):
        self.main_app_window.withdraw()
        self.deiconify()
        self.current_user = None

if __name__ == "__main__":
    database.initialize_db()
    app = SportCenterApp()
    app.mainloop()

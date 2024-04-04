import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *
from client import Client
from accueil import Accueil
import database

class SportCenterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sport Center")
        self.iconbitmap('icon.ico')
        self.geometry('400x500')
        self.resizable(width=False, height=False)

        self.main_frame = ttk.Frame(self, style='My.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        original_image = tk.PhotoImage(file='gradient.png')
        resized_image = original_image.subsample(4)
        self.bg_label = tk.Label(self.main_frame, image=resized_image)
        self.bg_label.image = resized_image
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        style = ttk.Style(self)
        style.configure('My.TLabel', background='#30c7cb', foreground='#000000')
        style.configure('My.TButton', font=('Arial', 12, 'bold'), padding=10, foreground='#000000',
                        background='black', width='8')

        self.initialize_ui()

    def initialize_ui(self):

        welcome_label = ttk.Label(self.main_frame, style='My.TLabel', text="Welcome to the Sport Center!",
                                  font=("Arial", 22))
        welcome_label.grid(row=0, column=0, pady=0, padx=10, sticky="EW")
        welcome_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER, width=400)

        login_button = ttk.Button(self.main_frame, text="Login", command=self.show_login_window, style="My.TButton")
        login_button.grid(row=1, column=0, padx=10, pady=10,  sticky="EW")
        login_button.place(relx=0.5, rely=0.3, anchor=tk.CENTER, width=200)

        register_button = ttk.Button(self.main_frame, text="Register User", command=self.register_user,
                                     style="My.TButton")
        register_button.grid(sticky="EW", row=2, column=0, padx=10, pady=10)
        register_button.place(relx=0.5, rely=0.45, anchor=tk.CENTER, width=200)

    def show_login_window(self):
        login_win = tk.Toplevel(self)
        login_win.title("Login")
        login_win.geometry("400x500")
        login_win.resizable(width=False, height=False)
        login_win.iconbitmap('icon.ico')

        original_image = tk.PhotoImage(file='gradient.png')
        resized_image = original_image.subsample(4)

        bg_label = tk.Label(login_win, image=resized_image)
        bg_label.image = resized_image
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        title = ttk.Label(bg_label, style="My.TLabel", text="Enter your username\nand password to log in", font=("Arial", 16))
        title.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        ttk.Label(bg_label, text="Username:", font=("Arial", 14)).place(relx=0.15, rely=0.3, anchor=tk.CENTER)

        username_entry = ttk.Entry(bg_label, font=("Arial", 14))
        username_entry.place(relx=0.55, rely=0.3, anchor=tk.CENTER)

        ttk.Label(bg_label, text="Password:", font=("Arial", 14)).place(relx=0.15, rely=0.4, anchor=tk.CENTER)
        password_entry = ttk.Entry(bg_label, show="*", font=("Arial", 14))
        password_entry.place(relx=0.55, rely=0.4, anchor=tk.CENTER)
        ttk.Button(bg_label, text="Login", command=lambda: self.verify_login(
            username_entry.get(), password_entry.get(), login_win, self), style="My.TButton").place(relx=0.5, rely=0.5,
                                                                                                    anchor=tk.CENTER)

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

    def logout(self):
        self.main_app_window.withdraw()
        self.deiconify()
        self.current_user = None

if __name__ == "__main__":
    database.initialize_db()
    app = SportCenterApp()
    app.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
from accueil import Accueil
from client import Client
import database

def submit_registration(username, password, email, role, window):
    if not username or not password or not email or not role:
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        database.add_user(username, password, email, role)
        window.destroy()
        messagebox.showinfo("Success", "User registered successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to register user. Error: {e}")


class SportCenterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sport Center")
        self.iconbitmap('icon.ico')
        self.geometry('400x500')
        self.resizable(width=False, height=False)

        self.main_frame = ttk.Frame(self, style='My.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        style = ttk.Style(self)
        style.configure('My.TFrame', background="#332c7a")
        style.configure('My.TLabel', background="#332c7a", foreground='#FFFFFF')
        style.map('My.TLabel', background=[('active', '!disabled', 'SystemHighlight')])

        style.configure('My.TButton', font=('Arial', 12, 'bold'), padding=10, foreground='#000000',
                        background="#332c7a")

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
        login_win.configure(background="#332c7a")

        title = ttk.Label(login_win, style="My.TLabel", text="Enter your username\nand password to log in",
                          font=("Arial", 16))
        title.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        ttk.Label(login_win, text="Username:", font=("Arial", 14)).place(relx=0.15, rely=0.3, anchor=tk.CENTER)

        username_entry = ttk.Entry(login_win, font=("Arial", 14))
        username_entry.place(relx=0.55, rely=0.3, anchor=tk.CENTER)

        ttk.Label(login_win, text="Password:", font=("Arial", 14)).place(relx=0.15, rely=0.4, anchor=tk.CENTER)
        password_entry = ttk.Entry(login_win, show="*", font=("Arial", 14))
        password_entry.place(relx=0.55, rely=0.4, anchor=tk.CENTER)
        ttk.Button(login_win, text="Login", command=lambda: self.verify_login(
            username_entry.get(), password_entry.get(), login_win, self), style="My.TButton").place(relx=0.5, rely=0.5,
                                                                                                    anchor=tk.CENTER)

    def verify_login(self, username, password, window, window1):
        user_id = Client.verify_user(username, password)
        if user_id:
            self.current_user = Client(master=None,
                                       user_id=user_id,
                                       nom=None,
                                       adresse=None,
                                       courriel=None,
                                       n_telephone=None)
            window.destroy()
            messagebox.showinfo("Login Success", "You are now logged in.")
            Accueil.open_main_window(self, user_id,
                                     nom=None,
                                     adresse=None,
                                     courriel=None,
                                     n_telephone=None)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def register_user(self):
        reg_win = tk.Toplevel(self)
        reg_win.title("Register User")
        reg_win.iconbitmap('icon.ico')
        reg_win.geometry('400x500')
        reg_win.resizable(width=False, height=False)
        reg_win.configure(background="#332c7a")

        title = ttk.Label(reg_win, style="My.TLabel", text="all fields below are required",
                          font=("Arial", 12))
        title.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(reg_win, style="My.TLabel", text="Username:").grid(row=2, column=0, padx=10, pady=10)
        username_entry = ttk.Entry(reg_win, font=("Arial", 14), width=20)
        username_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(reg_win, style="My.TLabel", text="Password:").grid(row=3, column=0, padx=10, pady=10)
        password_entry = ttk.Entry(reg_win, font=("Arial", 14), width=20)
        password_entry.grid(row=3, column=1, padx=10, pady=10)

        ttk.Label(reg_win,style="My.TLabel", text="Email:").grid(row=4, column=0, padx=10, pady=10)
        email_entry = ttk.Entry(reg_win, font=("Arial", 14), width=20)
        email_entry.grid(row=4, column=1, padx=10, pady=10)

        ttk.Label(reg_win,style="My.TLabel", text="Role:").grid(row=5, column=0, padx=10, pady=10)
        role_combo = ttk.Combobox(reg_win, values=["member", "instructor", "admin"], font=("arial", 14), width=19)
        role_combo.grid(row=5, column=1, padx=10, pady=10)
        role_combo.current(0)

        ttk.Label(reg_win,style="My.TLabel", text="").grid(row=6, column=0, padx=10)

        ttk.Button(reg_win, style="My.TButton", text="Register", command=lambda: submit_registration(
            username_entry.get(),
            password_entry.get(),
            email_entry.get(),
            role_combo.get(),
            reg_win), width=10).grid(row=6, column=1, pady=10)

        ttk.Label(reg_win, style="My.TLabel", text="").grid(row=6, column=2, padx=10)

    def logout(self):
        self.main_app_window.withdraw()
        self.deiconify()
        self.current_user = None


if __name__ == "__main__":
    database.initialize_db()
    app = SportCenterApp()
    app.mainloop()
import tkinter as tk
from tkinter import  NW
from tkinter import ttk, messagebox
from client import Client
from Profil import open_profile_window
import database

class SportCenterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sport Center")
        self.geometry("500x300")
        self.current_user = None

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.open_main_window()

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
            self.open_main_window()  # Ouvrir la fenêtre principale après le login réussi
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
        pass  # Cette méthode reste inchangée

    def open_main_window(self):
        #self = tk.Toplevel(self)
        #main_app_window.title("Centre Sportif")
        #main_app_window.config(bg="gray30")
        #main_app_window.geometry("400x600")
        #main_app_window.resizable(False, False)
        # Chargez les images
        navIcon = tk.PhotoImage(file='images/menu.png')
        closeIcon = tk.PhotoImage(file='images/close.png')
        fontImage = tk.PhotoImage(file='images/font.png')
        # Note: Pour éviter le garbage collection sur les images, attachez-les à la fenêtre
        self.navIcon = navIcon
        self.closeIcon = closeIcon
        self.fontImage = fontImage

        ttk.Label(self.main_frame, text="Welcome to the Sport Center!", font=("Arial", 16)).pack(pady=20)
        ttk.Button(self.main_frame, text="Login", command=self.show_login_window).pack(fill=tk.X, padx=50, pady=5)
        ttk.Button(self.main_frame, text="Register User", command=self.register_user).pack(fill=tk.X, padx=50, pady=5)
        ttk.Button(self.main_frame, text="Sign Up for Activity", command=self.sign_up_for_activity).pack(fill=tk.X, padx=50, pady=5)
        ttk.Button(self.main_frame, text="Make Payment", command=self.make_payment).pack(fill=tk.X, padx=50, pady=5)

        self.setup_nav_bar()

    def setup_nav_bar(self):
        btnState = False

        def switch_nav():
            nonlocal btnState
            if btnState:
                navLateral.place(x=-300, y=0)
                btnState = False
            else:
                navLateral.place(x=0, y=0)
                btnState = True

        topFrame = tk.Frame(self, bg="#800080")
        topFrame.pack(side="top", fill=tk.X)

        navBarBtn = tk.Button(topFrame, image=self.navIcon, bg="#800080", bd=0, activebackground="#800080", command=switch_nav)
        navBarBtn.place(x=10, y=10)

        navLateral = tk.Frame(self, bg="gray30", width=300, height=600)
        navLateral.place(x=-300, y=0)

        # Dynamically create nav options
        nav_options = {
            "Login": self.show_login_window,
            "Register User": self.register_user,
            "Sign Up for Activity": self.sign_up_for_activity,
            "Make Payment": self.make_payment,
            "Open Profile": lambda: open_profile_window(self.current_user)  # Assuming open_profile_window can accept the current user as an argument
        }

        y = 80
        for option, command in nav_options.items():
            tk.Button(navLateral, text=option, font="ExtraCondensed 16", bg="gray30", fg="white",
                      activebackground="gray30", bd=0, command=command).place(x=25, y=y)
            y += 40

        closeBtn = tk.Button(navLateral, image=self.closeIcon, bg="gray30", bd=0, activebackground="gray30", command=switch_nav)
        closeBtn.place(x=250, y=10)


        accueilText = tk.Label(topFrame, font="ExtraCondensed 15", bg="#800080", height=2, padx=20)
        accueilText.pack(side="right")

        can = tk.Canvas(self, width=400, height=600)#main_app_window
        can.pack()

        BannerText = tk.Label(self, text="Centre Sportif", font="ExtraCondensed 25", bg="#E6E8E9",
                              fg="#800080")#main_app_window
        BannerText.place(x=50, y=550)

        navBarBtn = tk.Button(topFrame, image=self.navIcon, bg="#800080", bd=0, activebackground="#800080",
                              command=switch_nav)
        navBarBtn.place(x=10, y=10)

        navLateral = tk.Frame(self, bg="gray30", width=300, height=600)#main_app_window
        navLateral.place(x=-300, y=0)

        y = 80
        options = ["ACCUEIL", "PAGES", "PROFIL", "PARAMETRES", "AIDE"]
        for i, option in enumerate(options):
            if option == "PROFIL":
                tk.Button(navLateral, text=option, font="ExtraCondensed 16", bg="gray30", fg="white",
                          activebackground="gray30", bd=0, command=open_profile_window).place(x=0, y=y)
            else:
                tk.Button(navLateral, text=option, font="ExtraCondensed 16", bg="gray30", fg="white",
                          activebackground="gray30", bd=0).place(x=0, y=y)
            y += 40

        fermeBtn = tk.Button(navLateral, image=self.closeIcon, bg="gray30", bd=0, activebackground="gray30",
                             command=switch_nav)
        fermeBtn.place(x=250, y=10)

if __name__ == "__main__":
    database.initialize_db()
    app = SportCenterApp()
    app.mainloop()
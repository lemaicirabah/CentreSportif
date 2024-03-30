import tkinter as tk
from tkinter import  NW
from tkinter import ttk, messagebox, PhotoImage
from client import Client
from Profil import open_profile_window
import database
import os

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
        """Initialise l'UI avec des boutons pour accéder aux différentes fonctionnalités."""
        style = ttk.Style(self)
        style.configure('My.TLabel', background='#333333',foreground='#FFFFFF')
        ttk.Label(self.main_frame, style='My.TLabel',text="Welcome to the Sport Center!", font=("Arial", 16)).grid(row=0, column=0, pady=20)
        ttk.Button(self.main_frame , text="Login", command=self.show_login_window, style="My.TButton").grid(sticky="news", row=1, column=0, padx=50, pady=5)
        ttk.Button(self.main_frame, text="Register User", command=self.register_user, style="My.TButton").grid(sticky="news",row=2, column=0, padx=50, pady=5)
        ttk.Button(self.main_frame,text="Sign Up for Activity", command=self.sign_up_for_activity, style="My.TButton").grid(sticky="news",row=3, column=0, padx=50, pady=5)
        ttk.Button(self.main_frame, text="Make Payment", command=self.make_payment, style="My.TButton").grid(sticky="news",row=4, column=0, padx=50, pady=5)



    def show_login_window(self):
        login_win = tk.Toplevel(self)
        Frame = ttk.Frame(login_win)
        login_win.title("Login")
        ttk.Label(Frame, text="Login", font=("Arial", 20)).grid(row=0, column=1, padx=10, pady=10)
        login_win.geometry("600x600")

        ttk.Label(Frame, text="Username:", font=("Arial",16)).grid(row=1, column=0, padx=10, pady=10)
        username_entry = ttk.Entry(Frame,font=("Arial",16))
        username_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(Frame, text="Password:", font=("Arial", 16)).grid(row=2, column=0, padx=10, pady=10)
        password_entry = ttk.Entry(Frame, show="*",font=("Arial",16))
        password_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Button(Frame, text="Login", command=lambda: self.verify_login(
            username_entry.get(), password_entry.get(), login_win,self), style="My.TButton").grid(row=3, column=1, columnspan=2, pady=10)
        
        Frame.pack()

    def verify_login(self, username, password, window,window1):
        user_id = Client.verify_user(username, password)
        if user_id:
            self.current_user = Client(user_id=user_id)
            window.destroy()
            messagebox.showinfo("Login Success", "You are now logged in.")
            self.open_main_window(window1)  # Ouvrir la fenêtre principale après le login réussi
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

    def logout(self):
        self.main_app_window.withdraw()  
        self.deiconify()  
        self.current_user = None 

    def open_main_window(self,window1):
        # Initialisez la nouvelle fenêtre principale
        self.main_app_window = tk.Toplevel(self)
        window1.withdraw()
        self.main_app_window.title("Centre Sportif")
        self.main_app_window.config(bg="gray30")
        self.main_app_window.geometry("400x600")
        
        script_dir = os.path.dirname(os.path.realpath(__file__))
        images_dir = os.path.join(script_dir, '..', 'images')

        # Now use the constructed path to load images
        navIcon = PhotoImage(file=os.path.join(images_dir, 'menu.png'))
        closeIcon = PhotoImage(file=os.path.join(images_dir, 'close.png'))
        fontImage = PhotoImage(file=os.path.join(images_dir, 'font.png'))

        # Note: Pour éviter le garbage collection sur les images, attachez-les à la fenêtre
        self.main_app_window.navIcon = navIcon
        self.main_app_window.closeIcon = closeIcon
        self.main_app_window.fontImage = fontImage

        btnEtat = False

        def switch():
            nonlocal btnEtat
            if btnEtat:
                for x in range(300):
                    navLateral.place(x=-x, y=0)
                    topFrame.update()
                btnEtat = False
            else:
                for x in range(-300, 0):
                    navLateral.place(x=x, y=0)
                    topFrame.update()
                btnEtat = True

        topFrame = tk.Frame(self.main_app_window, bg="#800080")
        topFrame.pack(side="top", fill=tk.X)

        accueilText = tk.Label(topFrame, font="ExtraCondensed 15", bg="#800080", height=2, padx=20)
        accueilText.pack(side="right")

        can = tk.Canvas(self.main_app_window, width=400, height=600)
        can.create_image(0, 0, anchor=NW, image=fontImage)
        can.pack()

        BannerText = tk.Label(self.main_app_window, text="Centre Sportif", font="ExtraCondensed 25", bg="#E6E8E9",
                              fg="#800080")
        BannerText.place(x=50, y=550)

        navBarBtn = tk.Button(topFrame, image=navIcon, bg="#800080", bd=0, activebackground="#800080",
                              command=switch)
        navBarBtn.place(x=10, y=10)

        navLateral = tk.Frame(self.main_app_window, bg="gray30", width=300, height=600)
        navLateral.place(x=-300, y=0)

        y = 80
        options = ["ACCUEIL", "PAGES", "PROFIL", "PARAMETRES", "AIDE", "DECONNEXION"]
        for i, option in enumerate(options):
            if option == "PROFIL":
                tk.Button(navLateral, text=option, font="ExtraCondensed 16", bg="gray30", fg="white",
                          activebackground="gray30", bd=0, command=open_profile_window).place(x=0, y=y)
            elif option == "DECONNEXION":
                tk.Button(navLateral, text=option, font="ExtraCondensed 16", bg="gray30", fg="white",
                            activebackground="gray30", bd=0, command=self.logout).place(x=0, y=y)
            else:
                tk.Button(navLateral, text=option, font="ExtraCondensed 16", bg="gray30", fg="white",
                        activebackground="gray30", bd=0).place(x=0, y=y)
                y += 40

        fermeBtn = tk.Button(navLateral, image=closeIcon, bg="gray30", bd=0, activebackground="gray30",
                             command=switch)
        fermeBtn.place(x=250, y=10)


    # Assurez-vous que cette partie reste à la fin de votre fichier pour lancer application
if __name__ == "__main__":
    database.initialize_db()
    app = SportCenterApp()
    app.mainloop()


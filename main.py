import tkinter as tk
from tkinter import  NW
from tkinter import ttk, messagebox
from client import Client
from Profil import open_profile_window
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
        """Initialise l'UI avec des boutons pour accéder aux différentes fonctionnalités."""
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
            self.open_main_window()  # Ouvrir la fenêtre principale après le login réussi
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def register_user(self):
        pass  # Cette méthode reste inchangée

    def sign_up_for_activity(self):
        pass  # Cette méthode reste inchangée

    def make_payment(self):
        pass  # Cette méthode reste inchangée

    def open_main_window(self):
        # Initialisez la nouvelle fenêtre principale
        main_app_window = tk.Toplevel(self)
        main_app_window.title("Centre Sportif")
        main_app_window.config(bg="gray30")
        main_app_window.geometry("400x600")
        main_app_window.resizable(False, False)
        # Chargez les images
        navIcon = tk.PhotoImage(file='images/menu.png')
        closeIcon = tk.PhotoImage(file='images/close.png')
        fontImage = tk.PhotoImage(file='images/font.png')
        # Note: Pour éviter le garbage collection sur les images, attachez-les à la fenêtre
        main_app_window.navIcon = navIcon
        main_app_window.closeIcon = closeIcon
        main_app_window.fontImage = fontImage

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

        topFrame = tk.Frame(main_app_window, bg="#800080")
        topFrame.pack(side="top", fill=tk.X)

        accueilText = tk.Label(topFrame, font="ExtraCondensed 15", bg="#800080", height=2, padx=20)
        accueilText.pack(side="right")

        can = tk.Canvas(main_app_window, width=400, height=600)
        can.create_image(0, 0, anchor=NW, image=fontImage)
        can.pack()

        BannerText = tk.Label(main_app_window, text="Centre Sportif", font="ExtraCondensed 25", bg="#E6E8E9",
                              fg="#800080")
        BannerText.place(x=50, y=550)

        navBarBtn = tk.Button(topFrame, image=navIcon, bg="#800080", bd=0, activebackground="#800080",
                              command=switch)
        navBarBtn.place(x=10, y=10)

        navLateral = tk.Frame(main_app_window, bg="gray30", width=300, height=600)
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

        fermeBtn = tk.Button(navLateral, image=closeIcon, bg="gray30", bd=0, activebackground="gray30",
                             command=switch)
        fermeBtn.place(x=250, y=10)

    # Assurez-vous que cette partie reste à la fin de votre fichier pour lancer application
if __name__ == "__main__":
    app = SportCenterApp()
    app.mainloop()
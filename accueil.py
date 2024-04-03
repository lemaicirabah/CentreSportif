import tkinter as tk
from tkinter import NW
from Profil import Profil
from activite import Activities
from client import Client 
from Paiement import Payment
from Facture import Facture


class Accueil:
    def __init__(self, master):
        self.master = master
        self.master.title("Main Window")
        tk.Button(master, text="Open New Window", command=self.open_main_window).pack()


    def open_main_window(self,user_id):
        self.withdraw()
        main_app_window = tk.Toplevel(self.master)
        main_app_window.title("Centre Sportif")
        main_app_window.config(bg="gray30")
        main_app_window.geometry("400x600")
        # Chargez les images
        #navIcon = tk.PhotoImage(file='../images/menu.png')
        #closeIcon = tk.PhotoImage(file='../images/close.png')
        #fontImage = tk.PhotoImage(file='../images/font.png')
        # Note: Pour éviter le garbage collection sur les images, attachez-les à la fenêtre
        #main_app_window.navIcon = navIcon
        #main_app_window.closeIcon = closeIcon
        #main_app_window.fontImage = fontImage
        client_instance = Client(main_app_window,user_id)

        profil = Profil(main_app_window,user_id)

        tk.Label(main_app_window, text="Choisissez une action :").pack(pady=10)
        tk.Button(main_app_window, text="Profil", command=profil.open_profile_window).pack(pady=5)
        tk.Button(main_app_window, text="S'inscrire à une activité", command=client_instance.show_register_interface).pack(pady=5)
        tk.Button(main_app_window, text="Se désinscrire d'une activité", command=client_instance.show_unregister_interface).pack(pady=5)
        payment_instance = Payment(self.master, user_id)
        tk.Button(main_app_window, text="Paiement", command=payment_instance.open_payment_window).pack(pady=5)
        facture_instance = Facture(self.master, user_id)
        tk.Button(main_app_window, text="Facture", command=facture_instance.display_invoice).pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = Accueil(root)
    root.mainloop()
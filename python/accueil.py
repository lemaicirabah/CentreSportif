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

    def open_main_window(self, user_id):
        self.withdraw()
        main_app_window = tk.Toplevel(self.master)
        main_app_window.title("Centre Sportif")
        main_app_window.config(bg="#332c7a")
        main_app_window.geometry("400x500")
        main_app_window.resizable(width=False, height=False)
        client_instance = Client(main_app_window, user_id)

        profil = Profil(main_app_window, user_id)

        title = tk.Label(main_app_window, background="#332c7a", text="Choisissez une action", font=("Arial", 22))
        title.grid(row=0, column=1, pady=0, padx=10, sticky="EW")

        profil_button = tk.Button(main_app_window, text="Edit my profil", command=profil.open_profile_window)
        profil_button.grid(row=1, column=1, pady=10, padx=20, sticky="EW")

        register_button = tk.Button(main_app_window, text="Register for an activity",
                                    command=client_instance.show_register_interface)
        register_button.grid(row=2, column=1, pady=10, padx=10, sticky="EW")

        unsubscribe_button = tk.Button(main_app_window, text="Unsubscribe from an activity",
                                       command=client_instance.show_unregister_interface)
        unsubscribe_button.grid(row=3, column=1, pady=10, padx=10, sticky="EW")

        payment_instance = Payment(self.master, user_id)
        payment_button = tk.Button(main_app_window, text="Payment", command=payment_instance.open_payment_window)
        payment_button.grid(row=4, column=1, pady=10, padx=10, sticky="EW")

        facture_instance = Facture(self.master, user_id)
        invoice_button = tk.Button(main_app_window, text="View my invoice", command=facture_instance.display_invoice)
        invoice_button.grid(row=5, column=1, pady=10, padx=10, sticky="EW")
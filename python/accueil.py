import tkinter as tk
from Profil import Profil
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

        title = tk.Label(main_app_window, background="#332c7a", text="Choisissez une action", font=("Arial", 22),
                         foreground="#FFFFFF")
        title.grid(row=0, column=1, pady=0, padx=10, sticky="EW")

        profil_button = tk.Button(main_app_window, text="Edit my profil", command=profil.open_profile_window)
        profil_button.grid(row=1, column=1, pady=10, padx=20, sticky="EW")
        profil_button.bind("<Enter>", lambda event, button=profil_button: on_hover(event, button))
        profil_button.bind("<Button-1>", lambda event, button=profil_button: on_click(event, button))
        profil_button.configure(background="#FFFFFF")

        register_button = tk.Button(main_app_window, text="Register for an activity",
                                    command=client_instance.show_register_interface)
        register_button.grid(row=2, column=1, pady=10, padx=20, sticky="EW")
        register_button.bind("<Enter>", lambda event, button=register_button: on_hover(event, button))
        register_button.bind("<Button-1>", lambda event, button=register_button: on_click(event, button))
        register_button.configure(background="#FFFFFF")

        unsubscribe_button = tk.Button(main_app_window, text="Unsubscribe from an activity",
                                       command=client_instance.show_unregister_interface)
        unsubscribe_button.grid(row=3, column=1, pady=10, padx=20, sticky="EW")
        unsubscribe_button.bind("<Enter>", lambda event, button=unsubscribe_button: on_hover(event, button))
        unsubscribe_button.bind("<Button-1>", lambda event, button=unsubscribe_button: on_click(event, button))
        unsubscribe_button.configure(background="#FFFFFF")

        payment_instance = Payment(main_app_window, user_id)
        payment_button = tk.Button(main_app_window, text="Payment", command=payment_instance.open_payment_window)
        payment_button.grid(row=4, column=1, pady=10, padx=20, sticky="EW")
        payment_button.bind("<Enter>", lambda event, button=payment_button: on_hover(event, button))
        payment_button.bind("<Button-1>", lambda event, button=payment_button: on_click(event, button))
        payment_button.configure(background="#FFFFFF")

        facture_instance = Facture(main_app_window, user_id)
        invoice_button = tk.Button(main_app_window, text="View my invoice", command=facture_instance.display_invoice)
        invoice_button.grid(row=5, column=1, pady=10, padx=20, sticky="EW")
        invoice_button.bind("<Enter>", lambda event, button=invoice_button: on_hover(event, button))
        invoice_button.bind("<Button-1>", lambda event, button=invoice_button: on_click(event, button))
        invoice_button.configure(background="#FFFFFF")


def on_hover(event, button):
    button.config(background="#ffff66", foreground="#000000")


def on_click(event, button):
    button.config(background="#FF0000", foreground="#FFFFFF")


def on_button_release(button):
    button.config(background="#FFFFFF", foreground="#000000")

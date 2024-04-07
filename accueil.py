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

    def open_main_window(self, master, nom, prenom, username, user_id, adresse, courriel, n_telephone, role):
        main_app_window = tk.Toplevel(self.master)
        main_app_window.title("Centre Sportif")
        main_app_window.config(bg="#332c7a")
        main_app_window.geometry("400x500")
        main_app_window.iconbitmap('icon.ico')
        main_app_window.resizable(width=False, height=False)

        client_instance = Client(main_app_window, nom, prenom, username, user_id, adresse, courriel, n_telephone, role)

        profil = Profil(main_app_window, user_id)

        title = tk.Label(main_app_window, background="#332c7a", text="Main options | select an action",
                         font=("Arial", 20),
                         foreground="#FFFFFF")
        title.grid(row=0, column=1, pady=0, padx=10, sticky="EW")

        profil_button = tk.Button(main_app_window, text="Edit my profil", command=profil.open_profile_window)
        profil_button.grid(row=1, column=1, pady=10, padx=20, sticky="EW")
        profil_button.bind("<Button-1>", lambda event, button=profil_button: on_click(event, button))
        profil_button.configure(background="#FFFFFF")

        register_button = tk.Button(main_app_window, text="Register for an activity",
                                    command=client_instance.show_register_interface)
        register_button.grid(row=2, column=1, pady=10, padx=20, sticky="EW")
        register_button.bind("<Button-1>", lambda event, button=register_button: on_click(event, button))
        register_button.configure(background="#FFFFFF")

        unsubscribe_button = tk.Button(main_app_window, text="Unsubscribe from an activity",
                                       command=client_instance.show_unregister_interface)
        unsubscribe_button.grid(row=3, column=1, pady=10, padx=20, sticky="EW")
        unsubscribe_button.bind("<Button-1>", lambda event, button=unsubscribe_button: on_click(event, button))
        unsubscribe_button.configure(background="#FFFFFF")

        personal_schedule = tk.Button(main_app_window, text="consult my personal schedule",
                                      command=client_instance.show_personal_schedule)
        personal_schedule.grid(row=4, column=1, pady=10, padx=20, sticky="EW")
        personal_schedule.bind("<Button-1>", lambda event, button=personal_schedule: on_click(event, button))
        personal_schedule.configure(background="#FFFFFF")

        facture_instance = Facture(main_app_window, user_id)
        invoice_button = tk.Button(main_app_window, text="View my invoice", command=facture_instance.display_invoice)
        invoice_button.grid(row=5, column=1, pady=10, padx=20, sticky="EW")
        invoice_button.bind("<Button-1>", lambda event, button=invoice_button: on_click(event, button))
        invoice_button.configure(background="#FFFFFF")

        payment_instance = Payment(main_app_window, user_id)
        payment_button = tk.Button(main_app_window, text="pay my bill", command=payment_instance.open_payment_window)
        payment_button.grid(row=6, column=1, pady=10, padx=20, sticky="EW")
        payment_button.bind("<Button-1>", lambda event, button=payment_button: on_click(event, button))
        payment_button.configure(background="#FFFFFF")

        logout_label = tk.Label(main_app_window, text="To log out\nplease close the main window", bg="#332c7a",
                                fg="yellow", font=("Verdana", 14))
        logout_label.grid(row=9, column=1, pady=10, padx=20, sticky="EW")


def on_click(event, button):
    button.config(background="#FF0000", foreground="#FFFFFF")


def on_button_release(button):
    button.config(background="#FFFFFF", foreground="#000000")

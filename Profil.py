import tkinter as tk

def open_profile_window():
    # Création de la nouvelle fenêtre
    profile_window = tk.Toplevel()
    profile_window.title("Profil")
    profile_window.geometry("300x200")
    profile_window.config(bg="lightgray")

    # Ajout d'un texte ou d'autres widgets selon les besoins
    tk.Label(profile_window, text="Voici la fenêtre de profil", bg="lightgray").pack(pady=20)

    # Affichage de la fenêtre
    profile_window.mainloop()

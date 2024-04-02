import tkinter as tk
from tkinter import ttk, messagebox
from database import execute_query
from activite import Activities

class Client:
    def __init__(self, master, user_id):
        self.master = master
        self.user_id = user_id


        self.activities = Activities.get_activities()
        self.activities_names = [activity[1] for activity in self.activities]

        self.activity_var = tk.StringVar()


    @staticmethod
    def verify_user(username, password):
        query = "SELECT user_id FROM users WHERE username=? AND password=?"
        user = execute_query(query, (username, password)).fetchone()
        return user[0] if user else None
    

    def show_register_interface(self):
        # Création d'une nouvelle fenêtre Toplevel pour l'inscription
        self.register_window = tk.Toplevel(self.master)
        self.register_window.title("Inscription à une activité")

        tk.Label(self.register_window, text="Choisissez une activité pour vous inscrire:").pack(pady=10)

        # Utilisation de self.activities et self.activities_names déjà récupérés
        self.activity_var_register = tk.StringVar(
            self.register_window)  # Création d'une nouvelle instance de StringVar pour cette interface
        self.combobox_activities_register = ttk.Combobox(self.register_window, textvariable=self.activity_var_register,
                                                         values=self.activities_names)
        self.combobox_activities_register.pack(pady=5)

        tk.Button(self.register_window, text="S'inscrire", command=self.register_activity_from_register_interface).pack(
            pady=10)

    def register_activity_from_register_interface(self):
        selected_activity_name = self.activity_var_register.get()
        selected_activity_id = [activity[0] for activity in self.activities if activity[1] == selected_activity_name][0]

        # Assurez-vous que la requête d'insertion correspond à la structure de votre base de données
        query = "INSERT INTO activity_groups (activity_id, user_id) VALUES (?, ?)"
        execute_query(query, (selected_activity_id, self.user_id))

        tk.messagebox.showinfo("Inscription réussie", f"Vous êtes inscrit à l'activité: {selected_activity_name}")
        self.register_window.destroy()  # Fermeture de la fenêtre d'inscription après succès

    def show_unregister_interface(self):
        self.unregister_window = tk.Toplevel(self.master)
        self.unregister_window.title("Se désinscrire d'une activité")

        self.registered_activities = self.get_registered_activities()
        if not self.registered_activities:
            tk.Label(self.unregister_window, text="Aucune activité inscrite.").pack(pady=10)
            return

        self.activity_listbox = tk.Listbox(self.unregister_window)
        self.activity_listbox.pack(pady=10)

        for activity in self.registered_activities:
            activity_str = f"{activity[1]}"
            if len(activity) > 2:
                activity_str += f" ({activity[2]}"
                if len(activity) > 3:
                    activity_str += f" - {activity[3]}"
                activity_str += ")"
            self.activity_listbox.insert(tk.END, activity_str)

        tk.Button(self.unregister_window, text="Se désinscrire", command=self.unregister_activity).pack(pady=5)

    def get_registered_activities(self):
        # Méthode pour récupérer les activités auxquelles l'utilisateur est inscrit
        query = "SELECT ag.group_id, a.name FROM activity_groups ag JOIN activities a ON ag.activity_id = a.activity_id WHERE ag.user_id = ?"
        return execute_query(query, (self.user_id,)).fetchall()

    def unregister_activity(self):
        # Méthode pour se désinscrire d'une activité sélectionnée
        selected_index = self.activity_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Sélectionnez une activité",
                                   "Veuillez sélectionner une activité pour vous désinscrire.")
            return

        group_id = self.registered_activities[selected_index[0]][0]
        query = "DELETE FROM activity_groups WHERE group_id = ?"
        execute_query(query, (group_id,))

        self.show_unregister_interface()  # Mise à jour de l'interface de désinscription
        messagebox.showinfo("Désinscription réussie", "Vous avez été désinscrit de l'activité.")

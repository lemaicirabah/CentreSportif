import tkinter as tk
from tkinter import ttk, messagebox
from database import execute_query
from activite import Activities


class Client:
    def __init__(self, master, nom, prenom, username, user_id, adresse, courriel, n_telephone, role):
        self.master = master
        self.nom = nom
        self.prenom = prenom
        self.username = username
        self.user_id = user_id
        self.adresse = adresse
        self.courriel = courriel
        self.n_telephone = n_telephone
        self.role = role

        self.activities = Activities.get_activities()
        self.activities_names = list(set(activity[1] for activity in self.activities))

        self.activity_var = tk.StringVar()

    @staticmethod
    def verify_user(courriel, password):
        query = "SELECT user_id FROM users WHERE courriel=? AND password=?"
        user = execute_query(query, (courriel, password)).fetchone()
        return user[0] if user else None

    def show_register_interface(self):
        self.register_window = tk.Toplevel(self.master)
        self.register_window.title("Inscription à une activité")
        self.register_window.geometry('400x300')

        self.register_window.configure(background="#332c7a")

        title = tk.Label(self.register_window, background="#332c7a", foreground="#FFFFFF", font="Arial(12)",
                         text="Choisissez une activité pour vous inscrire:")
        title.grid(row=0, column=0, pady=0, padx=10, sticky="EW")
        title.place(relx=0.5, rely=0.05, anchor=tk.CENTER, width=400)

        self.activity_var_register = tk.StringVar(self.register_window)
        self.combobox_activities_register = ttk.Combobox(self.register_window, textvariable=self.activity_var_register,
                                                         values=self.activities_names)
        self.combobox_activities_register.grid(row=1, column=0, pady=10, padx=20, sticky="EW")
        self.combobox_activities_register.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        register_button = tk.Button(self.register_window, text="S'inscrire",
                                    command=self.register_activity_from_register_interface)
        register_button.grid(row=2, column=0, pady=0, padx=10, sticky="EW")
        register_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER, width=200)


    def register_activity_from_register_interface(self):
        selected_activity_name = self.activity_var_register.get()
        selected_activity_id = [activity[0] for activity in self.activities if activity[1] == selected_activity_name][0]

        query = "INSERT INTO activity_groups (activity_id, user_id) VALUES (?, ?)"
        execute_query(query, (selected_activity_id, self.user_id))

        tk.messagebox.showinfo("Inscription réussie", f"Vous êtes inscrit à l'activité: {selected_activity_name}")
        self.register_window.destroy()

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
        query = "SELECT ag.group_id, a.name FROM activity_groups ag JOIN activities a ON ag.activity_id = a.activity_id WHERE ag.user_id = ?"
        return execute_query(query, (self.user_id,)).fetchall()

    def unregister_activity(self):
        selected_index = self.activity_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Sélectionnez une activité",
                                   "Veuillez sélectionner une activité pour vous désinscrire.")
            return

        group_id = self.registered_activities[selected_index[0]][0]
        query = "DELETE FROM activity_groups WHERE group_id = ?"
        execute_query(query, (group_id,))

        self.show_unregister_interface()
        messagebox.showinfo("Désinscription réussie", "Vous avez été désinscrit de l'activité.")

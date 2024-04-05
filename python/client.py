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
        self.activities_names = [activity[0] for activity in self.activities]

        self.activity_var = tk.StringVar()

    @staticmethod
    def verify_user(username, password):
        query = "SELECT user_id FROM users WHERE username=? AND password=?"
        user = execute_query(query, (username, password)).fetchone()
        return user[0] if user else None

    def show_register_interface(self):
        self.register_window = tk.Toplevel(self.master)
        self.register_window.title("Registration for an activity")
        self.register_window.geometry('400x300')

        self.register_window.configure(background="#332c7a")

        title = tk.Label(self.register_window, background="#332c7a", foreground="#FFFFFF", font="Arial(12)",
                         text="Choose an activity to register:")
        title.grid(row=0, column=0, pady=0, padx=10, sticky="EW")
        title.place(relx=0.5, rely=0.05, anchor=tk.CENTER, width=400)

        self.activity_var_register = tk.StringVar(self.register_window)
        self.combobox_activities_register = ttk.Combobox(self.register_window, textvariable=self.activity_var_register,
                                                         values=self.activities_names)
        self.combobox_activities_register.grid(row=1, column=0, pady=10, padx=20, sticky="EW")
        self.combobox_activities_register.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        register_button = tk.Button(self.register_window, text="Register",
                                    command=self.register_activity_from_register_interface)
        register_button.grid(row=2, column=0, pady=0, padx=10, sticky="EW")
        register_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER, width=200)

    def register_activity_from_register_interface(self):
        selected_activity_name = self.activity_var_register.get()

        selected_activity_info = None
        for activity in self.activities:
            if activity[0] == selected_activity_name:
                selected_activity_info = activity
                break
        print(selected_activity_info)

        query = ("INSERT INTO activity_groups (user_id, activity_name, jour, start_time, end_time, group_id) "
                 "VALUES (?, ?, ?, ?, ?, '1')")
        execute_query(query, (self.user_id, selected_activity_info[0], selected_activity_info[2],
                              selected_activity_info[3], selected_activity_info[4]))

        tk.messagebox.showinfo("successful registration", f"You are registered for the activity: {selected_activity_name}")
        self.register_window.destroy()

    def show_unregister_interface(self):
        unregister_window = tk.Toplevel(self.master)
        unregister_window.title("Unsubscribe")
        unregister_window.iconbitmap('icon.ico')
        unregister_window.geometry('400x300')
        unregister_window.resizable(width=False, height=False)
        unregister_window.configure(background="#332c7a")

        registered_activities = self.get_registered_activities()

        if not registered_activities:
            tk.Label(unregister_window, text="Aucune activité inscrite.").pack(pady=10)
            return

        activity_listbox = tk.Listbox(unregister_window)
        activity_listbox.pack(pady=10)

        for activity in registered_activities:
            activity_str = f"{activity[1]}"
            if len(activity) > 2:
                activity_str += f" ({activity[2]}"
                if len(activity) > 3:
                    activity_str += f" - {activity[3]}"
                activity_str += ")"
            activity_listbox.insert(tk.END, activity_str)

        tk.Button(unregister_window, text="Unsubscribe", command=self.unregister_activity).pack(pady=5)

    def get_registered_activities(self):
        query = ("SELECT * FROM activity_groups ag JOIN activities a ON ag.activity_name = a.activity_name "
                 "WHERE ag.user_id = ?")
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

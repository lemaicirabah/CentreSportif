import tkinter as tk
from tkinter import ttk, messagebox
from database import execute_query
from activite import Activities


class Client:
    def __init__(self, master, nom, prenom, username, user_id, adresse, courriel, n_telephone, role):
        self.unregister_window = None
        self.selected_activity_name = None
        self.activity_listbox = None
        self.activity_var_register = None
        self.register_window = None
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

        self.activity_var_register = tk.StringVar()
        combobox_activities_register = ttk.Combobox(self.register_window, textvariable=self.activity_var_register,
                                                    values=self.activities_names)

        combobox_activities_register.grid(row=1, column=0, pady=10, padx=20, sticky="EW")
        combobox_activities_register.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

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

        query = ("INSERT INTO activity_groups (user_id, activity_name, jour, start_time, end_time, group_id) "
                 "VALUES (?, ?, ?, ?, ?, '1')")
        execute_query(query, (self.user_id, selected_activity_info[0], selected_activity_info[2],
                              selected_activity_info[3], selected_activity_info[4]))

        tk.messagebox.showinfo("successful registration", f"You are registered for the activity: {selected_activity_name}")
        self.register_window.destroy()

    def show_unregister_interface(self):
        self.unregister_window = tk.Toplevel(self.master)
        self.unregister_window.title("Unsubscribe")
        self.unregister_window.iconbitmap('icon.ico')
        self.unregister_window.geometry('400x300')
        self.unregister_window.resizable(width=False, height=False)
        self.unregister_window.configure(background="#332c7a")

        self.activity_listbox = tk.Listbox(self.unregister_window, background="#332c7a", foreground="#FFFFFF",
                                           font=("Arial", 12))
        self.activity_listbox.grid(row=0, column=1, padx=10, pady=10)

        registered_activities = self.get_registered_activities()

        if not registered_activities:
            no_activities_label = ttk.Label(self.unregister_window, background="#332c7a", foreground="#FFFFFF",
                                            text="you are not registered for any activity", font=("Arial", 12))
            no_activities_label.grid(row=0, column=1, padx=10, pady=10)
            return

        for activity in registered_activities:
            activity_str = f"{activity[0]} - {activity[2]}"
            self.activity_listbox.insert(tk.END, activity_str)

        unregister_button = tk.Button(self.unregister_window, text="Unsubscribe",
                                      command=lambda: self.handle_unsubscribe())
        unregister_button.grid(row=1, column=0, padx=10, pady=10, sticky="EW")

    def get_registered_activities(self):
        query = ("SELECT * FROM activity_groups ag JOIN activities a ON ag.activity_name = a.activity_name "
                 "WHERE ag.user_id = ?")
        return execute_query(query, (self.user_id,)).fetchall()

    def handle_unsubscribe(self):
        selected_index = self.activity_listbox.curselection()
        if selected_index:
            selected_activity = self.activity_listbox.get(selected_index[0])
            print(selected_activity)
            activity_name = selected_activity.split(" - ")[1]
            self.unregister_activity(self.user_id, activity_name)

    def unregister_activity(self, user_id, activity_name):
        print("USER_ID", user_id, "ACTIVITY_NAME", activity_name)
        query = "DELETE FROM activity_groups WHERE user_id = ? AND activity_name = ?"
        execute_query(query, (user_id, activity_name))

        selected_index = self.activity_listbox.curselection()
        if selected_index:
            self.activity_listbox.delete(selected_index)

        messagebox.showinfo("Unsubscribe done !", "You have been unsubscribed from the activity.")
        self.unregister_window.destroy()


import tkinter as tk
from tkinter import ttk, messagebox
from database import execute_query
from activite import Activities


class Client:
    def __init__(self, master, nom, prenom, username, user_id, adresse, courriel, n_telephone, role):
        self.schedule_window = None
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
        self.register_window.iconbitmap('icon.ico')
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
        query = ("INSERT INTO registrations (user_id, group_id, activity_name, status)"
                 "VALUES (?, '1', ?, 'INCOMPLET')")
        execute_query(query, (self.user_id, selected_activity_info[0]))

        query = ("INSERT INTO invoice (user_id, activity_name, monthly_amount, invoice_date)"
                 "VALUES(?, ?, ?, '2024-04-05' )")

        execute_query(query, (self.user_id, selected_activity_info[0], selected_activity_info[5]))

        tk.messagebox.showinfo("successful registration",
                               f"You are registered for the activity: {selected_activity_name}")
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
        self.activity_listbox.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=400)

        registered_activities = self.get_registered_activities()

        if not registered_activities:
            no_activities_label = ttk.Label(self.unregister_window, background="#332c7a", foreground="#FFFFFF",
                                            text="no activity in your list \U0001F611", font=("Arial", 14))
            no_activities_label.grid(row=0, column=1, padx=10, pady=10)
            no_activities_label.place(relx=0.7, rely=0.5, anchor=tk.CENTER, width=400)

            return

        for activity in registered_activities:
            activity_str = f"{activity[0]} - {activity[2]}"
            self.activity_listbox.insert(tk.END, activity_str)

        unregister_button = tk.Button(self.unregister_window, text="Unsubscribe",
                                      command=lambda: self.handle_unsubscribe())
        unregister_button.grid(row=1, column=0, padx=10, pady=10, sticky="EW")

    def show_personal_schedule(self):
        self.schedule_window = tk.Toplevel(self.master)
        self.schedule_window.title("Scheduling")
        self.schedule_window.iconbitmap('icon.ico')
        self.schedule_window.geometry('400x300')
        self.schedule_window.resizable(width=False, height=False)
        self.schedule_window.configure(background="#332c7a")
        registered_activities = self.get_registered_activities()

        self.schedule_listbox = tk.Listbox(self.schedule_window, background="#332c7a", foreground="#FFFFFF",
                                           font=("Arial", 12))
        self.schedule_listbox.grid(row=0, column=1, padx=10, pady=10)
        self.schedule_listbox.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=400)

        if not registered_activities:
            no_schedule_label = ttk.Label(self.unregister_window, background="#332c7a", foreground="#FFFFFF",
                                          text="You are not registered\n in any activity \U0001F611",
                                          font=("Arial", 14))
            no_schedule_label.grid(row=0, column=1, padx=10, pady=10)
            no_schedule_label.place(relx=0.7, rely=0.5, anchor=tk.CENTER, width=400)

            return
        self.schedule_listbox.insert(0, "{:25} {:10} {:15} {:15}".format("Activity name", "Day", "Start time",
                                                                         "End time"))
        self.schedule_listbox.insert(1, "")
        for activity in registered_activities:
            self.schedule_listbox.insert(tk.END,
                                         "{:25} {:10} {:15} {:15}".format(activity[2], activity[3], activity[4],
                                                                          activity[5]))

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
        query = "DELETE FROM activity_groups WHERE user_id = ? AND activity_name = ?"
        execute_query(query, (user_id, activity_name))
        query = "DELETE FROM registrations WHERE user_id = ? AND activity_name = ?"
        execute_query(query, (user_id, activity_name))

        query = "DELETE FROM invoice WHERE user_id = ? AND activity_name = ?"
        execute_query(query, (user_id, activity_name))

        selected_index = self.activity_listbox.curselection()
        if selected_index:
            self.activity_listbox.delete(selected_index)

        messagebox.showinfo("Unsubscribe done !", "You have been unsubscribed from the activity.")
        self.unregister_window.destroy()

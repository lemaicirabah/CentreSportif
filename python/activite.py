from database import execute_query, get_activities
import tkinter as tk
from tkinter import ttk, messagebox


class Activities:
    def __init__(self, client, activity_id, activity_name, jour, start_time, end_time):
        self.client = client
        self.activity_id = activity_id
        self.activity_name = activity_name
        self.jour = jour
        self.start_time = start_time
        self.end_time = end_time


    def open_activite_window():
        activite_window = tk.Toplevel()
        activite_window.title("Profil")
        activite_window.geometry("300x200")
        activite_window.config(bg="lightgray")

        # Ajout d'un texte ou d'autres widgets selon les besoins
        user_id = 1  # Exemple, vous devrez remplacer cela par l'ID réel de l'utilisateur connecté

        # Initialisation de l'interface d'inscription à une activité

    @staticmethod
    def get_activities():
        query = "SELECT activity_name, description, jour, start_time, end_time FROM activities"
        activities = execute_query(query).fetchall()
        return activities

    @staticmethod
    def get_activity_by_name(self, activity_name):
        query = "SELECT * FROM activities WHERE activity_name = ?"
        activity = execute_query(query, (activity_name,)).fetchone()
        if activity:
            return activity
        else:
            return None

    @staticmethod
    def insert_activities(activities_to_insert):
        query = "INSERT INTO activities (activity_name, description, min_participants, max_participants) VALUES (?, ?, ?, ?)"
        execute_query(query, activities_to_insert)

    def sign_up_for_activity(self):
        activity_win = tk.Toplevel(self)
        activity_win.title("Sign Up for Activity")

        ttk.Label(activity_win, text="Choose an activity:").grid(row=0, column=0, padx=10, pady=10)
        activities = get_activities()
        activity_names = [activity[1] for activity in activities]
        selected_activity = tk.StringVar()
        activity_combo = ttk.Combobox(activity_win, textvariable=selected_activity, values=activity_names)
        activity_combo.grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(activity_win, text="Sign Up", command=lambda: self.submit_activity_signup(
            activities[activity_names.index(selected_activity.get())][0], activity_win)).grid(row=1, column=0,
                                                                                              columnspan=2, pady=10)

    def submit_activity_signup(self, activity_id, window):
        if self.client:
            self.client.register_activity(activity_id)
            messagebox.showinfo("Success", "Successfully signed up for the activity.")
            window.destroy()
        else:
            messagebox.showerror("Error", "You must be logged in to sign up for an activity.")

    def register_activity(self):
        selected_activity_name = self.activity_var.get()
        selected_activity_id = [activity[0] for activity in self.activities if activity[1] == selected_activity_name][0]

        query = "INSERT INTO activity_groups (activity_id, user_id) VALUES (?, ?)"
        execute_query(query, (selected_activity_id, self.user_id))

        tk.messagebox.showinfo("Inscription réussie", f"Vous êtes inscrit à l'activité: {selected_activity_name}")

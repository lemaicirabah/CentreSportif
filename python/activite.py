from database import execute_query
import tkinter as tk

from python.client import Client


def open_activite_window():
    # Création de la nouvelle fenêtre
    activite_window = tk.Toplevel()
    activite_window.title("Profil")
    activite_window.geometry("300x200")
    activite_window.config(bg="lightgray")

    # Ajout d'un texte ou d'autres widgets selon les besoins
    user_id = 1  # Exemple, vous devrez remplacer cela par l'ID réel de l'utilisateur connecté

    # Initialisation de l'interface d'inscription à une activité
    Client(activite_window, user_id)

@staticmethod
def get_activities():
        query = "SELECT activity_id, name FROM activities"
        activities = execute_query(query).fetchall()
        return activities

@staticmethod
def insert_activities(activities_to_insert):
        query = "INSERT INTO activities (name, description, min_participants, max_participants) VALUES (?, ?, ?, ?)"
        execute_query(query, activities_to_insert)
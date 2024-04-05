import tkinter as tk
from database import connect_db


class Profil:
    def __init__(self, master, user_id):
        self.master = master
        self.user_id = user_id

    def open_profile_window(self):
        user_info = self.get_user_info()

        # Création de la nouvelle fenêtre
        profile_window = tk.Toplevel(self.master)
        profile_window.title("Profil")
        profile_window.geometry("400x350")
        profile_window.resizable(width=False, height=False)
        profile_window.configure(background="#332c7a")

        title = tk.Label(profile_window, background="#332c7a", foreground="#FFFFFF", text="Your profil",
                         font=("Arial", 20))
        title.grid(row=0, column=2, padx=10, pady=10)
        title.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        if user_info:
            info_text = (f"First name: {user_info['prenom']}\n\nLast name: {user_info['nom']}\n\n"
                         f"Email: {user_info['courriel']}\n\nAddress: {user_info['adresse']}\n\n"
                         f"Phone number: {user_info['telephone']}")
            infos = tk.Label(profile_window, text=info_text, background="#332c7a", foreground="#FFFFFF", font=("Arial", 14))
            infos.grid(row=2, column=2, padx=10, pady=10)
            infos.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

            edit_button = tk.Button(profile_window, text="Modifier", command=self.modify_profile)
            edit_button.grid(row=4, column=2, pady=10)
            edit_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        else:
            tk.Label(profile_window, text="User information not available", bg="lightgray").grid(row=1, column=1,
                                                                                                 padx=10, pady=10)

    def modify_profile(self):
        # New window for profile modification
        mod_window = tk.Toplevel(self.master)
        mod_window.title("Modify Profile")
        mod_window.geometry("300x400")
        mod_window.config(bg="lightgray")

        tk.Label(mod_window, text="Nouveau Nom:", bg="lightgray").pack(pady=(10, 0))
        username_entry = tk.Entry(mod_window)
        username_entry.pack(pady=(0, 20))

        tk.Label(mod_window, text="Nouveau Courriel:", bg="lightgray").pack(pady=(10, 0))
        email_entry = tk.Entry(mod_window)
        email_entry.pack(pady=(0, 20))

        tk.Label(mod_window, text="Confirme Matricule", bg="lightgray").pack(pady=(10, 0))
        pass_entry = tk.Entry(mod_window, show="*")
        pass_entry.pack(pady=(0, 20))

        tk.Label(mod_window, text="Nouvelle Adresse:", bg="lightgray").pack(pady=(10, 0))
        adresse_entry = tk.Entry(mod_window)
        adresse_entry.pack(pady=(0, 20))

        tk.Label(mod_window, text="Nouveau Telephone:", bg="lightgray").pack(pady=(10, 0))
        telephone_entry = tk.Entry(mod_window)
        telephone_entry.pack(pady=(0, 20))

        tk.Button(mod_window, text="Submit",
                  command=lambda: self.submit_modifications(username_entry.get(), email_entry.get(), pass_entry.get(),
                                                            adresse_entry.get(),
                                                            telephone_entry.get(),
                                                            mod_window)).pack(pady=(0, 10))

    def verify_password(self, entered_password, stored_password_hash):
        return entered_password == stored_password_hash

    def submit_modifications(self, new_username, new_email, entered_password,new_adresse,new_telephone, window):
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT matricule FROM users WHERE user_id=?", (self.user_id,))
        current_password_hash = cursor.fetchone()[0]  # Assuming passwords are hashed

        if not self.verify_password(entered_password, current_password_hash):
            tk.messagebox.showerror("Error", "Password incorrect. Identity verification failed.")
            return

        try:
            cursor.execute("UPDATE users SET nom=?, courriel=? , adresse=?, n_telephone=? WHERE user_id=?",
                           (new_username, new_email,new_adresse,new_telephone, self.user_id))
            conn.commit()
            tk.messagebox.showinfo("Success", "Profile updated successfully!")
            window.destroy()  # Close the modification window
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to update profile: {e}")
        finally:
            conn.close()

    def get_user_info(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT prenom, nom, courriel, adresse ,n_telephone FROM users WHERE user_id=?", (self.user_id,))
        user_info = cursor.fetchone()
        conn.close()
        if user_info:
            return {'prenom': user_info[0], 'nom': user_info[1], 'courriel': user_info[2], 'adresse': user_info[3],
                    'telephone': user_info[4]}
        return None
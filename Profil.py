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
        profile_window.iconbitmap('icon.ico')
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
        mod_window.configure(background="#332c7a")

        new_password_label = tk.Label(mod_window, text="New password:", background="#332c7a", foreground="#FFFFFF",
                                      font=("Arial", 14))
        new_password_label.grid(row=0, column=0, pady=5, padx=10, sticky="EW")
        new_password_entry = tk.Entry(mod_window, font=("Arial", 14), highlightcolor="#000000", highlightthickness=2)
        new_password_entry.grid(row=1, column=0, pady=0, padx=10, sticky="EW")

        new_email_label = tk.Label(mod_window, text="New Email:", background="#332c7a", foreground="#FFFFFF",
                                   font=("Arial", 14))
        new_email_label.grid(row=2, column=0, pady=5, padx=10, sticky="EW")
        new_email_entry = tk.Entry(mod_window, font=("Arial", 14), highlightcolor="#000000", highlightthickness=2)
        new_email_entry.grid(row=3, column=0, pady=0, padx=10, sticky="EW")

        new_address_label = tk.Label(mod_window, text="New address:", background="#332c7a", foreground="#FFFFFF",
                                     font=("Arial", 14))
        new_address_label.grid(row=4, column=0, pady=5, padx=10, sticky="EW")
        new_address_entry = tk.Entry(mod_window, font=("Arial", 14), highlightcolor="#000000", highlightthickness=2)
        new_address_entry.grid(row=5, column=0, pady=0, padx=10, sticky="EW")

        new_phone_number_label = tk.Label(mod_window, text="New phone number:", background="#332c7a",
                                          foreground="#FFFFFF", font=("Arial", 14))
        new_phone_number_label.grid(row=6, column=0, pady=5, padx=10, sticky="EW")
        new_phone_number_entry = tk.Entry(mod_window, font=("Arial", 14), highlightcolor="#000000", highlightthickness=2)
        new_phone_number_entry.grid(row=7, column=0, pady=0, padx=10, sticky="EW")

        submit_button = tk.Button(mod_window, text="Submit", command=lambda: self.submit_modifications(
            new_password_entry.get(), new_email_entry.get(), new_address_entry.get(), new_phone_number_entry.get(),
            self.master))
        submit_button.grid(row=8, column=0, pady=15, padx=10, sticky="EW")

    def verify_password(self, entered_password, stored_password_hash):
        return entered_password == stored_password_hash

    def submit_modifications(self, new_password, new_email, new_address, new_phone_number, window):
        conn = connect_db()
        cursor = conn.cursor()

        try:
            update_values = []
            if new_password:
                update_values.append(("password", new_password))
            if new_email:
                update_values.append(("courriel", new_email))
            if new_address:
                update_values.append(("adresse", new_address))
            if new_phone_number:
                update_values.append(("n_telephone", new_phone_number))

            if update_values:
                set_clause = ", ".join([f"{field} = ?" for field, _ in update_values])
                update_query = f"UPDATE users SET {set_clause} WHERE user_id=?"
                params = [value for _, value in update_values]
                params.append(self.user_id)
                cursor.execute(update_query, params)
                conn.commit()
                tk.messagebox.showinfo("Success", "Profile updated successfully!")
            else:
                tk.messagebox.showinfo("Info", "No changes to update.")

            window.destroy()
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
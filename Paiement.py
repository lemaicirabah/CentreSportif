import tkinter as tk
from tkinter import messagebox
import random 
import database

class Payment:
    def __init__(self, master, user_id):
        self.master = master
        self.user_id = user_id

    def open_payment_window(self):
        payment_window = tk.Toplevel(self.master)
        payment_window.title("Payment")
        payment_window.geometry("400x400")
        payment_window.configure(background="#332c7a")

        # Widget: Account Number
        account_number_label = tk.Label(payment_window, text="Account Number:", background="#332c7a",
                                        foreground="#FFFFFF")
        account_number_label.place(relx=0.25, rely=0.05, anchor=tk.CENTER)
        account_entry = tk.Entry(payment_window)
        account_entry.place(relx=0.5, rely=0.1, anchor=tk.CENTER, width=200)

        # Widget: Expiration Date
        expiration_date_label = tk.Label(payment_window, text="Expiration Date (MM/YY):", background="#332c7a",
                                         foreground="#FFFFFF")
        expiration_date_label.place(relx=0.25, rely=0.2, anchor=tk.CENTER)
        expiration_entry = tk.Entry(payment_window)
        expiration_entry.place(relx=0.5, rely=0.25, anchor=tk.CENTER, width=200)

        # Widget: CVV
        cvv_label = tk.Label(payment_window, text="CVV:", background="#332c7a", foreground="#FFFFFF")
        cvv_label.place(relx=0.25, rely=0.35, anchor=tk.CENTER)
        cvv_entry = tk.Entry(payment_window)
        cvv_entry.place(relx=0.5, rely=0.4, anchor=tk.CENTER, width=200)

        # Widget: Amount
        amount_label = tk.Label(payment_window, text="Amount:", background="#332c7a", foreground="#FFFFFF")
        amount_label.place(relx=0.25, rely=0.5, anchor=tk.CENTER)
        amount_entry = tk.Entry(payment_window)
        amount_entry.place(relx=0.5, rely=0.55, anchor=tk.CENTER, width=200)

        submit_button = tk.Button(payment_window, text="Submit", command=lambda: self.generate_invoice(
            account_entry.get(), expiration_entry.get(), cvv_entry.get(), amount_entry.get()))
        submit_button.configure(background="yellow")
        submit_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER, width=100)

        # Centrer les widgets dans la fenêtre
        payment_window.grid_rowconfigure(0, weight=1)
        payment_window.grid_columnconfigure(0, weight=1)

    def generate_invoice(self, account_number, expiration_date, cvv, amount):
        # Simulate saving payment info and generating an invoice number
        invoice_number = self.save_payment_info(account_number, expiration_date, cvv)
        # Prepare invoice details
        invoice_details = (
            f"Invoice Number: {invoice_number}\n"
            f"Account Number: {account_number}\n"
            f"Expiration Date: {expiration_date}\n"
            f"CVV: {cvv}\n"
            "Your payment has been processed, and an invoice has been generated."
        )
        messagebox.showinfo("Invoice Generated", invoice_details)

    def save_payment_info(self, account_number, expiration_date, cvv):
        conn = database.connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO payment_info (user_id, account_number, expiration_date, cvv) VALUES (?, ?, ?, ?)",
                (self.user_id, account_number, expiration_date, cvv)
            )
            conn.commit()
            invoice_number = random.randint(10000, 99999)
            return invoice_number  
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            return None
        finally:
            conn.close()

    def show_invoice_details(self, invoice_number, account_number, expiration_date, cvv):
        invoice_window = tk.Toplevel(self.master)
        invoice_window.title("Invoice Details")
        invoice_window.geometry("400x300")
        invoice_window.config(bg="lightgray")

        tk.Label(invoice_window, text=f"Invoice Number: {invoice_number}", bg="lightgray").pack(pady=10)
        tk.Label(invoice_window, text=f"Account Number: {account_number}", bg="lightgray").pack(pady=10)
        tk.Label(invoice_window, text=f"Expiration Date: {expiration_date}", bg="lightgray").pack(pady=10)
        tk.Label(invoice_window, text=f"CVV: {cvv}", bg="lightgray").pack(pady=10)

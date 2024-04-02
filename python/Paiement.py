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
        payment_window.geometry("300x200")
        payment_window.config(bg="lightgray")

        tk.Label(payment_window, text="Account Number:", bg="lightgray").pack(pady=(10,0))
        account_entry = tk.Entry(payment_window)
        account_entry.pack(pady=(0,10))
        
        tk.Label(payment_window, text="Expiration Date (MM/YY):", bg="lightgray").pack()
        expiration_entry = tk.Entry(payment_window)
        expiration_entry.pack(pady=(0,10))
        
        tk.Label(payment_window, text="CVV:", bg="lightgray").pack()
        cvv_entry = tk.Entry(payment_window)
        cvv_entry.pack(pady=(0,10))

        tk.Button(payment_window, text="Submit", command=lambda: self.generate_invoice(account_entry.get(), expiration_entry.get(), cvv_entry.get())).pack(pady=10)

    def generate_invoice(self, account_number, expiration_date, cvv):
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
            # Simulate generating a unique invoice number (for demonstration purposes)
            invoice_number = random.randint(10000, 99999)
            return invoice_number  # Return the fake invoice number for display
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

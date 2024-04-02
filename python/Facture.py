import tkinter as tk
from tkinter import messagebox
from database import connect_db 

class Facture:
    def __init__(self, master, user_id):
        self.master = master
        self.user_id = user_id

    def display_invoice(self):
        invoice_details = self.fetch_invoice_details()
        if invoice_details:
            invoice_window = tk.Toplevel(self.master)
            invoice_window.title("Invoice Details")
            invoice_window.geometry("400x300")
            invoice_window.config(bg="lightgray")

            for detail in invoice_details:
                tk.Label(invoice_window, text=f"{detail}: {invoice_details[detail]}", bg="lightgray").pack(pady=10)
        else:
            messagebox.showinfo("Info", "No invoice details found.")

    def fetch_invoice_details(self):
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT account_number, amount, paid_at FROM payments WHERE user_id=?", (self.user_id,))
            payment_info = cursor.fetchone()
            if payment_info:
                return {
                    "Account Number": payment_info[0],
                    "Amount Paid": payment_info[1],
                    "Payment Date": payment_info[2]
                }
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred while fetching invoice details: {e}")
            return None
        finally:
            conn.close()

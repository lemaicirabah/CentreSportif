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
            invoice_window.geometry("400x600")
            invoice_window.configure(background="#332c7a")

            for invoice_detail in invoice_details:
                for label_text, value in invoice_detail.items():
                    text = tk.Label(invoice_window, text=f"{label_text}: {value}", background="#332c7a",
                                    foreground="#FFFFFF")
                    text.pack(pady=(5, 0))
                tk.Label(invoice_window, background="#332c7a", text="").pack()
        else:
            messagebox.showinfo("Info", "No invoice details found.")

    def fetch_invoice_details(self):
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT activity_name, monthly_amount, invoice_date FROM invoice WHERE user_id=?",
                           (self.user_id,))
            invoice_info = cursor.fetchall()
            if invoice_info:
                invoice_details = []
                total_amount = 0
                for activity_name, monthly_amount, invoice_date in invoice_info:
                    total_amount += monthly_amount
                    invoice_details.append({
                        "Activity ": activity_name,
                        "Monthly Amount": f"${monthly_amount}",
                        "Invoice Date": invoice_date
                    })

                invoice_details.append({
                    "Total Amount": f"${round(total_amount,2)}"
                })
                return invoice_details
            else:
                return None
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred while fetching invoice details: {e}")
            return None
        finally:
            conn.close()

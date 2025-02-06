import tkinter as tk
import customtkinter as ctk
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict

# Set up CustomTkinter theme
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# Create main app window
root = ctk.CTk()
root.title("Budgeting for College Students")
root.geometry("500x650")  

# File to store budget data
CSV_FILE = "budget_data.csv"

# Ensure CSV file exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Income", "Category", "Expense", "Savings"])  # Headers

# Global variables
expenses = []  # Stores (Category, Amount)
chart_frame = None  # Stores chart reference

# Function to update budget and show pie chart
def update_budget():
    try:
        income = float(income_entry.get())
    except ValueError:
        result_label.configure(text="Error: Enter a valid income amount!", text_color="red")
        return

    total_expenses = sum(expense[1] for expense in expenses)
    savings = income - total_expenses
    
    # Display results
    result_label.configure(text=f"Total Expenses: ₹{total_expenses:.2f}\nSavings: ₹{savings:.2f}", text_color="black")

    # Save data to CSV
    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        for category, amount in expenses:
            writer.writerow([income, category, amount, savings])

    # Show updated pie chart
    show_chart()

# Function to add an expense
def add_expense():
    category = category_entry.get().strip()
    try:
        amount = float(expense_entry.get())
        if category and amount >= 0:
            expenses.append((category, amount))
            update_expense_list()
            category_entry.delete(0, tk.END)
            expense_entry.delete(0, tk.END)
        else:
            result_label.configure(text="Enter valid category and amount!", text_color="red")
    except ValueError:
        result_label.configure(text="Enter a valid expense amount!", text_color="red")

# Function to update the displayed expense list
def update_expense_list():
    expense_listbox.delete(0, tk.END)
    for i, (category, amount) in enumerate(expenses, start=1):
        expense_listbox.insert(tk.END, f"{i}. {category}: ₹{amount:.2f}")

# Function to delete selected expense
def delete_expense():
    try:
        selected_index = expense_listbox.curselection()[0]
        del expenses[selected_index]
        update_expense_list()
    except IndexError:
        result_label.configure(text="Select an expense to delete!", text_color="red")

# Function to show pie chart with category-wise sums
def show_chart():
    global chart_frame  

    if not expenses:
        result_label.configure(text="No expenses to show in the chart!", text_color="red")
        return

    # Aggregate expenses by category
    expense_dict = defaultdict(float)
    for category, amount in expenses:
        expense_dict[category] += amount  

    categories = list(expense_dict.keys())
    amounts = list(expense_dict.values())

    # Remove old chart if it exists
    if chart_frame:
        chart_frame.destroy()

    # Create new frame for chart
    chart_frame = tk.Frame(root)
    chart_frame.pack(pady=10)

    # Create figure
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    ax.set_title("Expense Distribution")

    # Embed chart into Tkinter
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.get_tk_widget().pack()
    canvas.draw()

# UI Components
ctk.CTkLabel(root, text="Enter Monthly Income (₹):").pack(pady=(10, 0))
income_entry = ctk.CTkEntry(root, width=250)
income_entry.pack(pady=5)

# Expense Entry
ctk.CTkLabel(root, text="Enter Expense Category:").pack(pady=(10, 0))
category_entry = ctk.CTkEntry(root, width=250)
category_entry.pack(pady=5)

ctk.CTkLabel(root, text="Enter Expense Amount (₹):").pack(pady=(10, 0))
expense_entry = ctk.CTkEntry(root, width=250)
expense_entry.pack(pady=5)

# Buttons
ctk.CTkButton(root, text="Add Expense", command=add_expense).pack(pady=10)
ctk.CTkButton(root, text="Calculate Budget", command=update_budget).pack(pady=5)

# Expense List
ctk.CTkLabel(root, text="Expense List:").pack(pady=(10, 0))
expense_listbox = tk.Listbox(root, height=6, width=50)
expense_listbox.pack(pady=5)

# Delete Button
ctk.CTkButton(root, text="Delete Selected Expense", command=delete_expense, fg_color="red").pack(pady=5)

# Result Label
result_label = ctk.CTkLabel(root, text="", justify="left")
result_label.pack(pady=10)

# Run GUI
root.mainloop()
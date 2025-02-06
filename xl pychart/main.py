import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt

# Function to load and visualize Excel data
def load_excel():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", ".xlsx;.xls")])
    if not file_path:
        return

    try:
        # Read Excel File
        df = pd.read_excel(file_path)

        # Show column names for selection
        columns = df.columns.tolist()

        # Create new window for visualization options
        vis_window = tk.Toplevel(root)
        vis_window.title("Select Columns for Visualization")
        vis_window.geometry("400x400")

        # Data Preview
        tk.Label(vis_window, text="Data Preview:", font=("Arial", 10, "bold")).pack()
        preview_text = tk.Text(vis_window, height=5, width=50)
        preview_text.pack()
        preview_text.insert(tk.END, df.head().to_string(index=False))  # Show first 5 rows

        # Dropdowns for X and Y axis selection
        tk.Label(vis_window, text="X-axis:", font=("Arial", 10)).pack()
        x_var = tk.StringVar()
        x_dropdown = ttk.Combobox(vis_window, textvariable=x_var, values=columns, state="readonly")
        x_dropdown.pack()

        tk.Label(vis_window, text="Y-axis (Select Multiple):", font=("Arial", 10)).pack()
        y_var = tk.StringVar()
        y_listbox = tk.Listbox(vis_window, selectmode="multiple", height=5)
        for col in columns:
            y_listbox.insert(tk.END, col)
        y_listbox.pack()

        # Function to plot selected data
        def plot_chart(chart_type):
            x_col = x_var.get()
            selected_indices = y_listbox.curselection()
            y_cols = [y_listbox.get(i) for i in selected_indices]

            if not x_col or not y_cols:
                messagebox.showerror("Error", "Please select X and Y columns!")
                return

            plt.figure(figsize=(8, 5))

            if chart_type == "Bar Chart":
                df.plot(x=x_col, y=y_cols, kind="bar", legend=True)
            elif chart_type == "Pie Chart" and len(y_cols) == 1:
                df[y_cols[0]].plot(kind="pie", labels=df[x_col], autopct="%1.1f%%")
            elif chart_type == "Line Chart":
                df.plot(x=x_col, y=y_cols, kind="line", marker="o", linestyle="-", legend=True)
            elif chart_type == "Scatter Plot":
                for y in y_cols:
                    plt.scatter(df[x_col], df[y], label=y)
                plt.legend()
            elif chart_type == "Histogram":
                df[y_cols].plot(kind="hist", alpha=0.7, bins=10, edgecolor="black", legend=True)
            elif chart_type == "Box Plot":
                df[y_cols].plot(kind="box", vert=True, legend=True)

            plt.title(f"{chart_type} of {y_cols} vs {x_col}")
            plt.show()

        # Buttons for different chart types
        btn_frame = tk.Frame(vis_window)
        btn_frame.pack()

        chart_types = ["Bar Chart", "Pie Chart", "Line Chart", "Scatter Plot", "Histogram", "Box Plot"]
        for chart in chart_types:
            tk.Button(btn_frame, text=chart, command=lambda c=chart: plot_chart(c)).pack(side="left", padx=5)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load Excel file: {e}")

# Tkinter UI Setup
root = tk.Tk()
root.title("Excel Data Visualizer")
root.geometry("300x200")

tk.Button(root, text="Upload Excel File", font=("Arial", 12), command=load_excel).pack(pady=20)
root.mainloop()
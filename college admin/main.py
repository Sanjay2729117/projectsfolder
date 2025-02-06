import customtkinter as ctk
from tkinter import messagebox, ttk
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class CollegeAdmissionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("College Admission Seat Management")
        self.root.geometry("800x600")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")  
        
        self.conn = sqlite3.connect("college_admission.db")
        self.cursor = self.conn.cursor()
        self.create_tables()
        
        self.show_login()
    
    def create_tables(self):
        self.cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        """)
        
        self.cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                dob TEXT,
                cutoff REAL,
                community TEXT,
                department TEXT
            )
        """)
        
        self.cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                general_seats INTEGER,
                obc_seats INTEGER,
                sc_seats INTEGER,
                st_seats INTEGER
            )
        """)
        self.conn.commit()
    
    def show_login(self):
        self.clear_window()
        
        self.login_frame = ctk.CTkFrame(self.root)
        self.login_frame.pack(pady=50, padx=50)

        ctk.CTkLabel(self.login_frame, text="Admin Login", font=("Arial", 20, "bold")).pack(pady=10)
        
        ctk.CTkLabel(self.login_frame, text="Username:").pack()
        self.username_entry = ctk.CTkEntry(self.login_frame)
        self.username_entry.pack(pady=5)
        
        ctk.CTkLabel(self.login_frame, text="Password:").pack()
        self.password_entry = ctk.CTkEntry(self.login_frame, show="*")
        self.password_entry.pack(pady=5)
        
        ctk.CTkButton(self.login_frame, text="Login", command=self.login).pack(pady=10)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        self.cursor.execute("SELECT * FROM admin WHERE username=? AND password=?", (username, password))
        admin = self.cursor.fetchone()
        
        if admin:
            messagebox.showinfo("Login Success", "Welcome Admin")
            self.show_main_page()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")
    
    def show_main_page(self):
        self.clear_window()
        
        ctk.CTkLabel(self.root, text="College Admission Management", font=("Arial", 20, "bold")).pack(pady=10)
        
        ctk.CTkButton(self.root, text="Add Student", command=self.add_student).pack(pady=5)
        ctk.CTkButton(self.root, text="View Students", command=self.view_students).pack(pady=5)
        ctk.CTkButton(self.root, text="Manage Departments", command=self.manage_departments).pack(pady=5)
        ctk.CTkButton(self.root, text="Show Remaining Seats", command=self.view_remaining_seats).pack(pady=5)
    
    def add_student(self):
        self.clear_window()
        
        ctk.CTkLabel(self.root, text="Add Student", font=("Arial", 20, "bold")).pack(pady=10)
        
        self.student_name = ctk.CTkEntry(self.root, placeholder_text="Name")
        self.student_name.pack(pady=5)
        
        self.student_dob = ctk.CTkEntry(self.root, placeholder_text="Date of Birth (YYYY-MM-DD)")
        self.student_dob.pack(pady=5)
        
        self.student_cutoff = ctk.CTkEntry(self.root, placeholder_text="Cutoff")
        self.student_cutoff.pack(pady=5)
        
        self.student_community = ctk.CTkComboBox(self.root, values=["General", "OBC", "SC", "ST"])
        self.student_community.pack(pady=5)
        
        self.cursor.execute("SELECT name FROM departments")
        departments = [row[0] for row in self.cursor.fetchall()]
        self.student_department = ctk.CTkComboBox(self.root, values=departments)
        self.student_department.pack(pady=5)
        
        ctk.CTkButton(self.root, text="Submit", command=self.save_student).pack(pady=10)
        ctk.CTkButton(self.root, text="Back", command=self.show_main_page).pack(pady=5)
    
    def save_student(self):
        name = self.student_name.get()
        dob = self.student_dob.get()
        cutoff = self.student_cutoff.get()
        community = self.student_community.get()
        department = self.student_department.get()
        
        if not all([name, dob, cutoff, community, department]):
            messagebox.showerror("Input Error", "All fields are required.")
            return
        
        try:
            cutoff = float(cutoff)
        except ValueError:
            messagebox.showerror("Input Error", "Cutoff must be a number.")
            return
        
        # Reduce seats based on the selected community
        community_column = f"{community.lower()}_seats"
        self.cursor.execute(f"UPDATE departments SET {community_column} = {community_column} - 1 WHERE name=? AND {community_column} > 0", (department,))

        if self.cursor.rowcount == 0:
            messagebox.showerror("Seat Allocation Error", f"No available seats in the {community} community for the selected department.")
            return
        
        self.cursor.execute("INSERT INTO students (name, dob, cutoff, community, department) VALUES (?, ?, ?, ?, ?)",
                            (name, dob, cutoff, community, department))
        self.conn.commit()
        messagebox.showinfo("Success", "Student added successfully!")
        self.show_main_page()

        # Generate PDF after student is added
        self.generate_student_pdf(name, dob, cutoff, community, department)
    
    def generate_student_pdf(self, name, dob, cutoff, community, department):
        pdf_file = f"{name}_admission.pdf"
        c = canvas.Canvas(pdf_file, pagesize=letter)
        c.setFont("Helvetica", 12)
        
        c.drawString(100, 750, f"Student Admission Details")
        c.drawString(100, 730, f"Name: {name}")
        c.drawString(100, 710, f"DOB: {dob}")
        c.drawString(100, 690, f"Cutoff: {cutoff}")
        c.drawString(100, 670, f"Community: {community}")
        c.drawString(100, 650, f"Department: {department}")
        
        c.save()
        messagebox.showinfo("PDF Generated", f"Student PDF saved as {pdf_file}")
    
    def view_students(self):
        self.clear_window()
        ctk.CTkLabel(self.root, text="Student List", font=("Arial", 20, "bold")).pack(pady=10)

        # Filter Options
        self.community_filter = ctk.CTkComboBox(self.root, values=["All", "General", "OBC", "SC", "ST"])
        self.community_filter.pack(pady=5)
        
        self.department_filter = ctk.CTkComboBox(self.root, values=self.get_department_names())
        self.department_filter.pack(pady=5)

        ctk.CTkButton(self.root, text="Filter", command=self.apply_filters).pack(pady=5)

        self.display_student_table()

    def apply_filters(self):
        self.display_student_table()

    def display_student_table(self):
        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=10)

        columns = ("Name", "DOB", "Cutoff", "Community", "Department")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack()

        community = self.community_filter.get()
        department = self.department_filter.get()

        query = "SELECT name, dob, cutoff, community, department FROM students WHERE 1=1"
        params = []

        if community != "All":
            query += " AND community=?"
            params.append(community)
        
        if department:
            query += " AND department=?"
            params.append(department)

        self.cursor.execute(query, params)
        students = self.cursor.fetchall()

        for student in students:
            self.tree.insert("", "end", values=student)

        ctk.CTkButton(self.root, text="Back", command=self.show_main_page).pack(pady=5)
    
    def manage_departments(self):
        self.clear_window()
        ctk.CTkLabel(self.root, text="Manage Departments", font=("Arial", 20, "bold")).pack(pady=10)
        
        ctk.CTkButton(self.root, text="Add Department", command=self.add_department).pack(pady=5)
        ctk.CTkButton(self.root, text="View Departments", command=self.view_departments).pack(pady=5)
        ctk.CTkButton(self.root, text="Back", command=self.show_main_page).pack(pady=5)
    
    def add_department(self):
        self.clear_window()
        ctk.CTkLabel(self.root, text="Add Department", font=("Arial", 20, "bold")).pack(pady=10)
        
        self.department_name = ctk.CTkEntry(self.root, placeholder_text="Department Name")
        self.department_name.pack(pady=5)
        
        self.general_seats = ctk.CTkEntry(self.root, placeholder_text="General Seats")
        self.general_seats.pack(pady=5)
        
        self.obc_seats = ctk.CTkEntry(self.root, placeholder_text="OBC Seats")
        self.obc_seats.pack(pady=5)
        
        self.sc_seats = ctk.CTkEntry(self.root, placeholder_text="SC Seats")
        self.sc_seats.pack(pady=5)
        
        self.st_seats = ctk.CTkEntry(self.root, placeholder_text="ST Seats")
        self.st_seats.pack(pady=5)
        
        ctk.CTkButton(self.root, text="Submit", command=self.save_department).pack(pady=10)
        ctk.CTkButton(self.root, text="Back", command=self.manage_departments).pack(pady=5)
    
    def save_department(self):
        name = self.department_name.get()
        general_seats = self.general_seats.get()
        obc_seats = self.obc_seats.get()
        sc_seats = self.sc_seats.get()
        st_seats = self.st_seats.get()
        if not all([name, general_seats, obc_seats, sc_seats, st_seats]):
            messagebox.showerror("Input Error", "All fields are required.")
            return
        
        try:
            general_seats = int(general_seats)
            obc_seats = int(obc_seats)
            sc_seats = int(sc_seats)
            st_seats = int(st_seats)
        except ValueError:
            messagebox.showerror("Input Error", "Seats must be integers.")
            return
        
        self.cursor.execute("INSERT INTO departments (name, general_seats, obc_seats, sc_seats, st_seats) VALUES (?, ?, ?, ?, ?)",
                            (name, general_seats, obc_seats, sc_seats, st_seats))
        self.conn.commit()
        messagebox.showinfo("Success", "Department added successfully!")
        self.manage_departments()
    
    def view_departments(self):
        self.clear_window()
        ctk.CTkLabel(self.root, text="Department List", font=("Arial", 20, "bold")).pack(pady=10)

        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=10)

        columns = ("Department Name", "General Seats", "OBC Seats", "SC Seats", "ST Seats")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack()

        self.cursor.execute("SELECT name, general_seats, obc_seats, sc_seats, st_seats FROM departments")
        departments = self.cursor.fetchall()

        for department in departments:
            self.tree.insert("", "end", values=department)

        ctk.CTkButton(self.root, text="Back", command=self.manage_departments).pack(pady=5)
    
    def view_remaining_seats(self):
        self.clear_window()
        ctk.CTkLabel(self.root, text="Remaining Seats", font=("Arial", 20, "bold")).pack(pady=10)

        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=10)

        columns = ("Department", "General", "OBC", "SC", "ST")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack()

        self.cursor.execute("SELECT name, general_seats, obc_seats, sc_seats, st_seats FROM departments")
        departments = self.cursor.fetchall()

        for department in departments:
            self.tree.insert("", "end", values=department)

        ctk.CTkButton(self.root, text="Back", command=self.show_main_page).pack(pady=5)
    
    def get_department_names(self):
        self.cursor.execute("SELECT name FROM departments")
        return [row[0] for row in self.cursor.fetchall()]

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Create the main window and start the application
if __name__ == "__main__":
    root = ctk.CTk()
    app = CollegeAdmissionApp(root)
    root.mainloop()

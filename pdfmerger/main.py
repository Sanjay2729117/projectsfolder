from docx import Document
from tkinter import *
from tkinter import filedialog, messagebox
import customtkinter as ct
import pandas as pd
import os
from pikepdf import Pdf

def open_file(filepath):
    """Opens the given file in the default application."""
    if os.path.exists(filepath):
        os.startfile(filepath)  # Windows
    else:
        messagebox.showerror("Error", "File not found!")

def pdf():
    root = ct.CTkToplevel()
    root.grab_set()
    root.title('MULTIPLEXER')
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    root.config(background='#FFB6C1')

    file_list = []
    def file_open():
        filename = filedialog.askopenfilename(title='Select a file', filetypes=[('PDF', '*.pdf')])
        file_list.append(filename)
        ct.CTkLabel(root, text=filename, fg_color='#FFB6C1', text_color='black').place(x=550, y=450 + 20 * len(file_list))

    def file_print():
        if not combine_filename.get():
            messagebox.showerror("Error", "Enter file name!")
        elif len(file_list) < 2:
            messagebox.showerror("Error", "Select at least 2 files to combine!")
        else:
            output_file = combine_filename.get() + '.pdf'
            new_pdf = Pdf.new()
            for file in file_list:
                with Pdf.open(file.strip()) as pdf:
                    new_pdf.pages.extend(pdf.pages)
            new_pdf.save(output_file)
            messagebox.showinfo("Success", f"Merged PDF saved as {output_file}")
            ct.CTkButton(root, text="View PDF", fg_color="#800080", command=lambda: open_file(output_file)).place(x=650, y=500)

    combine_filename = StringVar()
    ct.CTkButton(root, text="Select file", fg_color="#800080", command=file_open).place(x=650, y=250)
    ct.CTkEntry(root, textvariable=combine_filename, fg_color='white', width=400).place(x=550, y=335)
    ct.CTkButton(root, text="Combine", fg_color="#800080", command=file_print).place(x=650, y=400)
    root.mainloop()

def doc():
    root = ct.CTkToplevel()
    root.grab_set()
    root.title('MULTIPLEXER')
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    root.config(background='#FFB6C1')

    file_lst = []
    def selectdoc():
        doc = filedialog.askopenfilename(title='Select a document', filetypes=[('Word Documents', '*.docx')])
        file_lst.append(doc)
        ct.CTkLabel(root, text=doc, fg_color='#FFB6C1', text_color='black').place(x=550, y=450 + 20 * len(file_lst))

    def combine():
        if not combinefile.get():
            messagebox.showerror("Error", "Enter file name!")
        elif len(file_lst) < 2:
            messagebox.showerror("Error", "Select at least 2 documents!")
        else:
            output_file = combinefile.get() + ".docx"
            merged_document = Document()
            for file in file_lst:
                doc = Document(file)
                for element in doc.element.body:
                    merged_document.element.body.append(element)
            merged_document.save(output_file)
            messagebox.showinfo("Success", f"Merged DOCX saved as {output_file}")
            ct.CTkButton(root, text="View DOCX", fg_color="#800080", command=lambda: open_file(output_file)).place(x=650, y=500)

    combinefile = StringVar()
    ct.CTkButton(root, text="Select Document", fg_color="#800080", command=selectdoc).place(x=650, y=250)
    ct.CTkEntry(root, textvariable=combinefile, fg_color='white', width=400).place(x=550, y=335)
    ct.CTkButton(root, text="Combine", fg_color="#800080", command=combine).place(x=650, y=400)
    root.mainloop()

def excel():
    root = ct.CTkToplevel()
    root.grab_set()
    root.title('MULTIPLEXER')
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    root.config(background='#FFB6C1')

    excel_files = []
    def file_open():
        filename = filedialog.askopenfilename(title='Select a file', filetypes=[('Excel', '*.xlsx')])
        excel_files.append(filename)
        ct.CTkLabel(root, text=filename, fg_color='#FFB6C1', text_color='black').place(x=550, y=450 + 20 * len(excel_files))

    def file_print():
        if not combine_filename.get():
            messagebox.showerror("Error", "Enter file name!")
        elif len(excel_files) < 2:
            messagebox.showerror("Error", "Select at least 2 files!")
        else:
            output_file = combine_filename.get() + '.xlsx'
            merged_data = pd.concat([pd.read_excel(file) for file in excel_files], ignore_index=True)
            merged_data.to_excel(output_file, index=False)
            messagebox.showinfo("Success", f"Merged Excel saved as {output_file}")
            ct.CTkButton(root, text="View Excel", fg_color="#800080", command=lambda: open_file(output_file)).place(x=650, y=500)

    combine_filename = StringVar()
    ct.CTkButton(root, text="Select File", fg_color="#800080", command=file_open).place(x=650, y=250)
    ct.CTkEntry(root, textvariable=combine_filename, fg_color='white', width=400).place(x=550, y=335)
    ct.CTkButton(root, text="Combine", fg_color="#800080", command=file_print).place(x=650, y=400)
    root.mainloop()

def spl():
    root = ct.CTkToplevel()
    root.grab_set()
    root.title('MULTIPLEXER')
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    root.config(background='#FFB6C1')

    def split_pdf():
        input_path = filedialog.askopenfilename(filetypes=[('PDF Files', '*.pdf')])
        output_dir = filedialog.askdirectory()
        if not input_path or not output_dir:
            return

        def comb():
            pages = page_entry.get()
            try:
                page_numbers = [int(p) for p in pages.split(',')]
                with Pdf.open(input_path.strip()) as pdf:
                    for page_num in page_numbers:
                        output_file = f"{output_dir}/page_{page_num}.pdf"
                        output_pdf = Pdf.new()
                        output_pdf.pages.append(pdf.pages[page_num - 1])
                        output_pdf.save(output_file)
                        ct.CTkButton(root, text=f"View Page {page_num}", fg_color="#800080",
                                     command=lambda: open_file(output_file)).place(x=650, y=500 + 30 * page_num)

                messagebox.showinfo("Success", "PDF pages split successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        page_entry = ct.CTkEntry(root, fg_color='white', width=400)
        page_entry.place(x=550, y=335)
        ct.CTkButton(root, text="Split", fg_color="#800080", command=comb).place(x=650, y=400)

    ct.CTkButton(root, text="Select PDF", fg_color="#800080", command=split_pdf).place(x=650, y=250)
    root.mainloop()

s = ct.CTk()
s.title('MULTIPLEXER')
s.geometry(f"{s.winfo_screenwidth()}x{s.winfo_screenheight()}")
s.config(background="#FFB6C1")

ct.CTkButton(s, text="PDF MERGER", fg_color="#800080", command=pdf).place(x=600, y=300)
ct.CTkButton(s, text="DOCUMENT MERGER", fg_color="#800080", command=doc).place(x=600, y=400)
ct.CTkButton(s, text="EXCEL MERGER", fg_color="#800080", command=excel).place(x=600, y=500)
ct.CTkButton(s, text="PDF SPLITTER", fg_color="#800080", command=spl).place(x=600, y=600)

s.mainloop()
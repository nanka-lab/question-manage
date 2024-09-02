import tkinter as tk
from tkinter import scrolledtext

class InputField_Q:
    def __init__(self, parent):
        self.q_entry = tk.Label(parent, text="Question", bg="red", width=31, height=1)
        self.q_entry.place(x=10, y=500, width=31, height=1)
        self.entry = scrolledtext.ScrolledText(parent, wrap=tk.WORD, width=39, height=8)
        self.entry.place(x=10, y=520)

    def get_input(self):
        return self.entry.get("1.0", tk.END).strip()

class InputField_Kind:
    def __init__(self, parent):
        self.kind_entry = tk.Label(parent, text="Kind of Question", bg="red", width=12, height=1)
        self.kind_entry.place(x=300, y=500)
        self.entry = scrolledtext.ScrolledText(parent, wrap=tk.WORD, width=14, height=8)
        self.entry.place(x=300, y=520)

    def get_input(self):
        return self.entry.get("1.0", tk.END).strip()

class InputField_Ans:
    def __init__(self, parent):
        self.answer_entry = tk.Label(parent, text="Answer", bg="red", width=42, height=1)
        self.answer_entry.place(x=420, y=500)
        self.entry = scrolledtext.ScrolledText(parent, wrap=tk.WORD, width=51, height=8)
        self.entry.place(x=420, y=520)

    def get_input(self):
        return self.entry.get("1.0", tk.END).strip()

class DisplayArea:
    def __init__(self, parent):
        self.canvas = tk.Canvas(parent, bg="green")
        self.canvas.place(x=10, y=0, relwidth=0.8, relheight=0.6)
        self.scrollbar = tk.Scrollbar(parent, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.place(x=parent.winfo_width()-15, y=0, height=parent.winfo_height(), anchor='ne')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')
        self.headers = ["q_id", "Question", "kind_id", "Kind of Question", "Answer"]
        self.column_widths = [5, 20, 5, 20, 20]
        self.create_table()
        self.data = []
        self.load_data()
        self.update_table()

    def create_table(self):
        for col, (header, width) in enumerate(zip(self.headers, self.column_widths)):
            label = tk.Label(self.frame, text=header, bg="lightgrey", borderwidth=1, relief="solid", width=width)
            label.grid(row=0, column=col, sticky='nsew')

    def load_data(self):
        # サンプルデータを追加
        q_id = 0
        self.data.append([q_id, 1, 23, 4, 5])

    def update_table(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.create_table()
        for row_index, row_data in enumerate(self.data):
            for col_index, cell_data in enumerate(row_data):
                label = tk.Label(self.frame, text=cell_data, borderwidth=1, relief="solid", width=self.column_widths[col_index])
                label.grid(row=row_index + 1, column=col_index, sticky='nsew')
        self.frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

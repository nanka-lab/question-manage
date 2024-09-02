import tkinter as tk
from widgets import InputField_Q, InputField_Kind, InputField_Ans, DisplayArea
from database_manager import DatabaseManager

class Application:
    def __init__(self, root):
        self.database = DatabaseManager()
        self.input_field_q = InputField_Q(root)
        self.input_field_kind = InputField_Kind(root)
        self.input_field_ans = InputField_Ans(root)
        self.display_area = DisplayArea(root)

        self.append_button = tk.Button(root, text="追加", command=self.add_entry)
        self.append_button.place(x=300, y=750)
        search_button = tk.Button(root, text="表示", command=self.display_records)
        search_button.place(x=200, y=750)

        # Entryウィジェットにバインドして入力が変更されたらボタンの表示を更新
        self.input_field_q.entry.bind("<KeyRelease>", self.update_button_state)
        self.input_field_kind.entry.bind("<KeyRelease>", self.update_button_state)

        self.update_button_state()  # 初期状態のチェック

    def update_button_state(self, event=None):
        # 両方のフィールドにテキストがある場合のみボタンを表示
        if self.input_field_q.get_input() and self.input_field_kind.get_input():
            self.append_button.place(x=300, y=750)
        else:
            self.append_button.place_forget()

    def add_entry(self):
        input_text_q = self.input_field_q.get_input()
        input_text_kind = self.input_field_kind.get_input()
        self.database.insert_question(input_text_q, input_text_kind)
        self.input_field_q.entry.delete("1.0", tk.END)
        self.input_field_kind.entry.delete("1.0", tk.END)
        self.display_area.update_table()
        self.update_button_state()  # 入力がリセットされた後にボタンの表示を更新

    def display_records(self):
        self.database.show_records()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Question Manage Tool Prototype")
    root.geometry("1000x1000")
    app = Application(root)
    root.mainloop()

import tkinter as tk
from tkinter import scrolledtext
import mysql.connector as sql

# データ入力クラス
class InputField_Q:
    def __init__(self, parent):
        self.q_entry = tk.Label(parent, text="Question", bg="red", width=31, height=1)
        self.q_entry.place(x=10, y=500, width=31, height=1)
        self.entry = scrolledtext.ScrolledText(parent, wrap=tk.WORD, width=39, height=8)
        self.entry.place(x=10, y=520)

    def get_input(self):
        return self.entry.get("1.0", tk.END).strip()  # .strip()で改行を取り除く
class InputField_Kind:
    def __init__(self, parent):
        self.kind_entry = tk.Label(parent, text="kind of Question", bg="red", width=12, height=1)
        self.kind_entry.place(x=300, y=500)
        self.entry = scrolledtext.ScrolledText(parent, wrap=tk.WORD, width=14, height=8)
        self.entry.place(x=300, y=520)

    def get_input(self):
        return self.entry.get("1.0", tk.END).strip()  # .strip()で改行を取り除く
class InputField_Ans:
    def __init__(self, parent):
        self.answer_entry = tk.Label(parent, text="Answer", bg="red", width=42, height=1)
        self.answer_entry.place(x=420, y=500)
        self.entry = scrolledtext.ScrolledText(parent, wrap=tk.WORD, width=51, height=8)
        self.entry.place(x=420, y=520)

    def get_input(self):
        return self.entry.get("1.0", tk.END).strip()  # .strip()で改行を取り除く

# 表示クラス
class DisplayArea:
    def __init__(self, parent):
        # Canvasを作成
        self.canvas = tk.Canvas(parent, bg="green")
        self.canvas.place(x=10, y=0, relwidth=0.8, relheight=0.6)

        # スクロールバーを作成
        self.scrollbar = tk.Scrollbar(parent, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.place(x=parent.winfo_width()-15, y=0, height=parent.winfo_height(), anchor='ne')

        # Canvasにスクロールバーを関連付け
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Canvas内にFrameを作成（テーブルを配置するため）
        self.frame = tk.Frame(self.canvas)

        # FrameをCanvasに配置
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        # 列のヘッダー
        self.headers = ["q_id", "Question", "kind_id", "Kind of Question", "Answer"]
        self.column_widths = [5, 20, 5, 20, 20]  # 列の幅をリストで指定
        self.create_table()

        # テーブルのデータ（サンプル）
        self.data = []

        self.append_data()

        self.update_table()

    def create_table(self):
        for col, (header, width) in enumerate(zip(self.headers, self.column_widths)):
            label = tk.Label(self.frame, text=header, bg="lightgrey", borderwidth=1, relief="solid", width=width)
            label.grid(row=0, column=col, sticky='nsew')
    def append_data(self):
        q_id=0
        self.data.append([q_id,1,23,4,5])
    def update_table(self):
        # 既存のセルをクリア
        for widget in self.frame.winfo_children():
            widget.destroy()

        # 再度テーブルのヘッダーを作成
        self.create_table()

        # データを更新
        for row_index, row_data in enumerate(self.data):
            for col_index, cell_data in enumerate(row_data):
                label = tk.Label(self.frame, text=cell_data, borderwidth=1, relief="solid", width=self.column_widths[col_index])
                label.grid(row=row_index + 1, column=col_index, sticky='nsew')

        # FrameのサイズをCanvasに合わせて更新
        self.frame.update_idletasks()  # Frameのサイズを更新
        self.canvas.config(scrollregion=self.canvas.bbox("all"))


# データベース管理クラス
class DatabaseManager:
    def __init__(self):
        self.connection = sql.connect(**{'user': 'ryuki_ishida',
                                         'password': 'password',
                                         'host': 'localhost',
                                         'database': 'test_database'})
        self.cursor = self.connection.cursor()
        #テーブル作成
        self.cursor.execute("""
CREATE TABLE IF NOT EXISTS kind_question(
    kind_id INT PRIMARY KEY,
    kind_question VARCHAR(100) NOT NULL)
""")
        self.cursor.execute("""
CREATE TABLE IF NOT EXISTS question(
    q_id INT AUTO_INCREMENT PRIMARY KEY,
    kind_id INT,
    question VARCHAR(200) NOT NULL,
    FOREIGN KEY (kind_id) REFERENCES kind_question(kind_id))
""")
        self.cursor.execute("""
CREATE TABLE IF NOT EXISTS answer(
    ans_id INT AUTO_INCREMENT PRIMARY KEY,
    q_id INT,
    kind_id INT,
    answer VARCHAR(1000) NOT NULL,
    FOREIGN KEY (q_id) REFERENCES question(q_id),
    FOREIGN KEY (kind_id) REFERENCES kind_question(kind_id))
""")
        self.kind_list={
            '誰':1,
            'どこ':2,
            '何':3,
            'いつ':4,
            '理由':5,
            '方法':6,
            '意味':7,
            '起源':8,
            '使い方':9,
            '何をした':10}
        self.append_q_kind_record()
    def append_q_kind_record(self):
        for key,value in self.kind_list.items():
            query="INSERT IGNORE INTO kind_question(kind_id,kind_question) VALUES (%s,%s)"
            data=(value,key)
            self.cursor.execute(query,data)

    def append_q_record(self, text_q,text_kind):
        
        
        query = """
INSERT INTO question(kind_id,question)
VALUES (%s,%s)
"""
        data = (self.kind_list.get(text_kind),text_q)
        self.cursor.execute(query, data)
        self.connection.commit()

    def show_record(self):
        self.cursor.execute("""
SELECT * FROM question
""")
        results = self.cursor.fetchall()
        for row in results:
            print(row)

# メインアプリケーションクラス
class Application:
    def __init__(self, root):
        self.input_field_q = InputField_Q(root)
        self.input_field_kind = InputField_Kind(root)
        self.input_field_ans = InputField_Ans(root)
        self.display_area = DisplayArea(root)
        self.database = DatabaseManager()

        self.append_button = tk.Button(root, text="追加", command=self.display_text)
        self.append_button.place(x=300, y=750)
        search_button = tk.Button(root, text="表示", command=self.database.show_record)
        search_button.place(x=200, y=750)

        # Entryウィジェットにバインドして入力が変更されたらボタンの表示を更新
        self.input_field_q.entry.bind("<KeyRelease>", self.update_button_state)
        self.input_field_kind.entry.bind("<KeyRelease>", self.update_button_state)

        self.update_button_state()  # 初期状態のチェック

    def update_button_state(self, event=None):
        # 両方のフィールドにテキストがある場合のみボタンを表示
        if self.input_field_q.get_input() != "" and self.input_field_kind.get_input() != "":
            self.append_button.place(x=300, y=750)
        else:
            self.append_button.place_forget()

    def display_text(self):#常にデータベースから情報を取得して表示したい
        input_text_q = self.input_field_q.get_input()
        input_text_kind = self.input_field_kind.get_input()
        self.database.append_q_record(input_text_q, input_text_kind)
        self.input_field_q.entry.delete("1.0", tk.END)
        self.input_field_kind.entry.delete("1.0", tk.END)
        self.display_area.update_table()
        self.update_button_state()  # 入力がリセットされた後にボタンの表示を更新


# メインループ
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Question Manage tool Prototype")
    root.geometry("1000x1000")  # サイズを調整
    app = Application(root)
    root.mainloop()


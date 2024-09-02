import mysql.connector as sql

# SQLクエリ文字列
INSERT_IGNORE_KIND_QUESTION = """
INSERT IGNORE INTO kind_question (kind_id, kind_question) VALUES (%s, %s)
"""

class DatabaseManager:
    def __init__(self):
        self.connection = sql.connect(
            user='ryuki_ishida',
            password='password',
            host='localhost',
            database='test_database'
        )
        self.cursor = self.connection.cursor()
        self.create_tables()
        self.kind_list = {
            '誰': 1,
            'どこ': 2,
            '何': 3,
            'いつ': 4,
            '理由': 5,
            '方法': 6,
            '意味': 7,
            '起源': 8,
            '使い方': 9,
            '何をした': 10
        }
        self.append_q_kind_record()

    def create_tables(self):
        with open('schema.sql', 'r') as schema_file:
            schema_sql = schema_file.read()
        self.cursor.execute(schema_sql)

    def append_q_kind_record(self):
        for key, value in self.kind_list.items():
            query = INSERT_IGNORE_KIND_QUESTION
            data = (value, key)
            self.cursor.execute(query, data)
        self.connection.commit()

    def insert_question(self, text_q, text_kind):
        query = """
        INSERT INTO question (kind_id, question)
        VALUES (%s, %s)
        """
        kind_id = self.kind_list.get(text_kind)
        data = (kind_id, text_q)
        self.cursor.execute(query, data)
        self.connection.commit()

    def show_records(self):
        self.cursor.execute("SELECT * FROM question")
        results = self.cursor.fetchall()
        for row in results:
            print(row)

import sqlite3
import os

##https://docs.python.org/3/library/sqlite3.html
DB_PATH = "todos.db" #database file path

def initialize_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        conn.execute('''
            CREATE TABLE tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

def add_todo(description):
    conn = sqlite3.connect(DB_PATH)
    conn.execute('INSERT INTO tasks (description) VALUES (?)', (description,))  #comma because we make it a tuple
    conn.commit()
    conn.close()


def get_all_todos():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT id, description FROM tasks")  #only 2 columns
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def delete_task(task_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()




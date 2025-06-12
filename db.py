import sqlite3
from pathlib import Path

DB_FILE = "encouragify.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # 日記テーブルを作成（あればスキップ）
    c.execute("""
    CREATE TABLE IF NOT EXISTS diary_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        mood TEXT,
        entry TEXT
    )
    """)

    # やること設定テーブル（1行のみ）
    c.execute("""
    CREATE TABLE IF NOT EXISTS task_config (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        start_date TEXT,
        task_1 TEXT,
        task_2 TEXT,
        task_3 TEXT
    )
    """)


    conn.commit()
    conn.close()

def insert_diary(date, mood, entry):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO diary_logs (date, mood, entry) VALUES (?, ?, ?)", (date, mood, entry))
    conn.commit()
    conn.close()

def get_recent_diaries(limit=5):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT date, mood, entry FROM diary_logs ORDER BY date DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows


def get_task_config():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT start_date, task_1, task_2, task_3 FROM task_config WHERE id = 1")
    row = c.fetchone()
    conn.close()
    return row  # None または (start_date, task_1, task_2, task_3)

def save_task_config(start_date, tasks):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("REPLACE INTO task_config (id, start_date, task_1, task_2, task_3) VALUES (1, ?, ?, ?, ?)",
              (start_date, *(tasks + [""] * (3 - len(tasks)))))
    conn.commit()
    conn.close()

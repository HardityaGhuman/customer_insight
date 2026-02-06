import sqlite3
import os
import json

DB_PATH = "data/app.db"

def get_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Decision log table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS decision_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        issue_category TEXT,
        category_confidence REAL,
        escalation_level TEXT,
        escalation_reason TEXT
    )
    """)

    # System state table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_state (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    conn.commit()
    conn.close()

def insert_decision(decision):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO decision_log (
            timestamp,
            issue_category,
            category_confidence,
            escalation_level,
            escalation_reason
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        decision["timestamp"],
        decision["issue_category"]["category"],
        decision["issue_category"]["confidence"],
        decision["escalation"]["level"],
        decision["escalation"]["reason"]
    ))

    conn.commit()
    conn.close()

def get_state(key, default=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT value FROM system_state WHERE key = ?",
        (key,)
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return default

    return json.loads(row[0])


def set_state(key, value):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO system_state (key, value)
        VALUES (?, ?)
        ON CONFLICT(key)
        DO UPDATE SET value = excluded.value
    """, (key, json.dumps(value)))

    conn.commit()
    conn.close()
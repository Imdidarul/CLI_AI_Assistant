import sqlite3
import json
import os

os.makedirs("./storage/database", exist_ok=True)

RAW_DB_PATH = "./storage/database/rawEvents.db"
MEMORY_DB_PATH = "./storage/database/memories.db"

def createDatabases():
    with sqlite3.connect(RAW_DB_PATH) as conn:
        conn.cursor().execute("""
            CREATE TABLE IF NOT EXISTS raw_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                app TEXT NOT NULL,
                source TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        conn.commit()
    with sqlite3.connect(MEMORY_DB_PATH) as conn:
        conn.cursor().execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                people TEXT,
                projects TEXT,
                topics TEXT,
                summary TEXT NOT NULL,
                sensitivity TEXT NOT NULL,
                justification TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)    
        conn.commit()


def saveRawEvent(event):
    with sqlite3.connect(RAW_DB_PATH) as conn:
        conn.cursor().execute("""
            INSERT INTO raw_events (event_type, app, source, content, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """,(event['type'],event['app'],event['source'],event['content'],event['timestamp'])
        )
        conn.commit()
def saveMemory(memory, timestamp):
    with sqlite3.connect(MEMORY_DB_PATH) as conn:
        conn.cursor().execute("""
            INSERT INTO memories (people, projects, topics, summary, sensitivity, justification, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                json.dumps(memory.get('people',[])),
                json.dumps(memory.get('projects',[])),
                json.dumps(memory.get('topics',[])),
                memory.get('summary',""),
                memory.get('sensitivity',""),
                memory.get('justification',""),
                timestamp
        ))
        conn.commit()

def deleteMemoriesBefore(timestamp):
    with sqlite3.connect(MEMORY_DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM memories
            WHERE timestamp < ?
        """,(timestamp,))
        deleted = cursor.rowcount
        conn.commit()
    print(f"{deleted} Memories deleted")

    with sqlite3.connect(RAW_DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM raw_events
            WHERE timestamp < ?
        """,(timestamp,))
        deleted = cursor.rowcount
        conn.commit()
    print(f"{deleted} Raw data deleted")

def deleteMemoriesAfter(timestamp):
    with sqlite3.connect(MEMORY_DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM memories
            WHERE timestamp > ?
        """,(timestamp,))
        deleted = cursor.rowcount
        conn.commit()
    print(f"{deleted} Memories deleted")
    with sqlite3.connect(RAW_DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM raw_events
            WHERE timestamp > ?
        """,(timestamp,))
        deleted = cursor.rowcount
        conn.commit()
    print(f"{deleted} Raw data deleted")

def wipeAll():
    with sqlite3.connect(MEMORY_DB_PATH) as conn:
        conn.execute("DELETE FROM memories")

    with sqlite3.connect(RAW_DB_PATH) as conn:
        conn.execute("DELETE FROM raw_events")
    print("All data wiped")
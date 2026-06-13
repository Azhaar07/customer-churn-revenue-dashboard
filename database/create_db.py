import sqlite3

DB_NAME = "database/churn_analytics.db"

with sqlite3.connect(DB_NAME) as conn:
    cursor = conn.cursor()

    with open("database/schema.sql", "r") as f:
        schema = f.read()

    cursor.executescript(schema)

    print("Database created successfully!")

conn.close()
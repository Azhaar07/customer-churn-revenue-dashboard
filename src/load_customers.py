import sqlite3
import pandas as pd

DB_PATH = "database/churn_analytics.db"
CSV_PATH = "data/sample/customers.csv"

# Read CSV
df = pd.read_csv(CSV_PATH)

# Connect to SQLite
conn = sqlite3.connect(DB_PATH)

# Insert into users table
df.to_sql(
    "users",
    conn,
    if_exists="append",
    index=False
)

conn.close()

print(f"{len(df)} customers inserted successfully!")
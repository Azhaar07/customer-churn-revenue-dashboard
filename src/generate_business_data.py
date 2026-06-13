import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = "database/churn_analytics.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Get all users
cursor.execute("SELECT user_id FROM users")
users = cursor.fetchall()

today = datetime.now()

for user in users:
    user_id = user[0]

    # Generate 12 months of payment history
    for month in range(12):
        payment_date = today - timedelta(days=30 * month)

        amount = random.choice([199, 299, 499])

        payment_status = random.choices(
            ["Paid", "Failed"],
            weights=[90, 10]
        )[0]

        cursor.execute("""
            INSERT INTO payments
            (user_id, payment_date, amount, payment_status)
            VALUES (?, ?, ?, ?)
        """, (
            user_id,
            payment_date.strftime("%Y-%m-%d"),
            amount,
            payment_status
        ))

    # Generate usage logs
    for month in range(12):
        usage_date = today - timedelta(days=30 * month)

        sessions = random.randint(0, 50)
        minutes_spent = sessions * random.randint(5, 30)

        cursor.execute("""
            INSERT INTO usage_logs
            (user_id, usage_date, sessions, minutes_spent)
            VALUES (?, ?, ?, ?)
        """, (
            user_id,
            usage_date.strftime("%Y-%m-%d"),
            sessions,
            minutes_spent
        ))

conn.commit()
conn.close()

print("Payments and usage logs generated successfully!")
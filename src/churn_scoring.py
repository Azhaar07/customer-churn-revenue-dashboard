import sqlite3

DB_PATH = "database/churn_analytics.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Clear old predictions
cursor.execute("DELETE FROM churn_predictions")

cursor.execute("""
SELECT
    u.user_id,
    AVG(ul.sessions) as avg_sessions,
    AVG(CASE WHEN p.payment_status='Failed' THEN 1 ELSE 0 END) as fail_rate
FROM users u
LEFT JOIN usage_logs ul
    ON u.user_id = ul.user_id
LEFT JOIN payments p
    ON u.user_id = p.user_id
GROUP BY u.user_id
""")

rows = cursor.fetchall()

for row in rows:
    user_id, avg_sessions, fail_rate = row

    score = 0

    if avg_sessions < 10:
        score += 60
    elif avg_sessions < 20:
        score += 30

    if fail_rate > 0.20:
        score += 40
    elif fail_rate > 0.10:
        score += 20

    if score >= 70:
        risk = "High Risk"
        churn = 1
    elif score >= 40:
        risk = "Medium Risk"
        churn = 0
    else:
        risk = "Safe"
        churn = 0

    cursor.execute("""
    INSERT INTO churn_predictions
    (
        user_id,
        risk_score,
        risk_level,
        predicted_churn
    )
    VALUES (?, ?, ?, ?)
    """, (
        user_id,
        score,
        risk,
        churn
    ))

conn.commit()
conn.close()

print("Churn predictions generated successfully!")
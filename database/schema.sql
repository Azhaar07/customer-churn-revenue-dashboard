-- USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    region TEXT NOT NULL,
    signup_date DATE NOT NULL,
    subscription_type TEXT NOT NULL,
    status TEXT DEFAULT 'Active'
);

-- PAYMENTS TABLE
CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    payment_date DATE NOT NULL,
    amount REAL NOT NULL,
    payment_status TEXT DEFAULT 'Paid',
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- USAGE LOGS TABLE
CREATE TABLE IF NOT EXISTS usage_logs (
    usage_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    usage_date DATE NOT NULL,
    sessions INTEGER DEFAULT 0,
    minutes_spent INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- CHURN PREDICTIONS TABLE
CREATE TABLE IF NOT EXISTS churn_predictions (
    prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    risk_score REAL,
    risk_level TEXT,
    predicted_churn INTEGER,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
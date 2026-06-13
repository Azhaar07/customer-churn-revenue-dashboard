-- Monthly Revenue

SELECT
    strftime('%Y-%m', payment_date) AS month,
    SUM(amount) AS revenue
FROM payments
WHERE payment_status = 'Paid'
GROUP BY month
ORDER BY month;

------------------------------------------------

-- Revenue Growth Using LAG()

SELECT
    month,
    revenue,
    revenue -
    LAG(revenue) OVER (
        ORDER BY month
    ) AS revenue_growth
FROM (
    SELECT
        strftime('%Y-%m', payment_date) AS month,
        SUM(amount) AS revenue
    FROM payments
    WHERE payment_status = 'Paid'
    GROUP BY month
);

------------------------------------------------

-- Customer Revenue Ranking

SELECT
    user_id,
    SUM(amount) AS total_revenue,
    RANK() OVER (
        ORDER BY SUM(amount) DESC
    ) AS revenue_rank
FROM payments
WHERE payment_status='Paid'
GROUP BY user_id;

------------------------------------------------

-- Highest Risk Customers

SELECT
    user_id,
    risk_score,
    risk_level
FROM churn_predictions
ORDER BY risk_score DESC
LIMIT 20;
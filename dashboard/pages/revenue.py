import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(
    page_title="Revenue Analytics",
    page_icon="",
    layout="wide"
)

st.title("Revenue Analytics")
st.caption("Revenue performance, customer value and growth trends")

conn = sqlite3.connect(
    "database/churn_analytics.db"
)

# =====================
# KPI SECTION
# =====================

total_revenue = pd.read_sql("""
SELECT SUM(amount) AS revenue
FROM payments
WHERE payment_status='Paid'
""", conn)

monthly_revenue = pd.read_sql("""
SELECT
AVG(month_revenue) AS avg_rev
FROM(
    SELECT
    SUM(amount) AS month_revenue
    FROM payments
    WHERE payment_status='Paid'
    GROUP BY strftime('%Y-%m',payment_date)
)
""", conn)

best_month = pd.read_sql("""
SELECT
strftime('%Y-%m',payment_date) AS month,
SUM(amount) AS revenue
FROM payments
WHERE payment_status='Paid'
GROUP BY month
ORDER BY revenue DESC
LIMIT 1
""", conn)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Revenue",
    f"₹{int(total_revenue.iloc[0]['revenue']):,}"
)

col2.metric(
    "Avg Monthly Revenue",
    f"₹{int(monthly_revenue.iloc[0]['avg_rev']):,}"
)

col3.metric(
    "Best Revenue Month",
    best_month.iloc[0]["month"]
)

st.divider()

# =====================
# REVENUE TREND
# =====================

st.subheader("📈 Monthly Revenue Trend")

revenue_df = pd.read_sql("""
SELECT
strftime('%Y-%m',payment_date) AS month,
SUM(amount) AS revenue
FROM payments
WHERE payment_status='Paid'
GROUP BY month
ORDER BY month
""", conn)

fig = px.area(
    revenue_df,
    x="month",
    y="revenue",
    markers=True,
    title="Revenue Growth Over Time"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================
# REGION ANALYSIS
# =====================

st.subheader("Revenue by Region")

region_df = pd.read_sql("""
SELECT
u.region,
SUM(p.amount) AS revenue
FROM payments p
JOIN users u
ON p.user_id=u.user_id
WHERE p.payment_status='Paid'
GROUP BY u.region
ORDER BY revenue DESC
""", conn)

fig_region = px.bar(
    region_df,
    x="region",
    y="revenue",
    title="Regional Revenue Performance"
)

st.plotly_chart(
    fig_region,
    use_container_width=True
)

# =====================
# SUBSCRIPTION ANALYSIS
# =====================

st.subheader("💳 Revenue by Subscription Plan")

plan_df = pd.read_sql("""
SELECT
u.subscription_type,
SUM(p.amount) AS revenue
FROM payments p
JOIN users u
ON p.user_id=u.user_id
WHERE p.payment_status='Paid'
GROUP BY u.subscription_type
ORDER BY revenue DESC
""", conn)

fig_plan = px.pie(
    plan_df,
    names="subscription_type",
    values="revenue",
    hole=0.5
)

st.plotly_chart(
    fig_plan,
    use_container_width=True
)

# =====================
# TOP CUSTOMERS
# =====================

st.subheader("Top Revenue Customers")

top_customers = pd.read_sql("""
SELECT
u.full_name,
u.region,
u.subscription_type,
SUM(p.amount) AS revenue,
RANK() OVER(
ORDER BY SUM(p.amount) DESC
) AS ranking
FROM payments p
JOIN users u
ON p.user_id=u.user_id
WHERE p.payment_status='Paid'
GROUP BY u.user_id
ORDER BY revenue DESC
LIMIT 15
""", conn)

st.dataframe(
    top_customers,
    use_container_width=True
)

conn.close()

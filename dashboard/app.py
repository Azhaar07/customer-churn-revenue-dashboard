import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
    page_title="Customer Churn Dashboard",
    layout="wide"
)

st.title("Customer Churn & Revenue Dashboard")

conn = sqlite3.connect(
    "database/churn_analytics.db"
)

regions = pd.read_sql(
    "SELECT DISTINCT region FROM users",
    conn
)

plans = pd.read_sql(
    "SELECT DISTINCT subscription_type FROM users",
    conn
)

selected_region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + regions["region"].tolist()
)

selected_plan = st.sidebar.selectbox(
    "Select Subscription",
    ["All"] + plans["subscription_type"].tolist()
)

filter_condition = ""

if selected_region != "All":
    filter_condition += f" AND u.region = '{selected_region}'"

if selected_plan != "All":
    filter_condition += f" AND u.subscription_type = '{selected_plan}'"

# KPI 1

users = pd.read_sql(
    "SELECT COUNT(*) as total FROM users",
    conn
)

# KPI 2

revenue = pd.read_sql(
    """
    SELECT SUM(amount) as revenue
    FROM payments
    WHERE payment_status='Paid'
    """,
    conn
)

# KPI 3

high_risk = pd.read_sql(
    """
    SELECT COUNT(*) as total
    FROM churn_predictions
    WHERE risk_level='High Risk'
    """,
    conn
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Customers",
    int(users.iloc[0]["total"])
)

col2.metric(
    "Revenue",
    f"₹{int(revenue.iloc[0]['revenue'])}"
)

col3.metric(
    "High Risk Users",
    int(high_risk.iloc[0]["total"])
)

# Revenue Trend Chart

st.subheader("Monthly Revenue Trend")

revenue_trend = pd.read_sql(
    f"""
    SELECT
        strftime('%Y-%m', p.payment_date) AS month,
        SUM(p.amount) AS revenue
    FROM payments p
    JOIN users u
        ON p.user_id = u.user_id
    WHERE p.payment_status='Paid'
    {filter_condition}
    GROUP BY month
    ORDER BY month
    """,
    conn
)

import plotly.express as px

fig = px.line(
    revenue_trend,
    x="month",
    y="revenue",
    markers=True,
    title="Monthly Revenue"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Churn Risk Distribution")

risk_distribution = pd.read_sql(
    f"""
    SELECT
        cp.risk_level,
        COUNT(*) as count
    FROM churn_predictions cp
    JOIN users u
        ON cp.user_id = u.user_id
    WHERE 1=1
    {filter_condition}
    GROUP BY cp.risk_level
    """,
    conn
)

fig2 = px.pie(
    risk_distribution,
    names="risk_level",
    values="count",
    title="Customer Risk Segmentation"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.subheader("Top 20 High Risk Customers")

risk_df = pd.read_sql(
    f"""
SELECT
    cp.*
FROM churn_predictions cp
JOIN users u
    ON cp.user_id = u.user_id
WHERE 1=1
{filter_condition}
ORDER BY cp.risk_score DESC
LIMIT 20
""",
    conn
)

st.subheader("Top Revenue Customers")

top_customers = pd.read_sql(
    f"""
    SELECT
        u.full_name,
        u.region,
        u.subscription_type,
        SUM(p.amount) AS total_revenue,
        RANK() OVER (
            ORDER BY SUM(p.amount) DESC
        ) AS revenue_rank
    FROM payments p
    JOIN users u
        ON p.user_id = u.user_id
    WHERE p.payment_status='Paid'
    {filter_condition}
    GROUP BY u.user_id
    ORDER BY total_revenue DESC
    LIMIT 10
    """,
    conn
)

st.dataframe(
    top_customers,
    use_container_width=True
)

csv = risk_df.to_csv(index=False)

st.download_button(
    label="Download High Risk Customers",
    data=csv,
    file_name="high_risk_customers.csv",
    mime="text/csv"
)

st.dataframe(risk_df)

conn.close()
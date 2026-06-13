import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(
    page_title="Overview",
    layout="wide"
)

st.title("Business Overview")

conn = sqlite3.connect(
    "database/churn_analytics.db"
)

# =========================
# KPI SECTION
# =========================

total_customers = pd.read_sql(
    "SELECT COUNT(*) AS total FROM users",
    conn
)

active_customers = pd.read_sql(
    """
    SELECT COUNT(*) AS total
    FROM users
    WHERE status='Active'
    """,
    conn
)

total_revenue = pd.read_sql(
    """
    SELECT SUM(amount) AS revenue
    FROM payments
    WHERE payment_status='Paid'
    """,
    conn
)

arpu = pd.read_sql(
    """
    SELECT
    SUM(amount) / COUNT(DISTINCT user_id)
    AS arpu
    FROM payments
    WHERE payment_status='Paid'
    """,
    conn
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Customers",
    int(total_customers.iloc[0]["total"])
)

col2.metric(
    "Active Customers",
    int(active_customers.iloc[0]["total"])
)

col3.metric(
    "Total Revenue",
    f"₹{int(total_revenue.iloc[0]['revenue'])}"
)

col4.metric(
    "ARPU",
    f"₹{int(arpu.iloc[0]['arpu'])}"
)

# =========================
# REGION DISTRIBUTION
# =========================

st.subheader("Customers by Region")

region_df = pd.read_sql(
    """
    SELECT
        region,
        COUNT(*) AS total
    FROM users
    GROUP BY region
    """,
    conn
)

fig_region = px.bar(
    region_df,
    x="region",
    y="total",
    title="Customer Distribution by Region"
)

st.plotly_chart(
    fig_region,
    use_container_width=True
)

# =========================
# SUBSCRIPTION DISTRIBUTION
# =========================

st.subheader("Subscription Distribution")

plan_df = pd.read_sql(
    """
    SELECT
        subscription_type,
        COUNT(*) AS total
    FROM users
    GROUP BY subscription_type
    """
    ,
    conn
)

fig_plan = px.pie(
    plan_df,
    names="subscription_type",
    values="total",
    title="Subscription Plans"
)

st.plotly_chart(
    fig_plan,
    use_container_width=True
)

conn.close()

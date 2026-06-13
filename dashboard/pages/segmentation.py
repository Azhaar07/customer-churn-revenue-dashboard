import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(
    page_title="Customer Segmentation",
    layout="wide"
)

st.title("Customer Segmentation")
st.caption("Customer grouping and behavioral insights")

conn = sqlite3.connect(
    "database/churn_analytics.db"
)

# =====================
# CUSTOMER BY REGION
# =====================

st.subheader("Customer Distribution by Region")

region_df = pd.read_sql("""
SELECT
region,
COUNT(*) AS customers
FROM users
GROUP BY region
ORDER BY customers DESC
""", conn)

fig_region = px.bar(
    region_df,
    x="region",
    y="customers"
)

st.plotly_chart(
    fig_region,
    use_container_width=True
)

# =====================
# CUSTOMER BY PLAN
# =====================

st.subheader("Customer Distribution by Subscription")

plan_df = pd.read_sql("""
SELECT
subscription_type,
COUNT(*) AS customers
FROM users
GROUP BY subscription_type
ORDER BY customers DESC
""", conn)

fig_plan = px.pie(
    plan_df,
    names="subscription_type",
    values="customers",
    hole=0.4
)

st.plotly_chart(
    fig_plan,
    use_container_width=True
)

# =====================
# REVENUE BY PLAN
# =====================

st.subheader("Revenue by Subscription")

revenue_plan = pd.read_sql("""
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

fig_rev = px.bar(
    revenue_plan,
    x="subscription_type",
    y="revenue"
)

st.plotly_chart(
    fig_rev,
    use_container_width=True
)

# =====================
# RISK BY PLAN
# =====================

st.subheader("Risk Distribution by Subscription")

risk_plan = pd.read_sql("""
SELECT
u.subscription_type,
cp.risk_level,
COUNT(*) AS customers
FROM churn_predictions cp
JOIN users u
ON cp.user_id=u.user_id
GROUP BY
u.subscription_type,
cp.risk_level
""", conn)

fig_risk = px.bar(
    risk_plan,
    x="subscription_type",
    y="customers",
    color="risk_level",
    barmode="group"
)

st.plotly_chart(
    fig_risk,
    use_container_width=True
)

# =====================
# CUSTOMER SEGMENT TABLE
# =====================

st.subheader("Customer Segments")

segment_table = pd.read_sql("""
SELECT
u.full_name,
u.region,
u.subscription_type,
cp.risk_level,
cp.risk_score
FROM users u
JOIN churn_predictions cp
ON u.user_id=cp.user_id
ORDER BY cp.risk_score DESC
LIMIT 25
""", conn)

st.dataframe(
    segment_table,
    use_container_width=True
)

conn.close()

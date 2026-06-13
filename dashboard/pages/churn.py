import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(
    page_title="Churn Analytics",
    page_icon="⚠️",
    layout="wide"
)

st.title("⚠️ Churn Analytics")
st.caption("Customer retention and churn risk monitoring")

conn = sqlite3.connect(
    "database/churn_analytics.db"
)

# =====================
# KPI SECTION
# =====================

high_risk = pd.read_sql("""
SELECT COUNT(*) AS total
FROM churn_predictions
WHERE risk_level='High Risk'
""", conn)

medium_risk = pd.read_sql("""
SELECT COUNT(*) AS total
FROM churn_predictions
WHERE risk_level='Medium Risk'
""", conn)

safe_users = pd.read_sql("""
SELECT COUNT(*) AS total
FROM churn_predictions
WHERE risk_level='Safe'
""", conn)

total_users = pd.read_sql("""
SELECT COUNT(*) AS total
FROM users
""", conn)

churn_rate = (
    high_risk.iloc[0]["total"]
    / total_users.iloc[0]["total"]
) * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🚨 High Risk",
    int(high_risk.iloc[0]["total"])
)

col2.metric(
    "⚡ Medium Risk",
    int(medium_risk.iloc[0]["total"])
)

col3.metric(
    "✅ Safe Users",
    int(safe_users.iloc[0]["total"])
)

col4.metric(
    "📉 Churn Rate",
    f"{churn_rate:.2f}%"
)

st.divider()

# =====================
# RISK DISTRIBUTION
# =====================

st.subheader("Customer Risk Distribution")

risk_df = pd.read_sql("""
SELECT
risk_level,
COUNT(*) AS total
FROM churn_predictions
GROUP BY risk_level
""", conn)

fig_risk = px.pie(
    risk_df,
    names="risk_level",
    values="total",
    hole=0.5
)

st.plotly_chart(
    fig_risk,
    use_container_width=True
)

# =====================
# RISK SCORE HISTOGRAM
# =====================

st.subheader("Risk Score Distribution")

score_df = pd.read_sql("""
SELECT risk_score
FROM churn_predictions
""", conn)

fig_hist = px.histogram(
    score_df,
    x="risk_score",
    nbins=20,
    title="Customer Risk Scores"
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)

# =====================
# HIGH RISK CUSTOMERS
# =====================

st.subheader("Top High Risk Customers")

high_risk_customers = pd.read_sql("""
SELECT
u.full_name,
u.region,
u.subscription_type,
cp.risk_score,
cp.risk_level
FROM churn_predictions cp
JOIN users u
ON cp.user_id=u.user_id
WHERE cp.risk_level='High Risk'
ORDER BY cp.risk_score DESC
LIMIT 20
""", conn)

st.dataframe(
    high_risk_customers,
    use_container_width=True
)

# =====================
# REGION RISK ANALYSIS
# =====================

st.subheader("Risk by Region")

region_risk = pd.read_sql("""
SELECT
u.region,
COUNT(*) AS high_risk_users
FROM churn_predictions cp
JOIN users u
ON cp.user_id=u.user_id
WHERE cp.risk_level='High Risk'
GROUP BY u.region
""", conn)

fig_region = px.bar(
    region_risk,
    x="region",
    y="high_risk_users",
    title="High Risk Customers by Region"
)

st.plotly_chart(
    fig_region,
    use_container_width=True
)

conn.close()

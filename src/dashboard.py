import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Customer Analytics Dashboard", layout="wide")

st.title("Customer Analytics & Business Intelligence Dashboard")

st.write("""
This dashboard analyzes customer behavior, revenue trends, and segmentation using real retail transaction data.
""")

# Load data
df = pd.read_csv("data/cleaned_retail.csv")
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Customer-level data
customer_df = pd.read_csv("outputs/customer_segments.csv")

# -----------------------------
# KPIs
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Revenue", f"${df['TotalSpend'].sum():,.0f}")

with col2:
    st.metric("Total Customers", df["CustomerID"].nunique())

with col3:
    st.metric("Total Transactions", df["InvoiceNo"].nunique())

# -----------------------------
# Revenue over time
# -----------------------------
st.subheader("Revenue Over Time")

monthly = df.copy()
monthly["month"] = monthly["InvoiceDate"].dt.to_period("M")
monthly = monthly.groupby("month")["TotalSpend"].sum().reset_index()

st.line_chart(monthly.set_index("month"))

# -----------------------------
# Top customers
# -----------------------------
st.subheader("Top Customers")

top_customers = df.groupby("CustomerID")["TotalSpend"].sum().sort_values(ascending=False).head(10)
st.bar_chart(top_customers)

# -----------------------------
# Customer Segments
# -----------------------------
st.subheader("Customer Segmentation")

if os.path.exists("outputs/customer_segments.png"):
    st.image("outputs/customer_segments.png")

if os.path.exists("outputs/customer_spend_vs_orders.png"):
    st.image("outputs/customer_spend_vs_orders.png")

st.dataframe(customer_df.head(20))

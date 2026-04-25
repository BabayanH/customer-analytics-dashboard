import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os

os.makedirs("outputs", exist_ok=True)

# 1. Load cleaned data
df=pd.read_csv("data/cleaned_retail.csv")

# 2. Save to SQL database
conn = sqlite3.connect("retail.db")

df.to_sql("transactions", conn, if_exists="replace",index=False)
print("Data loaded into SQL database")

# 3. SQL Queries
# Top 10 customers by spending
query_top_customers = """
SELECT CustomerID, SUM(TotalSpend) as total_spend
FROM transactions
GROUP BY CustomerID
ORDER BY total_spend DESC
LIMIT 10
"""

top_customers = pd.read_sql(query_top_customers, conn)

print("\nTop Customers:")
print(top_customers)

#Monthly Revenue
query_monthly = """
SELECT strftime('%Y-%m', InvoiceDate) as month,
       SUM(TotalSpend) as revenue
FROM transactions
GROUP BY month
ORDER BY month
"""

monthly_revenue= pd.read_sql(query_monthly, conn)
print("\nMonthly Revenue:")
print(monthly_revenue.head())


#4 Charts

# Chart 1: Top Customers
plt.figure(figsize=(10, 5))
plt.bar(top_customers["CustomerID"].astype(str), top_customers["total_spend"])
plt.title("Top 10 Customers by Spending")
plt.xlabel("Customer ID")
plt.ylabel("Total Spend")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/top_customers.png")
plt.show()

# Chart 2: Monthly Revenue
plt.figure(figsize=(12, 5))
plt.plot(monthly_revenue["month"], monthly_revenue["revenue"])
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/monthly_revenue.png")
plt.show()

print("Charts saved to outputs folder")
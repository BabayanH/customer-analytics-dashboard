import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os

os.makedirs("outputs", exist_ok=True)

df = pd.read_csv("data/cleaned_retail.csv")
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Customer-level summary
customer_df = df.groupby("CustomerID").agg(
    total_spend=("TotalSpend", "sum"),
    total_orders=("InvoiceNo", "nunique"),
    total_items=("Quantity", "sum"),
    avg_order_value=("TotalSpend", "mean")
).reset_index()

# Features for clustering
features = customer_df[[
    "total_spend",
    "total_orders",
    "total_items",
    "avg_order_value"
]]

# Scale the data so one large column does not dominate
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Create 3 customer groups
kmeans = KMeans(n_clusters=3, random_state=42)
customer_df["segment"] = kmeans.fit_predict(scaled_features)

# Rename segments based on average spend
segment_order = customer_df.groupby("segment")["total_spend"].mean().sort_values().index

segment_names = {
    segment_order[0]: "Low Value",
    segment_order[1]: "Medium Value",
    segment_order[2]: "High Value"
}

customer_df["segment_name"] = customer_df["segment"].map(segment_names)

customer_df.to_csv("outputs/customer_segments.csv", index=False)

print(customer_df.head())
print("\nSegment Summary:")
print(customer_df.groupby("segment_name")[["total_spend", "total_orders", "total_items"]].mean())

# Chart: Customer segments
segment_counts = customer_df["segment_name"].value_counts()

plt.figure(figsize=(8, 5))
plt.bar(segment_counts.index, segment_counts.values)
plt.title("Customer Segments")
plt.xlabel("Segment")
plt.ylabel("Number of Customers")
plt.tight_layout()
plt.savefig("outputs/customer_segments.png")
plt.show()

# Chart: Spend vs Orders
plt.figure(figsize=(9, 6))
for segment in customer_df["segment_name"].unique():
    subset = customer_df[customer_df["segment_name"] == segment]
    plt.scatter(subset["total_orders"], subset["total_spend"], label=segment, alpha=0.6)

plt.title("Customer Segmentation: Spend vs Orders")
plt.xlabel("Total Orders")
plt.ylabel("Total Spend")
plt.legend()
plt.tight_layout()
plt.savefig("outputs/customer_spend_vs_orders.png")
plt.show()
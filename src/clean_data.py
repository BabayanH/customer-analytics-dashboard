import pandas as pd
import os


os.makedirs("outputs", exist_ok=True)

df = pd.read_excel("data/Online Retail.xlsx")

print("Original rows:", len(df))
print(df.head())

#Remove missing customer IDs
df=df.dropna(subset=["CustomerID"])

#Remove returns/cancelled or invalid transactions
df=df[df["Quantity"]>0]
df=df[df["UnitPrice"]>0]

#Create total revenue column
df["TotalSpend"]=df["Quantity"] * df["UnitPrice"]

#Convert CustomerID to integer
df["CustomerID"] = df["CustomerID"].astype(int)

#Save cleaned CSV
df.to_csv("data/cleaned_retail.csv", index=False)

print("Cleaned rows:" , len(df))
print("Cleaned file saved to data/cleaned_retail.csv")
print(df.head())
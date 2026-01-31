import pandas as pd

print("DEBUG: Vendor & Customer Analysis started")

# ================= LOAD DATA =================
try:
    df = pd.read_excel("classified_with_recurring.xlsx")
    print("DEBUG: Loaded classified_with_recurring.xlsx")
except FileNotFoundError:
    df = pd.read_excel("classified_output.xlsx")
    print("DEBUG: Loaded classified_output.xlsx")

# ================= BASIC CLEANING =================
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"])

df["Credit Amount"] = df["Credit Amount"].fillna(0)
df["Debit Amount"] = df["Debit Amount"].fillna(0)

# ================= PARTY EXTRACTION =================
# Description format: "UPI - Name"
df["Party"] = df["Description"].apply(
    lambda x: str(x).split("-")[-1].strip()
)

# ================= MONTH COLUMN =================
df["Month"] = df["Date"].dt.to_period("M").astype(str)

# ==================================================
# 🧾 VENDOR ANALYSIS (DEBIT SIDE)
# ==================================================
vendors = df[df["Debit Amount"] > 0]

vendor_summary = vendors.groupby("Party").agg(
    Total_Spent=("Debit Amount", "sum"),
    Transaction_Count=("Debit Amount", "count"),
    Average_Amount=("Debit Amount", "mean"),
    First_Transaction=("Date", "min"),
    Last_Transaction=("Date", "max")
).reset_index()

vendor_summary = vendor_summary.sort_values(
    by="Total_Spent", ascending=False
)

vendor_summary.to_excel("vendor_summary.xlsx", index=False)
print("✔ Vendor summary generated")

# ================= VENDOR MONTHLY TREND =================
vendor_monthly = vendors.groupby(
    ["Party", "Month"]
).agg(
    Monthly_Spent=("Debit Amount", "sum")
).reset_index()

vendor_monthly.to_excel("vendor_monthly_trend.xlsx", index=False)
print("✔ Vendor monthly trend generated")

# ==================================================
# 🧾 CUSTOMER ANALYSIS (CREDIT SIDE)
# ==================================================
customers = df[df["Credit Amount"] > 0]

customer_summary = customers.groupby("Party").agg(
    Total_Received=("Credit Amount", "sum"),
    Transaction_Count=("Credit Amount", "count"),
    Average_Amount=("Credit Amount", "mean"),
    First_Transaction=("Date", "min"),
    Last_Transaction=("Date", "max")
).reset_index()

customer_summary = customer_summary.sort_values(
    by="Total_Received", ascending=False
)

customer_summary.to_excel("customer_summary.xlsx", index=False)
print("✔ Customer summary generated")

# ================= CUSTOMER MONTHLY TREND =================
customer_monthly = customers.groupby(
    ["Party", "Month"]
).agg(
    Monthly_Received=("Credit Amount", "sum")
).reset_index()

customer_monthly.to_excel("customer_monthly_trend.xlsx", index=False)
print("✔ Customer monthly trend generated")

print("🎉 Vendor & Customer analysis completed successfully")

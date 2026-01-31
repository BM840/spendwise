import pandas as pd
import matplotlib.pyplot as plt

print("DEBUG: Monthly & Category Trends started")

# ================= LOAD DATA =================
df = pd.read_excel("classified_output.xlsx")

# ================= BASIC CLEANING =================
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"])

df["Credit Amount"] = df["Credit Amount"].fillna(0)
df["Debit Amount"] = df["Debit Amount"].fillna(0)

# ================= MONTH COLUMN =================
df["Month"] = df["Date"].dt.to_period("M").astype(str)

# ==================================================
# 1️⃣ MONTHLY TOTALS (CREDIT / DEBIT / P&L)
# ==================================================
monthly_totals = df.groupby("Month").agg(
    Total_Credit=("Credit Amount", "sum"),
    Total_Debit=("Debit Amount", "sum")
).reset_index()

monthly_totals["Profit / Loss"] = (
    monthly_totals["Total_Credit"] - monthly_totals["Total_Debit"]
)

monthly_totals.to_excel("monthly_totals.xlsx", index=False)
print("✔ Monthly totals generated")

# ==================================================
# 2️⃣ MONTHLY CATEGORY-WISE DEBIT TRENDS
# ==================================================
category_monthly = df[df["Debit Amount"] > 0].groupby(
    ["Month", "Category"]
).agg(
    Monthly_Spend=("Debit Amount", "sum")
).reset_index()

category_monthly.to_excel("monthly_category_trends.xlsx", index=False)
print("✔ Monthly category trends generated")

# ==================================================
# 3️⃣ OVERALL CATEGORY SUMMARY
# ==================================================
category_summary = df[df["Debit Amount"] > 0].groupby(
    "Category"
).agg(
    Total_Spend=("Debit Amount", "sum"),
    Transaction_Count=("Debit Amount", "count")
).reset_index()

category_summary = category_summary.sort_values(
    by="Total_Spend", ascending=False
)

category_summary.to_excel("category_summary.xlsx", index=False)
print("✔ Category summary generated")

# ==================================================
# 4️⃣ OPTIONAL: CATEGORY SHARE PIE CHART
# ==================================================
plt.figure()
plt.pie(
    category_summary["Total_Spend"],
    labels=category_summary["Category"],
    autopct="%1.1f%%"
)
plt.title("Category-wise Expense Share")
plt.tight_layout()
plt.savefig("category_share.png")
plt.close()

print("✔ Category share chart saved")

print("🎉 Monthly & Category Trends completed")

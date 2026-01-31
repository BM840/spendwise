import pandas as pd
import matplotlib.pyplot as plt

print("DEBUG: reports.py started")

# ---------- LOAD DATA ----------
df = pd.read_excel("classified_output.xlsx")
print("DEBUG: file loaded")

# ---------- SAFE DATE PARSING ----------
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Remove non-transaction rows
df = df.dropna(subset=["Date"])
print("DEBUG: invalid date rows removed")

# ---------- MONTH COLUMN ----------
df["Month"] = df["Date"].dt.to_period("M")

# ---------- MONTHLY TOTALS ----------
monthly_summary = df.groupby("Month").agg({
    "Credit Amount": "sum",
    "Debit Amount": "sum"
}).reset_index()

print("DEBUG: monthly_summary created")

# ---------- PROFIT & LOSS ----------
monthly_summary["Profit / Loss"] = (
    monthly_summary["Credit Amount"] - monthly_summary["Debit Amount"]
)

monthly_summary.to_excel("profit_loss.xlsx", index=False)
print("✔ Profit & Loss report generated")

# ---------- CREDIT vs DEBIT CHART ----------
plt.figure()
plt.plot(
    monthly_summary["Month"].astype(str),
    monthly_summary["Credit Amount"],
    label="Credit"
)
plt.plot(
    monthly_summary["Month"].astype(str),
    monthly_summary["Debit Amount"],
    label="Debit"
)

plt.xlabel("Month")
plt.ylabel("Amount")
plt.title("Monthly Credit vs Debit")
plt.legend()
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig("credit_vs_debit.png")
plt.close()

print("✔ Credit vs Debit chart saved")

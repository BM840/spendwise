import pandas as pd

# ================= LOAD DATA =================
df = pd.read_excel("classified_output.xlsx")

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Month"] = df["Date"].dt.to_period("M")

alerts = []

# ================= 1️⃣ HIGH VALUE TRANSACTIONS =================
avg_debit = df["Debit Amount"].mean()
threshold = avg_debit * 3

high_txns = df[df["Debit Amount"] > threshold]

for _, row in high_txns.iterrows():
    alerts.append({
        "Type": "High Transaction",
        "Date": row["Date"],
        "Description": row["Description"],
        "Amount": row["Debit Amount"],
        "Reason": "Amount is unusually high compared to average spending"
    })

# ================= 2️⃣ VENDOR SPIKE =================
vendor_monthly = (
    df[df["Debit Amount"] > 0]
    .groupby(["Month", "Description"])["Debit Amount"]
    .sum()
    .reset_index()
)

vendor_avg = (
    vendor_monthly
    .groupby("Description")["Debit Amount"]
    .mean()
    .reset_index()
    .rename(columns={"Debit Amount": "Avg"})
)

vendor_spike = vendor_monthly.merge(vendor_avg, on="Description")

spikes = vendor_spike[vendor_spike["Debit Amount"] > 2 * vendor_spike["Avg"]]

for _, row in spikes.iterrows():
    alerts.append({
        "Type": "Vendor Spike",
        "Date": row["Month"].to_timestamp(),
        "Description": row["Description"],
        "Amount": row["Debit Amount"],
        "Reason": "Vendor spending spiked unusually this month"
    })

# ================= 3️⃣ CATEGORY SPIKE =================
category_monthly = (
    df[df["Debit Amount"] > 0]
    .groupby(["Month", "Category"])["Debit Amount"]
    .sum()
    .reset_index()
)

category_avg = (
    category_monthly
    .groupby("Category")["Debit Amount"]
    .mean()
    .reset_index()
    .rename(columns={"Debit Amount": "Avg"})
)

category_spike = category_monthly.merge(category_avg, on="Category")

cat_spikes = category_spike[category_spike["Debit Amount"] > 1.5 * category_spike["Avg"]]

for _, row in cat_spikes.iterrows():
    alerts.append({
        "Type": "Category Spike",
        "Date": row["Month"].to_timestamp(),
        "Description": row["Category"],
        "Amount": row["Debit Amount"],
        "Reason": "Category expense increased sharply this month"
    })

# ================= SAVE ALERTS =================
alerts_df = pd.DataFrame(alerts)
alerts_df.to_excel("alerts.xlsx", index=False)

print("✔ Anomaly alerts generated")

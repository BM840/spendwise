import pandas as pd

# ================= CONFIG =================
DATE_GAP_DAYS = 30
DATE_TOLERANCE = 5        # ±5 days
AMOUNT_TOLERANCE = 0.10   # ±10%

# ================= LOAD DATA =================
df = pd.read_excel("classified_output.xlsx")

# Ensure Date is datetime
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"])

# Sort for time comparison
df = df.sort_values(by=["Description", "Date"])

# ================= RECURRING LOGIC =================
df["Is Recurring"] = False
df["Recurring Reason"] = ""

group_cols = ["Description", "Category"]

for _, group in df.groupby(group_cols):
    if len(group) < 2:
        continue

    dates = group["Date"].reset_index(drop=True)
    amounts = group["Credit Amount"] + group["Debit Amount"]

    for i in range(1, len(group)):
        date_gap = (dates[i] - dates[i - 1]).days
        amt_prev = amounts.iloc[i - 1]
        amt_curr = amounts.iloc[i]

        if amt_prev == 0:
            continue

        amt_diff_ratio = abs(amt_curr - amt_prev) / amt_prev

        if (
            abs(date_gap - DATE_GAP_DAYS) <= DATE_TOLERANCE
            and amt_diff_ratio <= AMOUNT_TOLERANCE
        ):
            idx = group.index[i]
            df.at[idx, "Is Recurring"] = True
            df.at[idx, "Recurring Reason"] = "Monthly pattern detected"

# ================= SAVE =================
df.to_excel("classified_with_recurring.xlsx", index=False)
print("✔ Recurring transactions detected and saved")

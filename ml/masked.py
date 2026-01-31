import pandas as pd

# ================= AMOUNT MASKING =================
def mask_amount(val):
    if pd.isna(val) or val == 0:
        return 0
    if val < 1000:
        return "<1K"
    if val < 10000:
        return "1K-10K"
    if val < 50000:
        return "10K-50K"
    return ">50K"

# ================= MAIN MASK FUNCTION =================
def apply_masking(df):
    masked_df = df.copy()

    if "Credit Amount" in masked_df.columns:
        masked_df["Credit Amount Masked"] = masked_df["Credit Amount"].apply(mask_amount)

    if "Debit Amount" in masked_df.columns:
        masked_df["Debit Amount Masked"] = masked_df["Debit Amount"].apply(mask_amount)

    # Remove real amounts for privacy
    masked_df.drop(
        columns=[c for c in ["Credit Amount", "Debit Amount"] if c in masked_df.columns],
        inplace=True
    )

    return masked_df

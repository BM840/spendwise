import os
import pandas as pd
import joblib
import re

from ml.parser import parse_transaction
from ml.category_refiner import refine_category
from ml.masked import apply_masking

# ================= CONFIG =================
REVIEW_THRESHOLD = 0.60
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ================= LOAD ML =================
MODEL_PATH = os.path.join("ml", "model.pkl")
VECTORIZER_PATH = os.path.join("ml", "vectorizer.pkl")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

# ================= TEXT FOR ML =================
def clean_text_for_ml(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ================= ML =================
def ml_predict(text):
    vec = vectorizer.transform([text])
    pred = model.predict(vec)[0]
    prob = max(model.predict_proba(vec)[0])
    return pred, round(prob, 2)

# ================= RULE ENGINE =================
def rule_based_category(txn_type, action):
    action = action.lower()

    if txn_type == "CR":
        return "Sales", 1.00, False, "Credit transaction"

    if "rent" in action:
        return "Rent", 1.00, False, "Matched rent keyword"
    if "salary" in action:
        return "Salary", 1.00, False, "Matched salary keyword"
    if "gst" in action or "tax" in action:
        return "Tax", 1.00, False, "Matched tax keyword"
    if "charge" in action:
        return "Bank Charges", 1.00, False, "Matched bank charge keyword"

    return None, None, None, None

# ================= HEADER DETECTION =================
def find_header_row(file_path):
    temp = pd.read_excel(file_path, header=None)
    for i, row in temp.iterrows():
        row_str = " ".join(str(x).lower() for x in row if pd.notna(x))
        if "date" in row_str and "amount" in row_str:
            return i
    raise Exception("Could not detect header row")

def get_remarks_column(df):
    for col in df.columns:
        if col.lower() in {
            "remarks", "narration", "description",
            "transaction details", "transaction remarks"
        }:
            return col
    raise Exception("Narration column not found")

def get_amount_column(df):
    for col in df.columns:
        if "amount" in col.lower():
            return col
    raise Exception("Amount column not found")

# ================= CORE FUNCTION =================
def process_excel(uploaded_file_path: str):
    """
    MAIN ENTRY POINT
    Called from Streamlit with uploaded file path
    """

    header_row = find_header_row(uploaded_file_path)
    df = pd.read_excel(uploaded_file_path, header=header_row)

    remarks_col = get_remarks_column(df)
    amount_col = get_amount_column(df)

    results = []

    for _, row in df.iterrows():
        raw_desc = row.get(remarks_col, "")
        txn_type = str(row.get("Type", "")).upper()

        parsed = parse_transaction(raw_desc)

        mode = parsed["mode"]
        counterparty = parsed["counterparty"]
        action = parsed["action"]

        display_desc = f"{mode} - {counterparty}"

        ml_text = clean_text_for_ml(f"{mode} {counterparty} {action}")

        # ---------- RULE → ML ----------
        category, confidence, needs_review, reason = rule_based_category(
            txn_type, action
        )

        if category is None:
            category, confidence = ml_predict(ml_text)
            needs_review = confidence < REVIEW_THRESHOLD
            reason = "ML prediction"

        # ---------- CATEGORY REFINEMENT ----------
        final_category = refine_category(category, raw_desc)

        # ---------- CREDIT / DEBIT ----------
        credit = row[amount_col] if txn_type == "CR" else 0
        debit = row[amount_col] if txn_type != "CR" else 0

        results.append({
            "Date": row.get("Date"),
            "Description": display_desc,
            "Credit Amount": credit,
            "Debit Amount": debit,
            "Category": final_category,
            "Confidence": confidence,
            "Needs Review": needs_review,
            "Decision Source": reason
        })

    result_df = pd.DataFrame(results)

    # ================= SAVE OUTPUTS =================
    classified_path = os.path.join(OUTPUT_DIR, "classified_output.xlsx")
    masked_path = os.path.join(OUTPUT_DIR, "classified_output_masked.xlsx")
    pl_path = os.path.join(OUTPUT_DIR, "profit_loss.xlsx")

    result_df.to_excel(classified_path, index=False)
    apply_masking(result_df).to_excel(masked_path, index=False)

    # Profit & Loss
    pl_df = result_df.copy()
    pl_df["Month"] = pd.to_datetime(pl_df["Date"], errors="coerce").dt.to_period("M")
    pl_summary = pl_df.groupby("Month")[["Credit Amount", "Debit Amount"]].sum()
    pl_summary["Profit / Loss"] = (
        pl_summary["Credit Amount"] - pl_summary["Debit Amount"]
    )
    pl_summary.reset_index().to_excel(pl_path, index=False)

    return {
        "classified": classified_path,
        "masked": masked_path,
        "profit_loss": pl_path
    }

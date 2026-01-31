import re
import pandas as pd

def parse_transaction(text):
    if pd.isna(text):
        return {
            "mode": "UNKNOWN",
            "bank": "",
            "counterparty": "Unknown",
            "action": "",
            "raw": ""
        }

    raw = str(text).strip()
    upper = raw.upper()

    result = {
        "mode": "UNKNOWN",
        "bank": "",
        "counterparty": "Unknown",
        "action": "",
        "raw": raw
    }

    # ---------- MODE ----------
    MODES = {"UPI", "NEFT", "IMPS", "RTGS"}
    for m in MODES:
        if m in upper:
            result["mode"] = m
            break

    # ---------- TOKENS ----------
    tokens = [t.strip() for t in re.split(r"[\/\-]", raw) if len(t.strip()) > 1]
    tokens_upper = [t.upper() for t in tokens]

    # ---------- BANK ----------
    for t in tokens_upper:
        if (
            t.isalpha()
            and t not in MODES
            and len(t) <= 6
        ):
            result["bank"] = t
            break

    # ---------- ACTION ----------
    ACTIONS = {
        "PAYMENT", "RENT", "SALARY", "EMI",
        "BILL", "GST", "TAX", "CHARGE", "TRANSFER"
    }

    for t in tokens_upper:
        if t in ACTIONS:
            result["action"] = t.capitalize()
            break

    # ---------- COUNTERPARTY ----------
    blacklist = MODES | ACTIONS | {
        result["bank"], "BANK", "INDIA", "LIMITED", "LTD"
    }

    for t in tokens:
        clean = re.sub(r"[^A-Za-z ]", "", t).strip()
        if (
            len(clean) >= 3
            and clean.upper() not in blacklist
            and not clean.isdigit()
        ):
            result["counterparty"] = clean.title()
            break

    return result

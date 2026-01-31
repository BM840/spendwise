def refine_category(base_category, raw_text):
    if not isinstance(raw_text, str):
        return base_category

    text = raw_text.lower()
    # ---------- BANK CHARGES ----------
    if any(k in text for k in ["charge", "fee", "penalty", "gst on charges"]):
     return "Bank Charges"

    # ---------- UTILITIES SPLIT ----------
    if base_category == "Utilities":

        internet_keywords = [
            "jio", "airtel", "vi", "voda", "fiber",
            "broadband", "wifi", "isp", "net"
        ]

        electricity_keywords = [
            "electricity", "power", "bijli", "discom",
            "electric", "eb", "energy"
        ]

        mobile_keywords = [
            "mobile", "recharge", "prepaid",
            "postpaid", "sim"
        ]

        subscription_keywords = [
            "netflix", "prime", "spotify",
            "hotstar", "zee", "sonyliv"
        ]

        software_keywords = [
            "aws", "azure", "gcp", "github",
            "hosting", "server", "cloud"
        ]

        if any(k in text for k in internet_keywords):
            return "Internet"

        if any(k in text for k in electricity_keywords):
            return "Electricity"

        if any(k in text for k in mobile_keywords):
            return "Mobile"

        if any(k in text for k in subscription_keywords):
            return "Subscriptions"

        if any(k in text for k in software_keywords):
            return "Software"

        return "Other Utilities"


    # ---------- OPERATIONS ----------
    if base_category == "Rent":
        return "Office Rent"

    if base_category == "Salary":
        return "Employee Salary"

    # ---------- FINANCE ----------
    if base_category == "Bank Charges":
        return "Bank Charges"

    if base_category == "Tax":
        return "Tax & GST"

    # ---------- SALES ----------
    if base_category == "Sales":
        return "Sales Revenue"

    return base_category

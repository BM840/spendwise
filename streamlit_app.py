import streamlit as st
import pandas as pd
from ml.process_bank_excel import process_excel
from ml.dashboard_logic import render_dashboard
import os

st.set_page_config(page_title="SpendWise", layout="wide")
st.title("💰 SpendWise")
st.caption("Smart insights from your bank statements")

uploaded_file = st.file_uploader(
    "📤 Upload Bank Statement (Excel)",
    type=["xlsx", "xls"]
)

if uploaded_file is not None:
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    input_path = f"uploads/{uploaded_file.name}"

    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("Processing bank statement..."):
        paths = process_excel(input_path)

    df = pd.read_excel(paths["classified"])

    # ✅ CALL DASHBOARD ONCE
    render_dashboard(df)

else:
    st.info("Please upload a bank statement to begin.")

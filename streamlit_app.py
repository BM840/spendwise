import streamlit as st
import pandas as pd
import os

from ml.process_bank_excel import process_excel
from ml.dashboard_logic import render_dashboard

# ================= APP CONFIG =================
st.set_page_config(page_title="SpendWise", layout="wide")
st.title("💰 SpendWise")
st.caption("Smart insights from your bank statements")

st.divider()

# ================= PATH SETUP (CRITICAL FIX) =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
DEMO_FILE = os.path.join(BASE_DIR, "demo", "spendwise_demo_statement.xlsx")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ================= DEMO OR UPLOAD =================
col1, col2 = st.columns([1, 1])
use_demo = False

with col1:
    uploaded_file = st.file_uploader(
        "📤 Upload Bank Statement (Excel)",
        type=["xlsx", "xls"]
    )

with col2:
    st.markdown("### 👀 Just exploring?")
    if st.button("🚀 Try Demo Data"):
        use_demo = True

# ================= PROCESS =================
if uploaded_file is not None or use_demo:

    if use_demo:
        if not os.path.exists(DEMO_FILE):
            st.error("Demo file not found. Please redeploy the app.")
            st.stop()

        input_path = DEMO_FILE
        st.success("Using demo bank statement")

    else:
        input_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("File uploaded successfully")

    with st.spinner("Analyzing transactions..."):
        paths = process_excel(input_path)

    df = pd.read_excel(paths["classified"])
    render_dashboard(df)

else:
    st.info("Upload a bank statement or try demo data to get started.")

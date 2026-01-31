import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import zipfile
import io


# ================= DOWNLOAD HELPER =================
def download_button(label, file_path, mime):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            st.download_button(
                label=label,
                data=f,
                file_name=os.path.basename(file_path),
                mime=mime
            )
    else:
        st.caption(f"❌ {label} not available yet")


# ================= MAIN DASHBOARD =================
def render_dashboard(df: pd.DataFrame):

    # ================= BASIC CLEANING =================
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)

    # ================= KPI CARDS =================
    st.subheader("📊 Financial Overview")

    total_credit = df["Credit Amount"].sum()
    total_debit = df["Debit Amount"].sum()
    profit_loss = total_credit - total_debit

    k1, k2, k3 = st.columns(3)

    k1.markdown(
        f"""<div style="padding:20px;border-radius:14px;background:#0f172a;text-align:center;">
        <h4>💰 Total Credit</h4>
        <h2 style="color:#22c55e;">₹ {total_credit:,.0f}</h2>
        </div>""",
        unsafe_allow_html=True
    )

    k2.markdown(
        f"""<div style="padding:20px;border-radius:14px;background:#0f172a;text-align:center;">
        <h4>💸 Total Debit</h4>
        <h2 style="color:#ef4444;">₹ {total_debit:,.0f}</h2>
        </div>""",
        unsafe_allow_html=True
    )

    k3.markdown(
        f"""<div style="padding:20px;border-radius:14px;background:#0f172a;text-align:center;">
        <h4>📈 Profit / Loss</h4>
        <h2 style="color:#38bdf8;">₹ {profit_loss:,.0f}</h2>
        </div>""",
        unsafe_allow_html=True
    )

    # ================= ZIP DOWNLOAD =================
    st.divider()
    st.subheader("📦 Download All Reports")

    zip_buffer = io.BytesIO()

    files_to_zip = {
        "classified_output.xlsx": "outputs/classified_output.xlsx",
        "classified_output_masked.xlsx": "outputs/classified_output_masked.xlsx",
        "profit_loss.xlsx": "outputs/profit_loss.xlsx",
    }

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for zip_name, file_path in files_to_zip.items():
            if os.path.exists(file_path):
                zipf.write(file_path, arcname=zip_name)

    zip_buffer.seek(0)

    st.download_button(
        label="⬇ Download All Reports (ZIP)",
        data=zip_buffer,
        file_name="finance_reports.zip",
        mime="application/zip"
    )

    # ================= MONTHLY CREDIT vs DEBIT =================
    st.divider()
    st.subheader("📈 Monthly Credit vs Debit")

    monthly = (
        df.groupby("Month")[["Credit Amount", "Debit Amount"]]
        .sum()
        .reset_index()
    )

    col_chart, col_text = st.columns([2, 1])

    with col_chart:
        fig, ax = plt.subplots(figsize=(6, 3))  # 👈 SMALLER SIZE

        ax.plot(
            monthly["Month"],
            monthly["Credit Amount"],
            marker="o",
            linewidth=2,
            color="#22c55e",
            label="Credit"
        )

        ax.plot(
            monthly["Month"],
            monthly["Debit Amount"],
            marker="o",
            linewidth=2,
            color="#ef4444",
            label="Debit"
        )

        ax.set_ylabel("Amount (₹)")
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.xticks(rotation=45)
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)

    with col_text:
        st.markdown("### 💡 Insight")
        st.write("Compare income vs expenses month by month.")

    # ================= CATEGORY WISE EXPENSE =================
    st.divider()
    st.subheader("🧾 Category-wise Expense")

    expense_df = df[df["Debit Amount"] > 0]
    category_sum = expense_df.groupby("Category")["Debit Amount"].sum()

    if not category_sum.empty:
        category_sum = category_sum.sort_values(ascending=False).head(6)

        col_pie, col_info = st.columns([1, 1])

        with col_pie:
            fig, ax = plt.subplots(figsize=(4, 4))  # 👈 SMALL & CLEAN
            ax.pie(
                category_sum,
                labels=category_sum.index,
                autopct="%1.1f%%",
                startangle=90,
                wedgeprops={"edgecolor": "white"}
            )
            plt.tight_layout()
            st.pyplot(fig)

        with col_info:
            top_cat = category_sum.idxmax()
            pct = category_sum.max() / category_sum.sum() * 100
            st.markdown("### 💡 Insight")
            st.write(f"Highest spending is **{top_cat}** ({pct:.1f}%).")
    else:
        st.info("No expense data available.")

        # ================= CATEGORY TREND OVER TIME =================
    st.divider()
    st.subheader("📊 Category Spend Trend (Monthly)")

    expense_df = df[df["Debit Amount"] > 0]

    # Get top 3 categories by total spend
    top_categories = (
        expense_df.groupby("Category")["Debit Amount"]
        .sum()
        .sort_values(ascending=False)
        .head(3)
        .index
    )

    trend_df = (
        expense_df[expense_df["Category"].isin(top_categories)]
        .groupby(["Month", "Category"])["Debit Amount"]
        .sum()
        .reset_index()
    )

    col_chart, col_text = st.columns([2, 1])

    with col_chart:
        fig, ax = plt.subplots(figsize=(6, 3))

        for category in top_categories:
            cat_data = trend_df[trend_df["Category"] == category]
            ax.plot(
                cat_data["Month"],
                cat_data["Debit Amount"],
                marker="o",
                linewidth=2,
                label=category
            )

        ax.set_ylabel("Amount (₹)")
        ax.set_title("Top Category Spending Over Time", fontsize=13)
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.xticks(rotation=45)
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)

    with col_text:
        top_cat = top_categories[0]
        st.markdown("### 💡 Insight")
        st.write(
            f"**{top_cat}** is the highest spending category overall. "
            "Tracking this trend helps control long-term expenses."
        )


    # ================= TOP VENDORS =================
    st.divider()
    st.subheader("🏷 Top Vendors")

    vendor_df = expense_df.copy()
    vendor_df["Vendor"] = vendor_df["Description"].str.split("-").str[-1].str.strip()

    top_vendors = (
        vendor_df.groupby("Vendor")["Debit Amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    if not top_vendors.empty:
        fig, ax = plt.subplots(figsize=(8, 3.5))
        bars = ax.bar(top_vendors.index, top_vendors.values, color="#60a5fa")

        ax.set_ylabel("Amount (₹)")
        ax.set_title("Top Vendors by Spending", fontsize=14)
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.xticks(rotation=30, ha="right")

        for bar in bars:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                f"₹{int(bar.get_height()):,}",
                ha="center",
                va="bottom",
                fontsize=9
            )

        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.info("No vendor data available.")
            # ================= VENDOR FREQUENCY & GROWTH INSIGHTS =================
    st.divider()
    st.subheader("🏷 Vendor Frequency & Growth Insights")

    expense_df = df[df["Debit Amount"] > 0].copy()

    # Extract vendor
    expense_df["Vendor"] = (
        expense_df["Description"]
        .astype(str)
        .str.split("-")
        .str[-1]
        .str.strip()
    )

    # ---------------- Vendor Frequency ----------------
    vendor_freq = (
        expense_df.groupby("Vendor")
        .agg(
            transactions=("Debit Amount", "count"),
            total_spend=("Debit Amount", "sum")
        )
        .reset_index()
        .sort_values("transactions", ascending=False)
    )

    # ---------------- Vendor Monthly Spend ----------------
    monthly_vendor = (
        expense_df.groupby(["Vendor", "Month"])["Debit Amount"]
        .sum()
        .reset_index()
    )

    growth_records = []

    for vendor in monthly_vendor["Vendor"].unique():
        v_data = monthly_vendor[monthly_vendor["Vendor"] == vendor].sort_values("Month")
        if len(v_data) >= 2:
            start = v_data.iloc[0]["Debit Amount"]
            end = v_data.iloc[-1]["Debit Amount"]
            growth = ((end - start) / start) * 100 if start > 0 else 0
            growth_records.append((vendor, growth))

    growth_df = pd.DataFrame(growth_records, columns=["Vendor", "Growth %"])

    # ---------------- Insights ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔁 Most Frequent Vendors")
        for _, row in vendor_freq.head(5).iterrows():
            st.write(
                f"• **{row['Vendor']}** — "
                f"{row['transactions']} transactions, "
                f"₹{int(row['total_spend']):,} total"
            )

    with col2:
        st.markdown("### 📈 Fastest Growing Vendors")

        if not growth_df.empty:
            growth_df = growth_df.sort_values("Growth %", ascending=False).head(5)
            for _, row in growth_df.iterrows():
                arrow = "📈" if row["Growth %"] > 0 else "📉"
                st.write(
                    f"{arrow} **{row['Vendor']}** — "
                    f"{row['Growth %']:.1f}% change"
                )
        else:
            st.info("Not enough data to calculate vendor growth.")

    # ================= RECURRING TRANSACTIONS =================
    st.divider()
    st.subheader("🔁 Recurring Transactions")

    expense_df = df[df["Debit Amount"] > 0].copy()

    # Extract vendor cleanly
    expense_df["Vendor"] = (
        expense_df["Description"]
        .astype(str)
        .str.split("-")
        .str[-1]
        .str.strip()
    )

    # Group by Vendor + Category
    recurring = (
        expense_df
        .groupby(["Vendor", "Category"])
        .agg(
            months=("Month", "nunique"),
            avg_amount=("Debit Amount", "mean"),
            count=("Debit Amount", "count")
        )
        .reset_index()
    )

    # Recurring rule: appears in 3+ months
    recurring = recurring[recurring["months"] >= 3]

    if not recurring.empty:
        recurring = recurring.sort_values("months", ascending=False)

        st.markdown("### 🔍 Detected Recurring Expenses")

        for _, row in recurring.head(5).iterrows():
            st.write(
                f"🔁 **{row['Vendor']}** "
                f"({row['Category']}) — "
                f"₹{int(row['avg_amount']):,} avg, "
                f"appears in **{row['months']} months**"
            )
    else:
        st.success("No recurring expenses detected 🎉")


    # ================= ANOMALY DETECTION =================
    st.divider()
    st.subheader("⚠ Unusual Transactions")

    if not expense_df.empty:
        threshold = expense_df["Debit Amount"].mean() + 2 * expense_df["Debit Amount"].std()
        anomalies = expense_df[expense_df["Debit Amount"] > threshold]

        if not anomalies.empty:
            st.warning(f"{len(anomalies)} unusual transactions detected")
            st.dataframe(
                anomalies[["Date", "Description", "Debit Amount", "Category"]],
                use_container_width=True
            )
        else:
            st.success("No unusual spending detected 🎉")
    else:
        st.info("No debit transactions to analyze.")
            # ================= SMART INSIGHTS =================
    st.divider()
    st.subheader("🧠 Smart Financial Insights")

    insights = []

    # ---------- Category Insight ----------
    expense_df = df[df["Debit Amount"] > 0]

    if not expense_df.empty:
        category_sum = expense_df.groupby("Category")["Debit Amount"].sum()
        top_category = category_sum.idxmax()
        top_cat_pct = (category_sum.max() / category_sum.sum()) * 100
        insights.append(
            f"💸 Your highest spending category is **{top_category}**, "
            f"making up **{top_cat_pct:.1f}%** of total expenses."
        )

    # ---------- Vendor Frequency Insight ----------
    expense_df["Vendor"] = (
        expense_df["Description"]
        .astype(str)
        .str.split("-")
        .str[-1]
        .str.strip()
    )

    vendor_freq = expense_df["Vendor"].value_counts()

    if not vendor_freq.empty:
        top_vendor = vendor_freq.idxmax()
        top_vendor_count = vendor_freq.max()
        insights.append(
            f"🏷 **{top_vendor}** is your most frequent vendor "
            f"with **{top_vendor_count} transactions**."
        )

    # ---------- Recurring Insight ----------
    recurring_check = (
        expense_df.groupby(["Vendor", "Category"])
        .agg(months=("Month", "nunique"))
        .reset_index()
    )

    recurring_found = recurring_check[recurring_check["months"] >= 3]

    if not recurring_found.empty:
        row = recurring_found.iloc[0]
        insights.append(
            f"🔁 **{row['Vendor']}** appears regularly across months "
            f"— likely a recurring expense."
        )

    # ---------- Spending Trend Insight ----------
    monthly_spend = (
        expense_df.groupby("Month")["Debit Amount"]
        .sum()
        .reset_index()
    )

    if len(monthly_spend) >= 2:
        last = monthly_spend.iloc[-1]["Debit Amount"]
        prev = monthly_spend.iloc[-2]["Debit Amount"]

        if last > prev:
            change = ((last - prev) / prev) * 100 if prev > 0 else 0
            insights.append(
                f"📈 Your spending increased by **{change:.1f}%** "
                f"in the most recent month."
            )
        else:
            insights.append(
                "📉 Your spending decreased compared to the previous month."
            )

    # ---------- Anomaly Insight ----------
    threshold = expense_df["Debit Amount"].mean() + 2 * expense_df["Debit Amount"].std()
    anomalies = expense_df[expense_df["Debit Amount"] > threshold]

    if not anomalies.empty:
        insights.append(
            f"⚠ You had **{len(anomalies)} unusually high transactions** "
            f"that may need review."
        )

    # ---------- Display Insights ----------
    if insights:
        for insight in insights:
            st.write("• " + insight)
    else:
        st.success("Your finances look stable with no major concerns detected 🎉")


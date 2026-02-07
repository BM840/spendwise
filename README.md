# 💰 SpendWise – Smart Personal Finance Analyzer

SpendWise is a privacy-first web application that analyzes bank statements to deliver
clear insights into spending habits, trends, and unusual transactions.

🔗 **Live Demo:**  
https://spendwise-aedappr64t9iudf9mdvscjr.streamlit.app/

---

## 🚀 Key Features

- 📊 Financial overview: total credit, debit, and profit/loss
- 📈 Monthly credit vs debit trends
- 🧾 Category-wise spending analysis
- 🏷 Vendor-wise expense breakdown
- 🚨 Anomaly detection for high-value transactions
- 🧪 Demo mode (try without uploading personal data)
- 🔐 Privacy-first design (no permanent data storage)

---

## 🧠 How SpendWise Works

1. User uploads a bank statement (Excel) or selects **Demo Mode**
2. Transactions are parsed and normalized
3. A hybrid **rule-based + ML classifier** assigns categories
4. Recurring patterns and anomalies are detected
5. Interactive dashboards visualize insights
6. Reports are generated for download

---

## 🤖 Machine Learning Approach

- Text-based transaction classification
- Rule-based refinement for higher accuracy
- ML predictions enhanced with domain heuristics
- Focus on explainability and consistency
- Anomaly detection using statistical thresholds

---

## 🧪 Demo Mode

- Uses a synthetic bank statement
- No login required
- No personal data uploaded
- Ideal for recruiters and first-time users

---

## 🔐 Privacy & Security

- No data stored permanently
- Files processed only during session
- Demo data avoids real financial information
- No credentials required

---

## 🛠 Tech Stack

**Frontend / UI:**  
- Streamlit

**Backend / Processing:**  
- Python, Pandas

**Machine Learning:**  
- Scikit-learn

**Visualization:**  
- Matplotlib

**Version Control & Deployment:**  
- Git & GitHub  
- Streamlit Cloud (CI/CD)

---

## ▶️ Run Locally

```bash
git clone https://github.com/BM840/spendwise.git
cd spendwise
pip install -r requirements.txt
streamlit run streamlit_app.py

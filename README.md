💰 SpendWise – Smart Personal Finance Analyzer

SpendWise is a privacy-first, ML-powered web application that transforms raw bank statements into clear, actionable financial insights.
It helps users understand spending patterns, income trends, and unusual transactions without sharing bank credentials.

🚀 Live Demo

🔗 Try SpendWise here:
👉 https://spendwise-aedappr64t9iudf9mdvscjr.streamlit.app/

🔗 GitHub Repository:
👉 https://github.com/BM840/spendwise

✨ Key Features

📤 Upload bank statements in Excel format

👀 Try Demo Mode (explore without uploading personal data)

🧠 Hybrid transaction classification

Rule-based logic for known patterns

Machine Learning for intelligent categorization

📊 Interactive dashboard with:

Total Credit, Debit & Profit/Loss

Monthly Credit vs Debit trends

Category-wise spending analysis

Top vendor analysis

Unusual / high-value transaction detection

⬇ Download processed financial reports

🔒 Privacy-first design (no credentials, no permanent storage)

🧩 How SpendWise Works (Workflow)

User uploads a bank statement (Excel) or clicks Try Demo Data

System automatically detects headers and relevant columns

Transactions are parsed and normalized

Rule-based logic classifies obvious transactions (salary, rent, tax, etc.)

ML model predicts categories for remaining transactions

Category refinement improves accuracy and consistency

Aggregated insights are visualized on an interactive dashboard

Processed reports are generated for download

🤖 Machine Learning Approach

Supervised text classification model trained on labeled transaction descriptions

Text preprocessing includes cleaning and vectorization

ML predictions are combined with deterministic rules to:

Improve accuracy

Increase explainability

Reduce misclassification

Confidence scoring helps flag low-certainty transactions for review

📊 Dashboard Insights

SpendWise provides:

💰 Financial Overview – total credit, debit, and profit/loss

📈 Monthly Trends – income vs expenses over time

🧾 Category-wise Spending – expense distribution

🏷 Top Vendors – highest spending entities

⚠ Anomaly Detection – unusually high debit transactions

🧪 Demo Mode

SpendWise includes a built-in demo bank statement, allowing users to:

Instantly explore features

Test the app during interviews or demos

Avoid uploading personal or sensitive financial data

This makes SpendWise ideal for demonstrations and portfolio reviews.

🔐 Privacy & Security

No bank credentials required

No permanent data storage

Files are processed only during the active session

Password-protected PDFs are intentionally not auto-unlocked to maintain security and compliance

Users retain full control over their data

🛠 Technology Stack

Frontend / UI: Streamlit

Backend / Processing: Python, Pandas

Machine Learning: Scikit-learn

Visualization: Matplotlib

Version Control: Git & GitHub

Deployment: Streamlit Cloud

▶️ Run Locally
git clone https://github.com/BM840/spendwise.git
cd spendwise
pip install -r requirements.txt
streamlit run streamlit_app.py


Then open:

http://localhost:8501

🚀 Deployment

Repository connected to Streamlit Cloud

Automatic redeployment on every git push

Public URL available for anyone to test

🔮 Future Enhancements

Support for password-protected PDFs (user-provided password)

Recurring transaction detection UI

PDF executive financial reports

Editable and learning-based categories

Multi-profile support

👤 Author

Bharat Maheshwari
📧 bharatmaheshwari084@gmail.com

🔗 LinkedIn

💻 GitHub

⭐ If you like this project, consider starring the repository!

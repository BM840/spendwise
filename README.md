💰 SpendWise – Smart Personal Finance Analyzer



SpendWise is a privacy-first, ML-powered web application that helps users understand their bank statements by transforming raw transaction data into clear, actionable financial insights.



Users can upload their bank statements (Excel) or explore the app using demo data, without sharing any bank credentials.



🚀 Live Demo



🔗 Live App:



https://spendwise-xxxx.streamlit.app





🔗 GitHub Repository:



https://github.com/BM840/spendwise



✨ Key Features



📤 Upload bank statements in Excel format



🧠 Hybrid transaction classification (Rule-based + Machine Learning)



📊 Interactive dashboards:



Total Credit, Debit \& Profit/Loss



Monthly Credit vs Debit trends



Category-wise spending analysis



Top vendor analysis



Unusual / high-value transaction detection



👀 Demo Mode – explore the app without uploading personal data



🔒 Privacy-first design (no bank credentials required)



🧩 How It Works (Workflow)



User uploads a bank statement (Excel) or selects Try Demo Data



Header and column detection adapts to different bank formats



Transactions are parsed and normalized



Rule-based logic handles obvious cases (salary, rent, tax, etc.)



Machine Learning model predicts categories for remaining transactions



Category refinement improves accuracy



Aggregated insights are visualized on an interactive dashboard



Processed reports can be downloaded



🤖 Machine Learning Approach



Supervised text classification model trained on labeled transaction descriptions



Text preprocessing includes cleaning and vectorization



ML predictions are combined with deterministic rules to:



Improve accuracy



Increase explainability



Reduce misclassification



Confidence scoring helps flag low-certainty transactions



📊 Dashboard Insights



The dashboard provides:



💰 Financial Overview – total credit, debit, and profit/loss



📈 Monthly Trends – income vs expenses over time



🧾 Category-wise Spending – expense distribution



🏷 Top Vendors – highest spending entities



⚠ Anomaly Detection – unusually high debit transactions



🧪 Demo Mode



SpendWise includes a built-in demo bank statement, allowing users to:



Test the app instantly



Explore features during interviews or demos



Avoid uploading personal or sensitive data



This makes SpendWise ideal for demonstrations and portfolio reviews.



🔐 Privacy \& Security



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



Version Control: Git \& GitHub



Deployment: Streamlit Cloud



▶️ Run Locally

git clone https://github.com/BM840/spendwise.git

cd spendwise

pip install -r requirements.txt

streamlit run streamlit\_app.py





Open in browser:



http://localhost:8501



🚀 Deployment



Repository connected to Streamlit Cloud



Automatic redeployment on every git push



Public URL available for testing and sharing



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



⭐ If you find this project useful, consider starring the repository!


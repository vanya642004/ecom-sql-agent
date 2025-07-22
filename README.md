# 🛒 E-commerce AI SQL Agent

An AI-powered Streamlit app that answers questions about your product-level e-commerce metrics using natural language.

## 📦 Features
- Converts user questions into SQL with Gemini Pro
- Queries SQLite DB of e-commerce metrics
- Displays tabular answers + optional charts
- Fully deployable to Streamlit Cloud

## 📁 Files Included
- `ecom.db` – SQLite database
- `ad_sales.csv`, `total_sales.csv`, `eligibility.csv` – Source data
- `streamlit_app.py` – Main app
- `query_engine.py` – LLM-to-SQL engine
- `visualizer.py` – Plotly chart builder
- `requirements.txt` – Python dependencies

## 🚀 Deployment

1. **Create GitHub Repo**
2. Upload all files:
   - `ecom.db`
   - 3 CSVs
   - All `.py` files
   - `requirements.txt`
3. Go to [Streamlit Cloud](https://streamlit.io/cloud)
4. Connect your GitHub → Deploy repo
5. Set Gemini API key via Secrets:
   - `GEMINI_API_KEY = your_api_key`

## 🧪 Example Questions
- What is my total sales?
- Calculate the RoAS (Return on Ad Spend).
- Which product had the highest CPC?

---

Made with 💡 for Generative AI innovation.

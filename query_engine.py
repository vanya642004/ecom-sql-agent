import os
import sqlite3
import pandas as pd
import requests

# Prompt → SQL using OpenRouter LLM
def prompt_to_sql(prompt):
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "mistralai/mixtral-8x7b",  # You can switch to Claude, LLaMA, etc.
        "messages": [
            {
                "role": "system",
                "content": """You are a helpful assistant. Convert the user's question into a syntactically correct SQLite SQL query using:
- ad_sales(date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold)
- total_sales(date, item_id, total_sales, total_units_ordered)
- eligibility(eligibility_datetime_utc, item_id, eligibility, message)
Only return the SQL query."""
            },
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
        result = response.json()
        return result["choices"][0]["message"]["content"].strip("```sql").strip("```")
    except Exception as e:
        print("OpenRouter error:", e)
        return "SELECT 'OpenRouter API failed' AS error;"


# SQL → Pandas DataFrame
def run_sql(sql):
    try:
        conn = sqlite3.connect("ecom.db")  # relative path for GitHub/Streamlit Cloud
        df = pd.read_sql_query(sql, conn)
        conn.close()
        return df
    except Exception as e:
        print("SQLite error:", e)
        return pd.DataFrame()


# Final connector for streamlit_app.py
def ask_question(question):
    sql = prompt_to_sql(question)
    df = run_sql(sql)

    if df.empty:
        answer = "No data found."
    else:
        answer = f"Found {len(df)} rows."

    return answer, sql, df

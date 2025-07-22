import sqlite3
import pandas as pd
import requests

DB_PATH = "ecom.db"  # Use relative path in repo
GEMINI_API_KEY = "YOUR_API_KEY"  # Replace in Streamlit secrets or use env var

def prompt_to_sql(prompt):
    system_instruction = """
    You are a helpful data analyst. Convert the following natural language question
    into a syntactically correct SQLite query based on these tables:
    - ad_sales(date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold)
    - total_sales(date, item_id, total_sales, total_units_ordered)
    - eligibility(eligibility_datetime_utc, item_id, eligibility, message)
    Only return the SQL query and nothing else.
    """
    payload = {
        "contents": [{"parts": [{"text": f"{system_instruction}\n\nQ: {prompt}"}]}]
    }
    response = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
        headers={"Content-Type": "application/json"},
        params={"key": GEMINI_API_KEY},
        json=payload,
    )
    text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
    return text.strip().strip("```sql").strip("```")

def run_sql(sql):
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(sql, conn)
    except Exception as e:
        df = pd.DataFrame()
    conn.close()
    return df

def ask_question(question):
    sql = prompt_to_sql(question)
    df = run_sql(sql)

    if df.empty:
        answer = "No data found or invalid query."
    else:
        answer = f"Found {len(df)} rows."

    return answer, sql, df

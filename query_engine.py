import os
import sqlite3
import pandas as pd
import requests

# Convert question → SQL using OpenRouter
def prompt_to_sql(prompt):
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    if not OPENROUTER_API_KEY:
        print("❌ OPENROUTER_API_KEY is missing.")
        return "SELECT 'Missing OpenRouter API key' AS error;"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "anthropic/claude-3-sonnet",  # Let OpenRouter pick the best working model
        "messages": [
            {
                "role": "system",
                "content": """You are a helpful SQL assistant. Convert the user's question into a syntactically correct SQLite SQL query using:
- ad_sales(date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold)
- total_sales(date, item_id, total_sales, total_units_ordered)
- eligibility(eligibility_datetime_utc, item_id, eligibility, message)
ONLY return the SQL query. No explanation."""
            },
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
        json_data = response.json()

        if "choices" in json_data:
            sql_text = json_data["choices"][0]["message"]["content"]
            return sql_text.strip("```sql").strip("```")

        print("❌ OpenRouter failed response:", json_data)
        return "SELECT 'OpenRouter API failed - check key/quota/model' AS error;"

    except Exception as e:
        print("❌ OpenRouter Exception:", e)
        return "SELECT 'OpenRouter request crashed' AS error;"


# Run SQL on the database
def run_sql(sql):
    try:
        conn = sqlite3.connect("ecom.db")
        df = pd.read_sql_query(sql, conn)
        conn.close()
        return df
    except Exception as e:
        print("❌ SQLite Error:", e)
        return pd.DataFrame()


# Main agent function
def ask_question(question):
    sql = prompt_to_sql(question)
    df = run_sql(sql)

    if df.empty:
        answer = "No data found."
    else:
        answer = f"Found {len(df)} rows."

    return answer, sql, df

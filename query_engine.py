import os

def prompt_to_sql(prompt):
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "mistralai/mixtral-8x7b",  # You can change model (Claude, LLaMA3, etc.)
        "messages": [
            {
                "role": "system",
                "content": """You are a helpful SQL assistant. Convert the user's question into a syntactically correct SQLite SQL query using:
- ad_sales(date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold)
- total_sales(date, item_id, total_sales, total_units_ordered)
- eligibility(eligibility_datetime_utc, item_id, eligibility, message)
ONLY return the SQL query."""
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        import requests
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
        result = response.json()

        if "choices" in result:
            text = result["choices"][0]["message"]["content"]
            return text.strip("```sql").strip("```")

        return "SELECT 'Error: No valid response from OpenRouter' AS error;"

    except Exception as e:
        print("OpenRouter Error:", e)
        return "SELECT 'OpenRouter API crashed' AS error;"

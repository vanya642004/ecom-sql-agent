import plotly.express as px

def generate_chart(question, df):
    cols = df.columns.str.lower().tolist()
    question = question.lower()

    try:
        if "sales" in question and "item" in question and "total" in question:
            if "item_id" in cols and "total_sales" in cols:
                return px.bar(df, x="item_id", y="total_sales", title="Total Sales per Product")
        elif "clicks" in question and "date" in cols:
            return px.line(df, x="date", y="clicks", title="Clicks Over Time")
        elif "impressions" in question and "date" in cols:
            return px.area(df, x="date", y="impressions", title="Impressions Over Time")
        elif "roas" in question and "ad_sales" in cols and "ad_spend" in cols:
            return px.scatter(df, x="item_id", y="ad_sales", size="ad_spend", title="RoAS Bubble Chart")
        else:
            return None
    except Exception as e:
        print("Chart generation error:", e)
        return None

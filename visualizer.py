import plotly.express as px

def generate_chart(question, df):
    question = question.lower()
    if "sales" in question and "product" in question and "total" in question:
        return px.bar(df, x="item_id", y="total_sales", title="Total Sales per Product")
    if "clicks" in question:
        return px.line(df, x="date", y="clicks", title="Clicks Over Time")
    if "impressions" in question:
        return px.area(df, x="date", y="impressions", title="Ad Impressions Over Time")
    if "roas" in question:
        if "item_id" in df.columns:
            return px.scatter(df, x="item_id", y="ad_sales", size="ad_spend", title="RoAS Bubble Chart")
    return None

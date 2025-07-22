import streamlit as st
from query_engine import ask_question
from visualizer import generate_chart

st.set_page_config(page_title="E-commerce SQL Agent", layout="wide")
st.title("🛒 AI Agent: Ask Anything About Your E-commerce Data")

question = st.text_input("Ask your question:")

if question:
    with st.spinner("Thinking..."):
        answer, sql_query, result_df = ask_question(question)

        st.markdown(f"**Answer:** {answer}")
        st.markdown(f"`SQL:` `{sql_query}`")

        if not result_df.empty:
            st.dataframe(result_df)

            # Optional chart
            chart = generate_chart(question, result_df)
            if chart:
                st.plotly_chart(chart, use_container_width=True)

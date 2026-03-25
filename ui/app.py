"""Streamlit chat UI for Data Analyst Agent."""
import streamlit as st
import requests

st.set_page_config(page_title="Data Analyst Agent", page_icon="📊", layout="wide")
st.title("📊 Data Analyst Agent")
st.caption("Ask questions about your data in plain English")

with st.sidebar:
    st.header("Database Connection")
    db_url = st.text_input("Database URL", "sqlite:///./demo.db")
    model = st.selectbox("Model", ["gpt-4o", "gpt-4o-mini"])
    api_url = st.text_input("API URL", "http://localhost:8003")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sql"):
            with st.expander("SQL Query"):
                st.code(msg["sql"], language="sql")
        if msg.get("chart"):
            st.plotly_chart(msg["chart"])

if question := st.chat_input("Ask about your data..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                resp = requests.post(f"{api_url}/analyze", json={"question": question, "database_url": db_url, "model": model}, timeout=60)
                result = resp.json()
                st.markdown(result.get("analysis", "No analysis returned"))
                if result.get("sql"):
                    with st.expander("Generated SQL"):
                        st.code(result["sql"], language="sql")
                st.session_state.messages.append({"role": "assistant", "content": result.get("analysis",""), "sql": result.get("sql","")})
            except Exception as e:
                st.error(f"Error: {e}")

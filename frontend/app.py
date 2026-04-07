import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("AI Study Companion")

menu = st.sidebar.selectbox("Choose Feature", ["Chat Tutor", "Study Planner", "Notes Summarizer"])

if menu == "Chat Tutor":
    st.header("Ask Anything")
    question = st.text_input("Enter your question")
    if st.button("Ask"):
        res = requests.post(f"{API_URL}/chat", json={"question": question})
        st.write(res.json()["response"])

elif menu == "Study Planner":
    st.header("Generate Study Plan")
    subject = st.text_input("Subject")
    days = st.slider("Days", 1, 30, 7)
    if st.button("Generate"):
        res = requests.post(f"{API_URL}/plan", json={"subject": subject, "days": days})
        st.write(res.json()["plan"])

elif menu == "Notes Summarizer":
    st.header("Summarize Notes")
    content = st.text_area("Paste your notes")
    if st.button("Summarize"):
        res = requests.post(f"{API_URL}/summarize", json={"content": content})
        st.write(res.json()["summary"])
import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Study Companion", layout="centered")

st.title("🚀 AI Study Companion")

menu = st.sidebar.selectbox(
    "Choose Feature",
    ["Chat Tutor", "Study Planner", "Notes Summarizer"]
)

def call_api(endpoint, payload):
    try:
        res = requests.post(f"{API_URL}{endpoint}", json=payload, timeout=30)

        if res.status_code == 200:
            try:
                return res.json()
            except Exception:
                return {"error": "Invalid JSON response", "raw": res.text}
        else:
            return {"error": f"HTTP {res.status_code}", "raw": res.text}

    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Try again."}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}



# Chat Tutor

if menu == "Chat Tutor":
    st.header("🤖 Ask Anything")

    question = st.text_input("Enter your question")

    if st.button("Ask"):
        if not question.strip():
            st.warning("Please enter a question")
        else:
            with st.spinner("Thinking..."):
                data = call_api("/chat", {"question": question})

            if "response" in data:
                st.success(data["response"])
            else:
                st.error("Something went wrong")
                st.write(data)


# Study Planner

elif menu == "Study Planner":
    st.header("📊 Generate Study Plan")

    subject = st.text_input("Subject")
    days = st.slider("Days", 1, 30, 7)

    if st.button("Generate"):
        if not subject.strip():
            st.warning("Please enter a subject")
        else:
            with st.spinner("Generating plan..."):
                data = call_api("/plan", {"subject": subject, "days": days})

            if "plan" in data:
                st.success(data["plan"])
            else:
                st.error("Something went wrong")
                st.write(data)


# Notes Summarizer

elif menu == "Notes Summarizer":
    st.header("📝 Summarize Notes")

    content = st.text_area("Paste your notes")

    if st.button("Summarize"):
        if not content.strip():
            st.warning("Please enter some content")
        else:
            with st.spinner("Summarizing..."):
                data = call_api("/summarize", {"content": content})

            if "summary" in data:
                st.success(data["summary"])
            else:
                st.error("Something went wrong")
                st.write(data)

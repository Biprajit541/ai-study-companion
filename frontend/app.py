import streamlit as st
import requests

API_URL = "https://ideal-ambition-production-a154.up.railway.app"

st.title("🚀 AI Study Companion")

menu = st.sidebar.selectbox(
    "Choose Feature",
    ["Chat Tutor", "Study Planner", "Notes Summarizer"]
)

def call_api(endpoint, payload):
    try:
        res = requests.post(f"{API_URL}{endpoint}", json=payload, timeout=30)

        # 🔍 DEBUG: show raw response
        st.write("Raw response:", res.text)

        if res.status_code == 200:
            try:
                return res.json()
            except Exception:
                return {"error": "Invalid JSON response"}
        else:
            return {"error": f"HTTP {res.status_code}", "details": res.text}

    except Exception as e:
        return {"error": str(e)}


# ================= CHAT =================
if menu == "Chat Tutor":
    st.header("🤖 Ask Anything")

    question = st.text_input("Enter your question")

    if st.button("Ask"):
        data = call_api("/chat", {"question": question})

        if "response" in data:
            st.success(data["response"])
        else:
            st.error("Error from backend")
            st.write(data)


# ================= PLANNER =================
elif menu == "Study Planner":
    st.header("📊 Generate Study Plan")

    subject = st.text_input("Subject")
    days = st.slider("Days", 1, 30, 7)

    if st.button("Generate"):
        data = call_api("/plan", {"subject": subject, "days": days})

        if "plan" in data:
            st.success(data["plan"])
        else:
            st.error("Error from backend")
            st.write(data)


# ================= SUMMARIZER =================
elif menu == "Notes Summarizer":
    st.header("📝 Summarize Notes")

    content = st.text_area("Paste your notes")

    if st.button("Summarize"):
        data = call_api("/summarize", {"content": content})

        if "summary" in data:
            st.success(data["summary"])
        else:
            st.error("Error from backend")
            st.write(data)

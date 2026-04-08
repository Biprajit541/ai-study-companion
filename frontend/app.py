import streamlit as st
import requests

API_URL = "https://helpful-balance-production-f861.up.railway.app"

st.set_page_config(page_title="AI Study Companion", layout="wide")

# ---------- STYLING ----------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.block-container {
    padding-top: 2rem;
}
.card {
    background-color: #1e222a;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
}
.chat-user {
    background-color: #4CAF50;
    padding: 10px;
    border-radius: 10px;
    color: white;
    margin-bottom: 5px;
}
.chat-bot {
    background-color: #2a2f3a;
    padding: 10px;
    border-radius: 10px;
    color: white;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------- API ----------
def call_api(endpoint, payload):
    try:
        res = requests.post(f"{API_URL}{endpoint}", json=payload, timeout=30)

        if res.status_code == 200:
            return res.json()
        else:
            return {"error": res.text}

    except Exception as e:
        return {"error": str(e)}

# ---------- SIDEBAR ----------
st.sidebar.title("🚀 AI Study Companion")
menu = st.sidebar.radio(
    "Navigation",
    ["💬 Chat Tutor", "📊 Study Planner", "📝 Notes Summarizer"]
)

st.sidebar.markdown("---")
st.sidebar.info("Built using FastAPI + Groq + Streamlit")

# ---------- CHAT ----------
if menu == "💬 Chat Tutor":
    st.title("💬 AI Chat Tutor")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("Ask a question")

    if st.button("Send"):
        if user_input:
            with st.spinner("Thinking..."):
                data = call_api("/chat", {"question": user_input})

            response = data.get("response", "Error occurred")

            st.session_state.chat_history.append((user_input, response))

    # Display chat
    for user, bot in reversed(st.session_state.chat_history):
        st.markdown(f"<div class='chat-user'>🧑 {user}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-bot'>🤖 {bot}</div>", unsafe_allow_html=True)

# ---------- PLANNER ----------
elif menu == "📊 Study Planner":
    st.title("📊 Smart Study Planner")

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        subject = st.text_input("Subject")
    with col2:
        days = st.slider("Days", 1, 30, 7)

    if st.button("Generate Plan"):
        if subject:
            with st.spinner("Generating plan..."):
                data = call_api("/plan", {"subject": subject, "days": days})

            if "plan" in data:
                st.markdown("### 📅 Your Plan")
                st.markdown(f"<div class='card'>{data['plan']}</div>", unsafe_allow_html=True)
            else:
                st.error(data)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- SUMMARIZER ----------
elif menu == "📝 Notes Summarizer":
    st.title("📝 Notes Summarizer")

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    content = st.text_area("Paste your notes", height=200)

    if st.button("Summarize"):
        if content:
            with st.spinner("Summarizing..."):
                data = call_api("/summarize", {"content": content})

            if "summary" in data:
                st.markdown("### 📌 Summary")
                st.markdown(f"<div class='card'>{data['summary']}</div>", unsafe_allow_html=True)
            else:
                st.error(data)

    st.markdown("</div>", unsafe_allow_html=True)

import streamlit as st
import requests

API_URL = "http://ai-study-companion-production-33d6.up.railway.app"

st.set_page_config(page_title="AI Study Companion", layout="wide")

# ---------- STYLING ----------
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
.block-container {
    padding-top: 2rem;
}
.stTextInput>div>div>input {
    background-color: #1e222a;
    color: white;
}
.stTextArea textarea {
    background-color: #1e222a;
    color: white;
}
.stButton button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ---------- API CALL ----------
def call_api(endpoint, payload):
    try:
        res = requests.post(f"{API_URL}{endpoint}", json=payload, timeout=30)

        if res.status_code == 200:
            return res.json()
        else:
            return {"error": f"HTTP {res.status_code}", "details": res.text}

    except Exception as e:
        return {"error": str(e)}

# ---------- SIDEBAR ----------
st.sidebar.title("📚 AI Study Companion")
menu = st.sidebar.radio(
    "Navigate",
    ["💬 Chat Tutor", "📊 Study Planner", "📝 Notes Summarizer"]
)

# ---------- CHAT ----------
if menu == "💬 Chat Tutor":
    st.title("💬 AI Chat Tutor")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("Ask anything...")

    if st.button("Send") and user_input:
        with st.spinner("Thinking..."):
            data = call_api("/chat", {"question": user_input})

        response = data.get("response", "Error occurred")

        st.session_state.chat_history.append((user_input, response))

    for user, bot in reversed(st.session_state.chat_history):
        st.markdown(f"**🧑 You:** {user}")
        st.markdown(f"**🤖 AI:** {bot}")
        st.markdown("---")

# ---------- PLANNER ----------
elif menu == "📊 Study Planner":
    st.title("📊 Smart Study Planner")

    col1, col2 = st.columns(2)

    with col1:
        subject = st.text_input("Subject")
    with col2:
        days = st.number_input("Days", min_value=1, max_value=30, value=7)

    if st.button("Generate Plan"):
        if subject:
            with st.spinner("Creating your plan..."):
                data = call_api("/plan", {"subject": subject, "days": days})

            if "plan" in data:
                st.success("Your Study Plan:")
                st.write(data["plan"])
            else:
                st.error(data)

# ---------- SUMMARIZER ----------
elif menu == "📝 Notes Summarizer":
    st.title("📝 Notes Summarizer")

    content = st.text_area("Paste your notes here...", height=200)

    if st.button("Summarize"):
        if content:
            with st.spinner("Summarizing..."):
                data = call_api("/summarize", {"content": content})

            if "summary" in data:
                st.success("Summary:")
                st.write(data["summary"])
            else:
                st.error(data)

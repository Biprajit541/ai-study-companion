import streamlit as st
import requests
import re

API_URL = "https://ai-study-backend-py3f.onrender.com"

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
.source-box {
    background-color: #2a2f3a;
    padding: 10px;
    border-radius: 10px;
    text-align: center;
    font-weight: bold;
    transition: 0.3s;
    cursor: pointer;
}
.source-box:hover {
    background-color: #3a4150;
    transform: scale(1.05);
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

# ---------- RESPONSE FORMAT ----------
def format_response(response):
    parts = response.split("📌 Source:")

    answer = parts[0].strip()

    sources = []
    if len(parts) > 1:
        sources = re.findall(r'Page \d+', parts[1])

    return answer, sources

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

    # 🧠 Memory
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are an expert AI tutor."}
        ]

    # 📄 Upload document
    uploaded_file = st.file_uploader("📄 Upload notes", type=["pdf", "txt"])

    if uploaded_file and "uploaded" not in st.session_state:
        with st.spinner("Processing document..."):
            res = requests.post(
                f"{API_URL}/upload-doc",
                files={"file": uploaded_file}
            )
        st.session_state.uploaded = True
        st.success("Document ready! Ask questions.")

    # ✍️ Input
    user_input = st.text_input("Ask something...")

    # 🔄 Trim memory
    MAX_HISTORY = 6
    def trim_messages(messages):
        return [messages[0]] + messages[-MAX_HISTORY:]

    if st.button("Send"):
        if user_input:
            st.session_state.messages.append(
                {"role": "user", "content": user_input}
            )

            with st.spinner("Thinking..."):
                data = call_api("/chat", {
                    "messages": trim_messages(st.session_state.messages)
                })

            if "response" in data:
                response = data["response"]
            else:
                response = "⚠️ Error from backend"

            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )

    # 💬 Display chat with citations
    for msg in st.session_state.messages[1:]:
        if msg["role"] == "user":
            st.markdown(f"<div class='chat-user'>🧑 {msg['content']}</div>", unsafe_allow_html=True)

        else:
            answer, sources = format_response(msg["content"])

            # 🤖 Answer
            st.markdown(f"<div class='chat-bot'>🤖 {answer}</div>", unsafe_allow_html=True)

            # 📚 Sources
            if sources:
                st.markdown("#### 📚 Sources")

                cols = st.columns(len(sources))

                for i, src in enumerate(sources):
                    with cols[i]:
                        st.markdown(
                            f"<div class='source-box'>{src}</div>",
                            unsafe_allow_html=True
                        )

            st.caption("💡 Tip: Ask specific questions for better answers")

    # 🧹 Controls
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🧹 Clear Chat"):
            st.session_state.messages = [
                {"role": "system", "content": "You are an expert AI tutor."}
            ]
            st.session_state.pop("uploaded", None)

    with col2:
        if st.button("↩️ Undo Last"):
            if len(st.session_state.messages) > 2:
                st.session_state.messages.pop()
                st.session_state.messages.pop()

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

import streamlit as st
import json
import os
from groq import Groq

# --------------------------------
# Page Configuration
# --------------------------------
st.set_page_config(
    page_title="AI Chatbot with Memory",
    page_icon="🤖",
    layout="centered"
)

# --------------------------------
# Custom CSS
# --------------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"]{
    font-family:'Inter',sans-serif;
}

.stApp{
    background:linear-gradient(135deg,#0F0C29,#302B63,#24243E);
    background-attachment:fixed;
}

.block-container{
    background:rgba(255,255,255,0.05);
    backdrop-filter:blur(18px);
    border-radius:20px;
    padding:2rem;
    margin-top:20px;
    border:1px solid rgba(255,255,255,0.1);
}

h1{
    color:white;
    text-align:center;
}

[data-testid="stSidebar"]{
    background:rgba(20,20,35,.85);
    backdrop-filter:blur(20px);
}

[data-testid="stChatMessage"]{
    background:rgba(255,255,255,.08);
    border-radius:16px;
    padding:14px;
    margin-bottom:10px;
    border:1px solid rgba(255,255,255,.08);
}

footer{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------
# Load Groq API Key
# --------------------------------
try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("Please add GROQ_API_KEY in Streamlit Secrets.")
    st.stop()

client = Groq(api_key=api_key)

# --------------------------------
# System Prompt
# --------------------------------
SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are a helpful AI assistant."
}

# --------------------------------
# Load Chat History
# --------------------------------
if "saved_history" not in st.session_state:

    if os.path.exists("chat_history.json"):

        with open("chat_history.json", "r") as file:
            st.session_state.saved_history = json.load(file)

    else:
        st.session_state.saved_history = []

if "current_chat" not in st.session_state:

    st.session_state.current_chat = (
        st.session_state.saved_history.copy()
    )
# --------------------------------
# Header
# --------------------------------
st.title("🤖 AI Chatbot with Memory")
st.caption("Powered by Groq • Llama 3.3")

# --------------------------------
# Sidebar
# --------------------------------
with st.sidebar:

    st.header("⚙️ Settings")

    st.success("Model: Llama 3.3 70B")

    if st.button("🗑 Clear Chat"):
        # Only clear the UI
        st.session_state.current_chat = []
        st.rerun()

    if st.button("📂 Restore Previous Chat"):
        st.session_state.current_chat = (
        st.session_state.saved_history.copy()
        )
        st.rerun()

# --------------------------------
# Display Previous Messages
# --------------------------------
for message in st.session_state.current_chat:

    avatar = "👤" if message["role"] == "user" else "🤖"

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# --------------------------------
# User Input
# --------------------------------
prompt = st.chat_input("Ask me anything...")

if prompt:

    # Save user message
    st.session_state.current_chat.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Build conversation with memory
    conversation = [SYSTEM_PROMPT] + st.session_state.current_chat

    with st.chat_message("assistant", avatar="🤖"):

        with st.spinner("Thinking..."):

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=conversation,
                temperature=0.7,
                max_tokens=1024,
            )

            answer = response.choices[0].message.content

            st.markdown(answer)

    # Save assistant response
    st.session_state.current_chat.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
    # Save chat history to file
    st.session_state.saved_history = (
    st.session_state.current_chat.copy()
)

with open("chat_history.json", "w", encoding="utf-8") as file:

    json.dump(
        st.session_state.saved_history,
        file,
        ensure_ascii=False,
        indent=4
    )
        

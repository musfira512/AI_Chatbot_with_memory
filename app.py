import os
import streamlit as st
from groq import Groq

# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(
    page_title="AI Chatbot with Memory",
    page_icon="🤖",
    layout="centered"
)

.stApp{
background: linear-gradient(135deg,#141E30,#243B55);
}

[data-testid="stChatMessage"]{
background:rgba(255,255,255,0.08);
backdrop-filter:blur(12px);
border-radius:20px;
padding:15px;
border:1px solid rgba(255,255,255,0.1);
}
# ---------------------------
# Groq API
# ---------------------------
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("⚠️ GROQ_API_KEY not found.")
    st.stop()

client = Groq(api_key=api_key)

# ---------------------------
# Session Memory
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        }
    ]

# ---------------------------
# Header
# ---------------------------
st.markdown("# 🤖 AI Chatbot with Memory")
st.caption("Powered by Groq • Llama 3.3")

# ---------------------------
# Sidebar
# ---------------------------
with st.sidebar:
    st.title("⚙️ Settings")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            }
        ]
        st.rerun()

# ---------------------------
# Display Messages
# ---------------------------
for message in st.session_state.messages:

    if message["role"] == "system":
        continue

    avatar = "👤" if message["role"] == "user" else "🤖"

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ---------------------------
# Chat Input
# ---------------------------
prompt = st.chat_input("Ask anything...")

if prompt:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):

        with st.spinner("Thinking..."):

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                temperature=0.7,
            )

            answer = response.choices[0].message.content

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":answer
        }
    )

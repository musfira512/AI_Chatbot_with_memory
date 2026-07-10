import os
import streamlit as st
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
    font-family: 'Inter', sans-serif;
}

/* Background */
.stApp{
    background: linear-gradient(
        135deg,
        #0F0C29 0%,
        #302B63 50%,
        #24243E 100%
    );
    background-attachment: fixed;
}

/* Main container */
.block-container{
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(18px);
    border-radius: 20px;
    padding: 2rem;
    margin-top: 20px;
    border: 1px solid rgba(255,255,255,0.1);
}

/* Title */
h1{
    text-align:center;
    color:white;
    font-weight:700;
}

/* Caption */
.stCaption{
    text-align:center;
    color:#D8B4FE !important;
}

/* Sidebar */
[data-testid="stSidebar"]{
    background: rgba(20,20,35,0.85);
    backdrop-filter: blur(20px);
}

/* Chat messages */
[data-testid="stChatMessage"]{
    background: rgba(255,255,255,0.08);
    border-radius:18px;
    padding:15px;
    margin-bottom:12px;
    border:1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
}

/* Textbox */
.stTextInput input{
    border-radius:15px;
}

/* Buttons */
.stButton>button{
    width:100%;
    border-radius:12px;
    border:none;
    background:#8B5CF6;
    color:white;
    font-weight:600;
}

.stButton>button:hover{
    background:#7C3AED;
}

/* Hide Streamlit Footer */
footer{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------
# Groq API
# --------------------------------
try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("❌ GROQ_API_KEY is missing from Streamlit Secrets.")
    st.info("Go to App Settings → Secrets and add:\n\nGROQ_API_KEY = \"gsk_your_api_key\"")
    st.stop()

client = Groq(api_key=api_key)

# --------------------------------
# Session Memory
# --------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        }
    ]

# --------------------------------
# Header
# --------------------------------
st.title("🤖 AI Chatbot with Memory")
st.caption("Powered by Groq • Llama 3.3 • Streamlit")

# --------------------------------
# Sidebar
# --------------------------------
with st.sidebar:

    st.title("⚙️ Settings")

    st.write("### AI Model")
    st.info("Llama 3.3 70B Versatile")

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = [
            {
                "role":"system",
                "content":"You are a helpful AI assistant."
            }
        ]

        st.rerun()

# --------------------------------
# Display Chat
# --------------------------------
for message in st.session_state.messages:

    if message["role"] == "system":
        continue

    avatar = "👤" if message["role"] == "user" else "🤖"

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# --------------------------------
# Chat Input
# --------------------------------
prompt = st.chat_input("💬 Ask me anything...")

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
                max_tokens=1024
            )

            answer = response.choices[0].message.content

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":answer
        }
    )

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
# Load All Chats
# --------------------------------
CHAT_FILE = "chat_history.json"

if "chats" not in st.session_state:

    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r", encoding="utf-8") as file:
            st.session_state.chats = json.load(file)
    else:
        st.session_state.chats = []

# Current selected chat index
if "current_chat_index" not in st.session_state:
    st.session_state.current_chat_index = None


def save_chats():
    with open(CHAT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            st.session_state.chats,
            file,
            ensure_ascii=False,
            indent=4
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

    st.title("💬 Chats")

    # ---------------------------
    # New Chat Button
    # ---------------------------
   if st.button("➕ New Chat", use_container_width=True):

    # Only create a new chat if the current one has messages
    if (
        st.session_state.current_chat_index is None
        or st.session_state.chats[st.session_state.current_chat_index]["messages"]
    ):

        st.session_state.chats.append(
            {
                "title": "New Chat",
                "messages": []
            }
        )

        st.session_state.current_chat_index = len(st.session_state.chats) - 1

        save_chats()

    st.rerun()

    # ---------------------------
    # Conversation List
    # ---------------------------
    for i, chat in enumerate(st.session_state.chats):

        if st.button(
            chat["title"],
            key=f"chat_{i}",
            use_container_width=True
        ):

            st.session_state.current_chat_index = i

            st.rerun()

    st.divider()

    st.success("Model: Llama 3.3 70B")

# --------------------------------
# Display Current Chat
# --------------------------------
if st.session_state.current_chat_index is not None:

    current_chat = st.session_state.chats[
        st.session_state.current_chat_index
    ]

    for message in current_chat["messages"]:

        avatar = "👤" if message["role"] == "user" else "🤖"

        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# --------------------------------
# User Input
# --------------------------------
prompt = st.chat_input("Ask me anything...")

if prompt:

# If no chat exists, create one automatically
if st.session_state.current_chat_index is None:

    st.session_state.chats.append(
        {
            "title": prompt[:30],
            "messages": []
        }
    )

    st.session_state.current_chat_index = (
        len(st.session_state.chats) - 1
    )

current_chat = st.session_state.chats[
    st.session_state.current_chat_index
]

# Change "New Chat" title to first message
if current_chat["title"] == "New Chat":
    current_chat["title"] = prompt[:30]
    save_chats()

# Save user message
current_chat["messages"].append(
    {
        "role": "user",
        "content": prompt
    }
)

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Build conversation with memory
    conversation = [SYSTEM_PROMPT]

    conversation.extend(current_chat["messages"])

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
current_chat["messages"].append(
    {
        "role": "assistant",
        "content": answer
    }
)
    # Save chat history to file
   save_chats()
        

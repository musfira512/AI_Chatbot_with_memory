import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(
    page_title="AI Chatbot with Memory",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS
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

# Load Groq API Key
try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("Please add GROQ_API_KEY in Streamlit Secrets.")
    st.stop()

client = Groq(api_key=api_key)

# System Prompt
SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are a helpful AI assistant."
}

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.title("🤖 AI Chatbot with Memory")
st.caption("Powered by Groq • Llama 3.3")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    st.success("Model: Llama 3.3 70B")
    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    if st.button("📝 View Chat History"):
        st.write("### Chat History:")
        for i, message in enumerate(st.session_state.messages):
            st.write(f"**Message {i+1}:**")
            st.write(message["content"])
            st.write("---")

# Display Previous Messages
def display_previous_messages():
    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# User Input
def get_user_input():
    prompt = st.chat_input("Ask me anything...")
    if prompt:
        return prompt
    else:
        return None

user_input = get_user_input()

if user_input:
    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Build conversation with memory
    conversation = [SYSTEM_PROMPT] + st.session_state.messages

    def get_assistant_response(conversation):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=conversation,
                temperature=0.7,
                max_tokens=1024,
            )
            return response.choices[0].message.content
        except Exception as e:
            return str(e)

    # Get assistant response
    assistant_response = get_assistant_response(conversation)

    # Display assistant response
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(assistant_response)

    # Save assistant response
    st.session_state.messages.append(
        {
            "

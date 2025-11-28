import streamlit as st

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Chatbot UI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Initialize Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.title("Navigation")
    st.markdown("Customize your chatbot here.")
    
    if st.button("New Chat", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()
    
    st.divider()
    
    # Display message count
    message_count = len(st.session_state["messages"])
    st.caption(f"💬 Messages: {message_count}")

# -----------------------------
# Main Chat Interface
# -----------------------------
st.title("Chatbot Application")
st.markdown("---")

# -----------------------------
# Display Chat History
# -----------------------------
chat_container = st.container()
with chat_container:
    if len(st.session_state["messages"]) == 0:
        st.info("👋 Start a conversation by typing a message below!")
    else:
        for msg in st.session_state["messages"]:
            if msg["role"] == "user":
                with st.chat_message("user", avatar="👤"):
                    st.markdown(msg["content"])
            else:
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(msg["content"])

# -----------------------------
# User Input Box
# -----------------------------
user_input = st.chat_input("Send a message...")

if user_input:
    # Store user message
    st.session_state["messages"].append({
        "role": "user",
        "content": user_input
    })
    
    # Generate bot reply (placeholder logic)
    bot_reply = f"You said: **{user_input}**"
    
    # Store bot message
    st.session_state["messages"].append({
        "role": "assistant",
        "content": bot_reply
    })
    
    # Refresh to display new messages
    st.rerun()
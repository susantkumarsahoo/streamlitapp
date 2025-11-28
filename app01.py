import streamlit as st
import time
import requests
from datetime import datetime


# Page configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    
    .user-message {
        background-color: #e3f2fd;
        margin-left: 20%;
    }
    
    .bot-message {
        background-color: #f5f5f5;
        margin-right: 20%;
    }
    
    .message-avatar {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    .message-content {
        font-size: 1rem;
        line-height: 1.5;
    }
    
    .timestamp {
        font-size: 0.75rem;
        color: #666;
        margin-top: 0.5rem;
    }
    
    .stTextInput > div > div > input {
        border-radius: 20px;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_endpoint" not in st.session_state:
    st.session_state.api_endpoint = "http://localhost:8000/chat"

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# Sidebar configuration
with st.sidebar:
    st.title("⚙️ Settings")
    
    # API Configuration
    st.subheader("API Configuration")
    api_endpoint = st.text_input(
        "Backend API Endpoint",
        value=st.session_state.api_endpoint,
        help="Enter your chatbot backend API endpoint"
    )
    st.session_state.api_endpoint = api_endpoint
    
    api_key = st.text_input(
        "API Key (if required)",
        value=st.session_state.api_key,
        type="password",
        help="Enter your API key if authentication is required"
    )
    st.session_state.api_key = api_key
    
    st.divider()
    
    # Chat settings
    st.subheader("Chat Settings")
    temperature = st.slider("Response Temperature", 0.0, 1.0, 0.7, 0.1)
    max_tokens = st.number_input("Max Response Tokens", 100, 4000, 1000, 100)
    
    st.divider()
    
    # Chat history management
    st.subheader("Chat History")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    if st.button("💾 Export Chat", use_container_width=True):
        chat_export = "\n\n".join([
            f"[{msg['timestamp']}] {msg['role'].upper()}: {msg['content']}"
            for msg in st.session_state.messages
        ])
        st.download_button(
            "Download Chat Log",
            chat_export,
            file_name=f"chat_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
    
    st.divider()
    
    # Statistics
    st.subheader("📊 Statistics")
    total_messages = len(st.session_state.messages)
    user_messages = sum(1 for m in st.session_state.messages if m["role"] == "user")
    bot_messages = sum(1 for m in st.session_state.messages if m["role"] == "assistant")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total", total_messages)
        st.metric("User", user_messages)
    with col2:
        st.metric("Bot", bot_messages)
        
        
# Main chat interface
st.title("🤖 AI Chatbot")
st.caption("Powered by your custom backend")

# Display chat messages
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <div class="message-avatar">👤 You</div>
                <div class="message-content">{message["content"]}</div>
                <div class="timestamp">{message["timestamp"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot-message">
                <div class="message-avatar">🤖 Assistant</div>
                <div class="message-content">{message["content"]}</div>
                <div class="timestamp">{message["timestamp"]}</div>
            </div>
            """, unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to chat
    timestamp = datetime.now().strftime("%I:%M %p")
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": timestamp
    })
    
    # Display user message immediately
    with chat_container:
        st.markdown(f"""
        <div class="chat-message user-message">
            <div class="message-avatar">👤 You</div>
            <div class="message-content">{user_input}</div>
            <div class="timestamp">{timestamp}</div>
        </div>
        """, unsafe_allow_html=True)
        
        
        
    # Show typing indicator
    with st.spinner("🤖 Assistant is typing..."):
        try:
            # Prepare request payload
            headers = {"Content-Type": "application/json"}
            if st.session_state.api_key:
                headers["Authorization"] = f"Bearer {st.session_state.api_key}"
            
            payload = {
                "message": user_input,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "conversation_history": [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages[:-1]  # Exclude the just-added user message
                ]
            }
            
            # Call backend API
            response = requests.post(
                st.session_state.api_endpoint,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                bot_response = response.json().get("response", "No response received")
            else:
                bot_response = f"Error: API returned status code {response.status_code}"
                
        except requests.exceptions.ConnectionError:
            bot_response = "⚠️ Could not connect to backend. Please check your API endpoint."
        except requests.exceptions.Timeout:
            bot_response = "⚠️ Request timed out. The backend took too long to respond."
        except Exception as e:
            bot_response = f"⚠️ Error: {str(e)}"
    
    # Add bot response to chat
    bot_timestamp = datetime.now().strftime("%I:%M %p")
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_response,
        "timestamp": bot_timestamp
    })
    # Rerun to display the new message
    st.rerun()

# Welcome message if no messages yet
if len(st.session_state.messages) == 0:
    st.info("👋 Welcome! Start a conversation by typing a message below.")
    
    # Quick start examples
    st.subheader("Try these examples:")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💡 Tell me a joke"):
            st.session_state.messages.append({
                "role": "user",
                "content": "Tell me a joke",
                "timestamp": datetime.now().strftime("%I:%M %p")
            })
            st.rerun()
    
    with col2:
        if st.button("📚 Explain AI"):
            st.session_state.messages.append({
                "role": "user",
                "content": "Explain artificial intelligence in simple terms",
                "timestamp": datetime.now().strftime("%I:%M %p")
            })
            st.rerun()
    
    with col3:
        if st.button("🎯 Help me brainstorm"):
            st.session_state.messages.append({
                "role": "user",
                "content": "Help me brainstorm ideas for a project",
                "timestamp": datetime.now().strftime("%I:%M %p")
            })
            st.rerun()


    

        
        








"""
Streamlit Chatbot Frontend

Save this file as `streamlit_chatbot_app.py` and run:
    streamlit run streamlit_chatbot_app.py

Features:
- Chat UI using Streamlit's st.chat_message
- Sidebar controls: model (placeholder), temperature, system prompt, persona presets
- File upload (text/PDF) to add context to the conversation
- Streaming responses (if OpenAI API key provided) and fallback local echo bot
- Conversation history stored in session_state
- Export / download chat as JSON
- Clear chat button
- Basic markdown/Code rendering and attachments preview
"""

import streamlit as st
from typing import List, Dict, Any
import time
import json
import os
import base64

# Optional imports (used only if available)
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False

try:
    import PyPDF2
except Exception:
    PyPDF2 = None

# -------------------- Utilities --------------------

def init_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'context_documents' not in st.session_state:
        st.session_state.context_documents = []
    if 'streaming' not in st.session_state:
        st.session_state.streaming = False


def add_message(role: str, content: str, attachments: List[Dict[str, Any]] = None):
    st.session_state.messages.append({
        'role': role,
        'content': content,
        'time': time.time(),
        'attachments': attachments or []
    })


def clear_chat():
    st.session_state.messages = []
    st.session_state.context_documents = []


def download_chat_json():
    data = {
        'messages': st.session_state.messages,
        'context_documents': st.session_state.context_documents,
        'meta': {'exported_at': time.time()}
    }
    return json.dumps(data, indent=2)


def read_uploaded_file(uploaded_file) -> str:
    name = uploaded_file.name.lower()
    if name.endswith('.txt') or name.endswith('.md'):
        content = uploaded_file.getvalue().decode('utf-8')
        return content
    if name.endswith('.pdf') and PyPDF2 is not None:
        try:
            reader = PyPDF2.PdfReader(uploaded_file)
            pages = []
            for p in reader.pages:
                pages.append(p.extract_text() or '')
            return '\n\n'.join(pages)
        except Exception as e:
            return f"[unreadable pdf: {e}]"
    # Fallback: binary to base64 (for images or unknown types)
    b64 = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
    return f"[base64:{uploaded_file.name}:{b64[:200]}...]"


# -------------------- LLM Backend (Optional) --------------------

class LocalEchoLLM:
    """A simple fallback LLM that echoes the user and adds a tiny transformation."""

    @staticmethod
    def generate(system_prompt: str, history: List[Dict[str, str]], temperature: float = 0.0):
        last_user = next((m['content'] for m in reversed(history) if m['role'] == 'user'), '')
        reply = f"Echoing: {last_user}\n\n(You can plug an OpenAI key in the sidebar to enable real models.)"
        for i in range(1, len(reply.split()) + 1, 6):
            yield ' '.join(reply.split()[:i])
            time.sleep(0.05)
        yield reply


def openai_stream_response(api_key: str, model: str, system_prompt: str, history: List[Dict[str, str]], temperature: float = 0.0):
    """Streams response tokens from OpenAI ChatCompletion API."""
    if not OPENAI_AVAILABLE:
        yield from LocalEchoLLM.generate(system_prompt, history, temperature)
        return

    try:
        client = OpenAI(api_key=api_key)
        
        # Build messages in OpenAI format
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        for m in history:
            messages.append({"role": m['role'], "content": m['content']})

        # Use streaming mode
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=True,
        )

        collected = ''
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                collected += chunk.choices[0].delta.content
                yield collected
        
        yield collected
    except Exception as e:
        yield from LocalEchoLLM.generate(system_prompt, history, temperature)


# -------------------- Streamlit UI --------------------

st.set_page_config(page_title="Streamlit Chatbot UI", layout="wide")
init_state()

# Sidebar
with st.sidebar:
    st.title("Chatbot Settings")
    api_key_input = st.text_input("OpenAI API Key (optional)", type='password')
    if api_key_input:
        st.warning("Your API key will be used only in this session.")

    model = st.selectbox("Model", options=["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"], index=0)
    temp = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.05)

    st.markdown("---")
    st.subheader("System prompt / Persona")
    persona_presets = {
        'Helpful assistant': 'You are a helpful assistant. Answer concisely and helpfully.',
        'Teacher': 'You are a patient teacher. Explain steps and reasoning.',
        'Code assistant': 'You are a code assistant. Prefer code examples and short explanations.'
    }
    preset = st.selectbox("Preset persona", options=list(persona_presets.keys()))
    system_prompt = st.text_area("System prompt", value=persona_presets[preset], height=120)

    st.markdown("---")
    st.subheader("Conversation Controls")
    if st.button("Clear chat"):
        clear_chat()
        st.rerun()

    export_json = download_chat_json()
    st.download_button("Download chat (JSON)", export_json, file_name="chat_export.json", mime='application/json')

    st.markdown("---")
    st.markdown("**Context documents**")
    uploaded = st.file_uploader("Upload files (txt, md, pdf) to include as context", accept_multiple_files=True, key='sidebar_uploader')
    if uploaded:
        for f in uploaded:
            # Check if already processed
            if not any(d['name'] == f.name for d in st.session_state.context_documents):
                text = read_uploaded_file(f)
                st.session_state.context_documents.append({'name': f.name, 'text': text})
                add_message('system', f"[Attached file: {f.name}]\n\n{text[:500]}...")
        st.success(f"Total context files: {len(st.session_state.context_documents)}")

    st.markdown("---")
    st.caption("Demo chatbot UI. Connect to other LLM providers by modifying the backend.")

# Main layout
col1, col2 = st.columns([3, 1])

with col1:
    st.header("Chat")

    # Display chat messages
    if not st.session_state.messages:
        st.info("Start the conversation by typing a message below.")
    else:
        for msg in st.session_state.messages:
            role = msg['role']
            content = msg['content']
            if role in ['user', 'assistant']:
                with st.chat_message(role):
                    st.markdown(content)
            else:
                st.markdown(f"**{role}**: {content}")

    # Input area
    user_input = st.chat_input("Type a message...")
    
    if user_input:
        # Add user message
        add_message('user', user_input)

        # Prepare history for LLM
        history_for_llm = [
            {'role': m['role'], 'content': m['content']} 
            for m in st.session_state.messages 
            if m['role'] in ['user', 'assistant']
        ]

        # Streaming response
        with st.chat_message('assistant'):
            message_placeholder = st.empty()
            
            # Choose backend: OpenAI if key provided else local echo
            if api_key_input and OPENAI_AVAILABLE:
                stream_gen = openai_stream_response(api_key_input, model, system_prompt, history_for_llm, temperature=temp)
            else:
                stream_gen = LocalEchoLLM.generate(system_prompt, history_for_llm, temperature=temp)

            assistant_text = ''
            for partial in stream_gen:
                assistant_text = partial
                message_placeholder.markdown(assistant_text + '▌')
            
            message_placeholder.markdown(assistant_text)
            add_message('assistant', assistant_text)

with col2:
    st.header("Context & Tools")
    st.markdown("**Recent conversation**")
    last_msgs = st.session_state.messages[-6:]
    summary = '\n\n'.join([f"{m['role']}: {m['content'][:100]}..." for m in last_msgs]) or "No messages yet."
    st.code(summary, language='')

    st.markdown("---")
    st.subheader("Context documents")
    if st.session_state.context_documents:
        for d in st.session_state.context_documents:
            with st.expander(f"📄 {d['name']}"):
                st.write(d['text'][:500] + "...")
    else:
        st.info('No extra context documents uploaded')

    st.markdown("---")
    st.subheader("Quick actions")
    if st.button('Export last 5 messages'):
        md = ''
        for m in st.session_state.messages[-5:]:
            prefix = '### User' if m['role'] == 'user' else '### Assistant'
            md += f"{prefix}\n\n{m['content']}\n\n"
        st.download_button('Download .md', md, file_name='last_5_messages.md', mime='text/markdown')

    if st.button('Show session info'):
        st.json({
            'messages_count': len(st.session_state.messages),
            'context_docs_count': len(st.session_state.context_documents),
            'streaming': st.session_state.streaming
        })

st.markdown('---')
st.caption('Streamlit Chatbot UI — Demo application')
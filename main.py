import streamlit as st
import wikipedia
import speech_recognition as sr
import re

# --- Page Config ---
st.set_page_config(page_title="Wikipedia Chatbot 🧠", page_icon="📚", layout="centered")

# --- Styling ---
st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Quicksand', sans-serif;
        }
        .chat-row {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .chat-input-box {
            flex: 1;
        }
        .icon-button {
            background: none;
            border: none;
            font-size: 1.3rem;
            cursor: pointer;
            padding: 6px 8px;
            margin-top: 5px;
        }
        .message-box {
            padding: 10px 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            line-height: 1.5;
        }
        .user {
            background-color: #1e293b;
            color: #f0fdf4;
        }
        .bot {
            background-color: #334155;
            border-left: 4px solid #10b981;
            color: #e0f2f1;
        }
    </style>
""", unsafe_allow_html=True)

# --- Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Helper Functions ---
def clean_query(raw):
    raw = raw.lower()
    raw = re.sub(r"\b(who is|what is|tell me about|please|explain|define)\b", "", raw)
    return raw.strip()

def get_wikipedia_summary(query):
    try:
        results = wikipedia.search(query)
        if not results:
            return "😕 I couldn't find anything on that topic."
        summary = wikipedia.summary(results[0], sentences=2)
        return summary
    except Exception:
        return "⚠️ Oops! Something went wrong."

# --- Input Row ---
st.markdown('<div class="chat-row">', unsafe_allow_html=True)

# text box
user_query = st.text_input("", placeholder="💬 Ask me anything...", key="chatbox", label_visibility="collapsed")

# mic button
mic_btn = st.button("🎙️", help="Tap to speak")

# plus button (file uploader hidden)
file_upload = st.file_uploader("", type=["jpg", "jpeg", "png", "pdf", "txt"], label_visibility="collapsed")

st.markdown('</div>', unsafe_allow_html=True)

# --- Handle Mic ---
if mic_btn:
    st.toast("🎤 (Mic feature placeholder)")

# --- Handle Query ---
if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    cleaned = clean_query(user_query)
    summary = get_wikipedia_summary(cleaned)
    st.session_state.messages.append({"role": "bot", "content": summary})

# --- Display Messages ---
for msg in st.session_state.messages:
    role_class = "user" if msg["role"] == "user" else "bot"
    speaker = "You" if msg["role"] == "user" else "Bot"
    st.markdown(f"<div class='message-box {role_class}'><strong>{speaker}:</strong> {msg['content']}</div>", unsafe_allow_html=True)

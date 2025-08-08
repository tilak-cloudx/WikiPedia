import streamlit as st
import wikipedia
import speech_recognition as sr
import tempfile
import os
import re
from PIL import Image
from PyPDF2 import PdfReader

# --- Page Config ---
st.set_page_config(page_title="Wikipedia Chatbot 🧠", page_icon="📚", layout="centered")

# --- Styling ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500&display=swap');
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
        .footer {
            margin-top: 40px;
            font-size: 0.8rem;
            color: #6b7280;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
    <div style='text-align: center; padding-bottom: 10px;'>
        <h1>📚 Wikipedia Chatbot</h1>
        <p style='font-size: 1.1rem; color: #9ca3af;'>Ask anything, talk it out 🎤, or upload a pic 🖼️ — let’s explore Wikipedia!</p>
    </div>
""", unsafe_allow_html=True)

# --- Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Helper Functions ---
def clean_query(raw):
    raw = raw.lower()
    raw = re.sub(r"\b(who is|what is|tell me about|please|explain|define)\b", "", raw)
    return raw.strip()

def get_wikipedia_summary_and_image(query):
    try:
        results = wikipedia.search(query)
        if not results:
            return "😕 I couldn't find anything on that topic.", None
        page = wikipedia.page(results[0], auto_suggest=False, redirect=True)
        summary = wikipedia.summary(results[0], sentences=2)
        image_url = page.images[0] if page.images else None
        return summary, image_url
    except wikipedia.DisambiguationError as e:
        return f"🤔 Hmm… did you mean: {', '.join(e.options[:5])}?", None
    except wikipedia.PageError:
        return "😢 No Wikipedia page found for that query.", None
    except Exception:
        return "⚠️ Oops! Something went wrong.", None

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "😅 I couldn’t understand your voice clearly."
    except sr.RequestError:
        return "❌ Speech recognition service is down."

# --- Main Input UI ---
st.markdown('<div class="chat-row">', unsafe_allow_html=True)

user_query = st.text_input("💬 Ask me anything... curious cat 🐱:", key="chatbox", label_visibility="collapsed")

col1, col2 = st.columns([0.1, 0.1])

with col1:
    if st.button("🎙️", help="Tap to speak"):
        st.session_state['listening'] = not st.session_state.get('listening', False)
        if st.session_state['listening']:
            st.toast("🎤 Listening... Tap again to stop")
        else:
            st.toast("🛑 Stopped listening (voice not live)")

with col2:
    uploaded_file = st.file_uploader("+", type=["jpg", "jpeg", "png", "pdf", "txt"], label_visibility="collapsed")

st.markdown('</div>', unsafe_allow_html=True)

# --- File Handler ---
if uploaded_file:
    file_text = ""
    ext = uploaded_file.name.split('.')[-1].lower()

    if ext in ["jpg", "jpeg", "png"]:
        st.image(uploaded_file, use_column_width=True)
        user_query = st.text_input("🖼️ What's in the image?", key="img_q")
    elif ext == "pdf":
        reader = PdfReader(uploaded_file)
        file_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        st.text_area("📄 PDF Extract:", file_text[:2000])
        user_query = st.text_input("📝 Ask about this PDF:", key="pdf_q")
    elif ext == "txt":
        content = uploaded_file.read().decode("utf-8")
        st.text_area("📄 Text File:", content[:2000])
        user_query = st.text_input("📝 Ask about this TXT:", key="txt_q")

# --- Process Query ---
if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    cleaned = clean_query(user_query)
    summary, image_url = get_wikipedia_summary_and_image(cleaned)
    st.session_state.messages.append({"role": "bot", "content": summary})
    if image_url:
        st.image(image_url, use_column_width=True)

# --- Display Messages ---
for msg in st.session_state.messages:
    role_class = "user" if msg["role"] == "user" else "bot"
    speaker = "You" if msg["role"] == "user" else "Bot"
    st.markdown(f"<div class='message-box {role_class}'><strong>{speaker}:</strong> {msg['content']}</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
    <div class='footer'>
        Made with ❤️ using <a href='https://streamlit.io' target='_blank'>Streamlit</a> and
        <a href='https://pypi.org/project/wikipedia/' target='_blank'>Wikipedia API</a> 🧠<br>
        Stay curious, my friend 🐾✨
    </div>
""", unsafe_allow_html=True)

import streamlit as st
import wikipedia
import speech_recognition as sr
import tempfile
import os
import re
from pydub import AudioSegment
from streamlit_mic_recorder import mic_recorder  # Requires `streamlit-mic-recorder`

# --- Page Setup ---
st.set_page_config(
    page_title="Wikipedia Chatbot 🧠",
    page_icon="📚",
    layout="centered"
)

# --- Custom CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500&display=swap');
    html, body, [class*="css"] {
        font-family: 'Quicksand', sans-serif;
    }
    .message-box {
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 10px;
        line-height: 1.6;
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
        font-size: 0.9rem;
        color: #94a3b8;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
    <div style='text-align: center; padding-bottom: 10px;'>
        <h1 style='font-size: 2.6rem;'>📚 Wikipedia Chatbot</h1>
        <p style='font-size: 1.1rem; color: #9ca3af;'>Now with voice search 🎤 and image preview 🖼️</p>
    </div>
""", unsafe_allow_html=True)

# --- Chat State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Utilities ---
def clean_query(raw):
    raw = raw.lower()
    raw = re.sub(r"\b(who is|what is|tell me about|please|explain|define)\b", "", raw)
    return raw.strip()

def get_wikipedia_summary_and_image(query):
    try:
        results = wikipedia.search(query)
        if not results:
            return "😕 Sorry, I couldn't find anything on that topic.", None
        page = wikipedia.page(results[0], auto_suggest=False, redirect=True)
        summary = wikipedia.summary(results[0], sentences=2)
        image_url = page.images[0] if page.images else None
        return summary, image_url
    except wikipedia.DisambiguationError as e:
        return f"🤔 That was a bit ambiguous. Did you mean: {', '.join(e.options[:5])}?", None
    except wikipedia.PageError:
        return "😢 Sorry, I couldn't find a page matching your query.", None
    except Exception:
        return "⚠️ Oops, something went wrong while searching Wikipedia.", None

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand the audio."
    except sr.RequestError:
        return "Speech recognition service is unavailable."

# --- Text Input + Mic UI ---
col1, col2 = st.columns([10, 1])
with col1:
    user_input = st.text_input("💬 Ask me anything... curious cat 🐱:", key="text_input")

with col2:
    audio = mic_recorder(
        start_prompt="🎙️",
        stop_prompt="🛑",
        just_once=True,
        use_container_width=True
    )

if audio:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio["bytes"])
        transcript = transcribe_audio(tmp_file.name)
        os.unlink(tmp_file.name)
    if transcript:
        st.success(f"You said: {transcript}")
        user_input = transcript

# --- Voice Upload ---
audio_bytes = st.file_uploader("📁 Or upload a voice message (WAV/MP3):", type=["wav", "mp3"])
if audio_bytes:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        audio = AudioSegment.from_file(audio_bytes)
        audio.export(tmp_file.name, format="wav")
        transcript = transcribe_audio(tmp_file.name)
        os.unlink(tmp_file.name)
    if transcript:
        st.success(f"You said: {transcript}")
        user_input = transcript

# --- Handle Input ---
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    cleaned = clean_query(user_input)
    summary, image_url = get_wikipedia_summary_and_image(cleaned)
    st.session_state.messages.append({"role": "bot", "content": summary})
    if image_url:
        st.image(image_url, use_column_width=True)

# --- Chat History Display ---
for msg in st.session_state.messages:
    role_class = "user" if msg["role"] == "user" else "bot"
    speaker = "You" if msg["role"] == "user" else "Bot"
    st.markdown(f"<div class='message-box {role_class}'><strong>{speaker}:</strong> {msg['content']}</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
    <div class='footer'>
        🧠 Made with ❤️ using <a href='https://streamlit.io' target='_blank'>Streamlit</a> and <a href='https://pypi.org/project/wikipedia/' target='_blank'>Wikipedia API</a>.<br>
        Built for curious cats 🐱
    </div>
""", unsafe_allow_html=True)

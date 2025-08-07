import streamlit as st
import wikipedia
import speech_recognition as sr
import tempfile
import os
import re
from streamlit_mic_recorder import mic_recorder

# --- Page Config ---
st.set_page_config(
    page_title="Wikipedia Chatbot 🧠",
    page_icon="📚",
    layout="centered"
)

# --- Custom CSS for Cute Style ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Quicksand', sans-serif;
        }

        .message-box {
            padding: 12px 18px;
            border-radius: 12px;
            margin-bottom: 12px;
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
            margin-top: 50px;
            font-size: 0.9rem;
            color: #6b7280;
            text-align: center;
        }

        .chat-container {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .mic-button {
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            padding: 0;
        }

        .upload-note {
            font-size: 0.9rem;
            color: #6b7280;
        }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
    <div style='text-align: center; padding-bottom: 10px;'>
        <h1 style='font-size: 2.8rem;'>📚 Wikipedia Chatbot</h1>
        <p style='font-size: 1.1rem; color: #9ca3af;'>Now with voice input 🎤, image preview 🖼️, and file uploads 📁</p>
    </div>
""", unsafe_allow_html=True)

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "mic_active" not in st.session_state:
    st.session_state.mic_active = False

# --- Clean User Query ---
def clean_query(raw):
    raw = raw.lower()
    raw = re.sub(r"\b(who is|what is|tell me about|please|explain|define|the)\b", "", raw)
    return raw.strip()

# --- Wikipedia Fetch ---
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
        return f"🤔 Hmm, that was a bit broad. Did you mean: {', '.join(e.options[:5])}?", None
    except wikipedia.PageError:
        return "😢 Couldn't find a page that matches your query.", None
    except Exception:
        return "⚠️ Oops! Something went wrong while searching.", None

# --- Transcribe Audio ---
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

# --- Chat Input ---
col1, col2 = st.columns([8, 1])
with col1:
    user_input = st.text_input("💬 Ask me anything... curious cat 🐱", key="text_input")
with col2:
    mic_clicked = mic_recorder(
        start_prompt="🎙️", stop_prompt="🔴", key="mic", use_container_width=True
    )

# --- Handle Mic Input ---
if mic_clicked is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(mic_clicked)
        tmp_file_path = tmp_file.name
    transcript = transcribe_audio(tmp_file_path)
    os.unlink(tmp_file_path)
    if transcript:
        st.success(f"🗣️ You said: {transcript}")
        user_input = transcript

# --- File Upload (Non-audio) ---
uploaded_files = st.file_uploader(
    "📁 Upload files or images related to your question (optional):",
    type=["jpg", "jpeg", "png", "txt", "pdf"],
    accept_multiple_files=True
)

# --- Final Query Handling ---
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
    st.markdown(
        f"<div class='message-box {role_class}'><strong>{speaker}:</strong> {msg['content']}</div>",
        unsafe_allow_html=True
    )

# --- Display Uploaded Files (Optional) ---
if uploaded_files:
    st.markdown("### 📎 Uploaded Files Preview:")
    for file in uploaded_files:
        if file.type.startswith("image"):
            st.image(file, caption=file.name, use_column_width=True)
        elif file.type == "text/plain":
            st.text(f"📄 {file.name}")
            st.text(file.read().decode("utf-8")[:500])
        elif file.type == "application/pdf":
            st.markdown(f"📕 {file.name} (PDF uploaded)")

# --- Footer ---
st.markdown("""
    <div class='footer'>
        Made with ❤️ using <a href='https://streamlit.io' target='_blank'>Streamlit</a> + 
        <a href='https://pypi.org/project/wikipedia/' target='_blank'>Wikipedia API</a> 🐍<br>
        Stay curious, you adorable human 🐾
    </div>
""", unsafe_allow_html=True)

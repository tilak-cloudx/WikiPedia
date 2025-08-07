import streamlit as st
import wikipedia
import speech_recognition as sr
import tempfile
import os
import re
from st_audiorec import st_audiorec

st.set_page_config(
    page_title="Wikipedia Chatbot 🧠",
    page_icon="📚",
    layout="centered"
)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500&display=swap');
        html, body, [class*="css"]  {
            font-family: 'Quicksand', sans-serif;
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
            margin-top: 50px;
            font-size: 0.8rem;
            color: #6b7280;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: center; padding-bottom: 10px;'>
        <h1 style='font-size: 2.8rem;'>📚 Wikipedia Chatbot</h1>
        <p style='font-size: 1.1rem; color: #9ca3af;'>Now with voice search 🎤 and image preview 🖼️</p>
    </div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

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

user_input = st.text_input("💬 Ask me anything... curious cat 🐱:")

# Live Mic
st.markdown("### 🎙️ Or talk to the bot live:")
wav_audio_data = st_audiorec()
if wav_audio_data is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(wav_audio_data)
        tmp_file_path = tmp_file.name
    transcript = transcribe_audio(tmp_file_path)
    os.unlink(tmp_file_path)
    if transcript:
        st.success(f"You said: {transcript}")
        user_input = transcript

# Final Query Handling
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    cleaned = clean_query(user_input)
    summary, image_url = get_wikipedia_summary_and_image(cleaned)
    st.session_state.messages.append({"role": "bot", "content": summary})
    if image_url:
        st.image(image_url, use_column_width=True)

# Chat History
for msg in st.session_state.messages:
    role_class = "user" if msg["role"] == "user" else "bot"
    speaker = "You" if msg["role"] == "user" else "Bot"
    st.markdown(f"<div class='message-box {role_class}'><strong>{speaker}:</strong> {msg['content']}</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='footer'>
        Made with ❤️ using <a href='https://streamlit.io' target='_blank'>Streamlit</a> and <a href='https://pypi.org/project/wikipedia/' target='_blank'>Wikipedia API</a>.
    </div>
""", unsafe_allow_html=True)

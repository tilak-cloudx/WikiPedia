import streamlit as st
import wikipedia
import speech_recognition as sr
import tempfile
import os
import base64
import re
from pydub import AudioSegment

# --- Page Setup ---
st.set_page_config(page_title="Wikipedia Chatbot", page_icon="📚", layout="centered")

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "listening" not in st.session_state:
    st.session_state.listening = False

# --- Custom Style + Mic Button ---
mic_icon = "🎙️"
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: 'Quicksand', sans-serif;
    }
    .chat-input-container {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .mic-button {
        border: none;
        background: none;
        font-size: 24px;
        cursor: pointer;
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

st.markdown("<h1 style='text-align: center;'>📚 Wikipedia Chatbot</h1>", unsafe_allow_html=True)

# --- Clean Query ---
def clean_query(raw):
    raw = raw.lower()
    return re.sub(r"\b(who is|what is|tell me about|please|explain|define)\b", "", raw).strip()

# --- Wikipedia Fetch ---
def get_wikipedia_summary_and_image(query):
    try:
        results = wikipedia.search(query)
        if not results:
            return "😕 Sorry, I couldn't find anything.", None
        page = wikipedia.page(results[0], auto_suggest=False, redirect=True)
        summary = wikipedia.summary(results[0], sentences=2)
        image_url = page.images[0] if page.images else None
        return summary, image_url
    except wikipedia.DisambiguationError as e:
        return f"🤔 Too broad. Try one of: {', '.join(e.options[:5])}.", None
    except wikipedia.PageError:
        return "😢 No matching page found.", None
    except Exception:
        return "⚠️ Error searching Wikipedia.", None

# --- Transcription ---
def transcribe_audio(path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand."
    except sr.RequestError:
        return "Speech service unavailable."

# --- Audio Recorder (Pure JS Button) ---
st.markdown("### 💬 Ask me anything...")

audio_recorder_html = """
<script>
let mediaRecorder;
let audioChunks = [];

const recordBtn = window.parent.document.querySelector("button.mic-button");
const streamlitInput = window.parent.document.querySelectorAll('input[type="file"]')[0];

recordBtn.addEventListener("click", async () => {
    if (!mediaRecorder || mediaRecorder.state === "inactive") {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = e => {
            if (e.data.size > 0) audioChunks.push(e.data);
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const arrayBuffer = await audioBlob.arrayBuffer();
            const base64String = btoa(String.fromCharCode(...new Uint8Array(arrayBuffer)));
            window.parent.postMessage({ type: 'streamlit:setComponentValue', value: base64String }, '*');
        };

        mediaRecorder.start();
        recordBtn.innerText = "🛑 Listening...";
    } else {
        mediaRecorder.stop();
        recordBtn.innerText = "🎙️";
    }
});
</script>
"""

component_placeholder = st.empty()
mic_button = component_placeholder.button(mic_icon, key="mic", help="Click to talk", on_click=None)
st.components.v1.html(audio_recorder_html, height=0)

# --- Audio Handling from JS (base64 input) ---
b64_audio = st.experimental_get_query_params().get("audio_base64", [None])[0]
if b64_audio:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(base64.b64decode(b64_audio))
        tmp_path = tmp_file.name
    transcript = transcribe_audio(tmp_path)
    os.unlink(tmp_path)
    if transcript:
        st.session_state.messages.append({"role": "user", "content": transcript})
        cleaned = clean_query(transcript)
        summary, image_url = get_wikipedia_summary_and_image(cleaned)
        st.session_state.messages.append({"role": "bot", "content": summary})
        if image_url:
            st.image(image_url, use_column_width=True)

# --- Text Input Fallback ---
user_input = st.text_input("", placeholder="Type your question here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    cleaned = clean_query(user_input)
    summary, image_url = get_wikipedia_summary_and_image(cleaned)
    st.session_state.messages.append({"role": "bot", "content": summary})
    if image_url:
        st.image(image_url, use_column_width=True)

# --- Chat Display ---
for msg in st.session_state.messages:
    style = "user" if msg["role"] == "user" else "bot"
    speaker = "You" if msg["role"] == "user" else "Bot"
    st.markdown(f"<div class='message-box {style}'><strong>{speaker}:</strong> {msg['content']}</div>", unsafe_allow_html=True)

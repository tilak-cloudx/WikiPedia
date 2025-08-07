import streamlit as st
import wikipedia
import speech_recognition as sr
import tempfile
import os
from pydub import AudioSegment
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import av

# --- Page Config ---
st.set_page_config(
    page_title="Wikipedia Chatbot 🧠",
    page_icon="📚",
    layout="centered"
)

# --- Custom Font and Style ---
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

# --- Header ---
st.markdown("""
    <div style='text-align: center; padding-bottom: 10px;'>
        <h1 style='font-size: 2.8rem;'>📚 Wikipedia Chatbot</h1>
        <p style='font-size: 1.1rem; color: #9ca3af;'>Now with voice search 🎤 and image preview 🖼️</p>
    </div>
""", unsafe_allow_html=True)

# --- Initialize Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Wikipedia Summary + Image ---
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

# --- Voice Input Processing ---
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand the audio."
    except sr.RequestError:
        return "Speech recognition service is unavailable."

# --- Text Input ---
user_input = st.text_input("💬 Ask me anything... curious cat 🐱:")

# --- Voice Upload ---
audio_bytes = st.file_uploader("🎤 Or upload a voice message (WAV/MP3):", type=["wav", "mp3"])
if audio_bytes is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        audio = AudioSegment.from_file(audio_bytes)
        audio.export(tmp_file.name, format="wav")
        transcript = transcribe_audio(tmp_file.name)
        os.unlink(tmp_file.name)

        if transcript:
            st.success(f"You said: {transcript}")
            user_input = transcript

# --- Live Mic Input ---
st.markdown("### 🎙️ Or talk to the bot live:")

class AudioProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def recv(self, frame):
        audio_data = frame.to_ndarray().flatten().tobytes()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
            tmp_wav.write(audio_data)
            tmp_wav.close()
            try:
                with sr.AudioFile(tmp_wav.name) as source:
                    audio = self.recognizer.record(source)
                    text = self.recognizer.recognize_google(audio)
                    st.session_state.messages.append({"role": "user", "content": text})
                    summary, image = get_wikipedia_summary_and_image(text)
                    st.session_state.messages.append({"role": "bot", "content": summary})
            except Exception:
                st.error("⚠️ Could not process the audio.")
        return av.AudioFrame.from_ndarray(frame.to_ndarray(), layout="mono")

webrtc_streamer(
    key="live-mic",
    mode=WebRtcMode.SENDONLY,
    in_audio=True,
    client_settings=ClientSettings(
        media_stream_constraints={"audio": True, "video": False},
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    ),
    audio_processor_factory=AudioProcessor
)

# --- Handle Input (text or transcript) ---
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    summary, image_url = get_wikipedia_summary_and_image(user_input)
    st.session_state.messages.append({"role": "bot", "content": summary})

    if image_url:
        st.image(image_url, use_column_width=True)

# --- Display Chat ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='message-box user'><strong>You:</strong> {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='message-box bot'><strong>Bot:</strong> {msg['content']}</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
    <div class='footer'>
        Made with ❤️ using <a href='https://streamlit.io' target='_blank'>Streamlit</a> and <a href='https://pypi.org/project/wikipedia/' target='_blank'>Wikipedia API</a>.
    </div>
""", unsafe_allow_html=True)

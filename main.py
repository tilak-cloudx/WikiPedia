import streamlit as st
import wikipedia
import speech_recognition as sr
import pyttsx3
from io import BytesIO

# --- Page config ---
st.set_page_config(page_title="Wikipedia Chatbot", page_icon="📚", layout="centered")

# --- Custom CSS ---
st.markdown("""
    <style>
        .main {
            background-color: #0f172a;
            color: white;
        }
        .stTextInput>div>div>input {
            background-color: transparent;
            color: white;
            border: 1px solid #ef4444;
            border-radius: 6px;
            padding-right: 60px;
        }
        .icon-btn {
            position: absolute;
            right: 35px;
            top: 7px;
            cursor: pointer;
        }
        .file-btn {
            position: absolute;
            right: 5px;
            top: 7px;
            cursor: pointer;
        }
        .love-footer {
            text-align: center;
            font-size: 13px;
            color: #bbb;
            margin-top: 10px;
        }
        .love-footer span {
            color: red;
        }
    </style>
""", unsafe_allow_html=True)

# --- TTS engine ---
engine = pyttsx3.init()

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# --- Mic input ---
def mic_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.toast("🎙 Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except:
            return ""

# --- File upload handler ---
def handle_file_upload(file):
    if file:
        st.success(f"📁 Uploaded: {file.name}")
        # In real app: process file here

# --- Chat state ---
if "chat" not in st.session_state:
    st.session_state.chat = []

# --- Title ---
st.markdown("<h1 style='text-align:center;'>📚 Wikipedia Chatbot</h1>", unsafe_allow_html=True)

# --- Input container with icons ---
col1, col2 = st.columns([8, 1])
with col1:
    user_input = st.text_input("Ask me something from Wikipedia", label_visibility="collapsed")
with col2:
    mic_pressed = st.button("🎤")
    file_uploaded = st.file_uploader("", type=["jpg", "jpeg", "png", "txt", "pdf"], label_visibility="collapsed")

if mic_pressed:
    spoken = mic_input()
    if spoken:
        user_input = spoken
        st.experimental_rerun()

if file_uploaded:
    handle_file_upload(file_uploaded)

# --- Process input ---
if user_input:
    try:
        summary = wikipedia.summary(user_input, sentences=2)
        st.session_state.chat.append(("user", user_input))
        st.session_state.chat.append(("bot", summary))
        speak_text(summary)
    except wikipedia.exceptions.DisambiguationError as e:
        msg = f"⚠ Too many results: {e.options[:5]}"
        st.session_state.chat.append(("bot", msg))
    except wikipedia.exceptions.PageError:
        msg = "❌ No page found for your query."
        st.session_state.chat.append(("bot", msg))

# --- Display chat ---
for sender, message in st.session_state.chat:
    if sender == "user":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🤖 Bot:** {message}")
        st.markdown('<div class="love-footer">Made with <span>❤️</span> by Likhiii</div>', unsafe_allow_html=True)

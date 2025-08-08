import streamlit as st
import wikipedia
import tempfile
import speech_recognition as sr
from gtts import gTTS
import base64
import os
from streamlit_mic_recorder import mic_recorder

st.set_page_config(page_title="Wikipedia Chatbot", page_icon="📚", layout="centered")

st.markdown(
    """
    <style>
    .stTextInput > div {
        display: flex;
        align-items: center;
        position: relative;
    }
    .chat-input-container {
        position: relative;
        width: 100%;
    }
    .chat-icons {
        position: absolute;
        right: 8px;
        top: 50%;
        transform: translateY(-50%);
        display: flex;
        gap: 6px;
    }
    .icon-btn {
        background: none;
        border: none;
        font-size: 18px;
        cursor: pointer;
        color: #555;
        padding: 4px;
    }
    .icon-btn:hover {
        color: black;
    }
    input[type="file"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align:center;'>📚 Wikipedia Chatbot</h1>", unsafe_allow_html=True)

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to get wiki answer
def get_wiki_answer(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except:
        return "Sorry, I couldn't find anything on Wikipedia for that."

# Function to speak bot reply
def speak_text(text):
    tts = gTTS(text=text, lang='en', tld='co.in', slow=False)  # cute female voice
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp.name)
    audio_file = open(tmp.name, "rb").read()
    audio_b64 = base64.b64encode(audio_file).decode()
    audio_html = f"""
    <audio autoplay>
        <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# Function to handle user query
def handle_query(query):
    if query.strip():
        bot_reply = get_wiki_answer(query)
        st.session_state.chat_history.append(("You", query))
        st.session_state.chat_history.append(("Bot", bot_reply))
        speak_text(bot_reply)

# Display chat history
for sender, msg in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"🧑 **You:** {msg}")
    else:
        st.markdown(f"🤖 **Bot:** {msg}")

# Mic recording
audio = mic_recorder(start_prompt="🎤 Start speaking", stop_prompt="⏹ Stop recording", just_once=True, use_container_width=False)

# If mic recorded audio, transcribe and handle
if audio:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
        tmp_audio.write(audio["bytes"])
        recognizer = sr.Recognizer()
        with sr.AudioFile(tmp_audio.name) as source:
            audio_data = recognizer.record(source)
            try:
                query_from_voice = recognizer.recognize_google(audio_data)
                handle_query(query_from_voice)
            except sr.UnknownValueError:
                st.error("Could not understand your voice input.")

# Text input
user_input = st.text_input(
    "",
    key="chat_input",
    label_visibility="collapsed",
    placeholder="Type your question and press Enter..."
)

if user_input:
    handle_query(user_input)
    st.session_state.chat_input = ""  # clear box

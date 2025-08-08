import streamlit as st
import wikipedia
import speech_recognition as sr
from PIL import Image
import io

# --- Page Config ---
st.set_page_config(page_title="Wikipedia Chatbot", page_icon="📚", layout="centered")

# --- Custom CSS ---
st.markdown("""
    <style>
        body {
            font-family: 'Inter', sans-serif;
        }
        .stTextInput input {
            border: 2px solid #ef4444;
            border-radius: 8px;
        }
        .bot-message {
            background-color: #111827;
            padding: 10px;
            border-radius: 8px;
            margin-top: 10px;
            color: white;
        }
        .footer {
            text-align: center;
            color: #aaa;
            font-size: 12px;
            margin-top: 5px;
        }
        .mic-button, .upload-button {
            display: inline-block;
            vertical-align: middle;
            margin-left: 6px;
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Speech-to-Text ---
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙 Listening... Speak now.")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        st.success(f"✅ You said: {text}")
        return text
    except sr.UnknownValueError:
        st.error("Sorry, I couldn't understand.")
    except sr.RequestError:
        st.error("Speech recognition service error.")
    return ""

# --- Wikipedia Search ---
def search_wikipedia(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Your query is ambiguous. Suggestions: {', '.join(e.options[:5])}"
    except wikipedia.exceptions.PageError:
        return "No page found for your query."
    except Exception as e:
        return f"Error: {str(e)}"

# --- Header ---
st.markdown("<h1 style='text-align:center;'>📚 Wikipedia Chatbot</h1>", unsafe_allow_html=True)

# --- Input Row ---
col1, col2, col3 = st.columns([6, 1, 1])
with col1:
    user_input = st.text_input("", placeholder="Ask me anything from Wikipedia...", label_visibility="collapsed")
with col2:
    if st.button("🎤", help="Speak"):
        spoken_text = recognize_speech()
        if spoken_text:
            user_input = spoken_text
with col3:
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png", "txt", "pdf"], label_visibility="collapsed")

# --- Process Query ---
if user_input:
    bot_reply = search_wikipedia(user_input)
    st.session_state.messages.append({"user": user_input, "bot": bot_reply})

# --- Chat Display ---
for msg in st.session_state.messages:
    st.markdown(f"**👤 You:** {msg['user']}")
    st.markdown(f"<div class='bot-message'>🤖 <b>Bot:</b> {msg['bot']}</div>", unsafe_allow_html=True)
    st.markdown("<div class='footer'>Made with ❤️ by Likhiii</div>", unsafe_allow_html=True)

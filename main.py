import streamlit as st
import wikipedia
from gtts import gTTS
import tempfile
import base64
import time

st.set_page_config(page_title="Cute Wikipedia Chatbot", page_icon="📚", layout="centered")

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "music_on" not in st.session_state:
    st.session_state.music_on = False

# --- CSS STYLES ---
st.markdown("""
<style>
body {
    background: linear-gradient(-45deg, #ffdde1, #ee9ca7, #c1c8e4, #fbc2eb, #a1c4fd);
    background-size: 400% 400%;
    animation: gradientShift 12s ease infinite;
}
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Chat bubbles */
.chat-bubble {
    padding: 10px 15px;
    border-radius: 20px;
    margin: 8px 0;
    max-width: 80%;
    display: inline-block;
    animation: fadeIn 0.3s ease-in-out;
}
.user-bubble {
    background-color: #ffe4ec;
    align-self: flex-end;
    color: #333;
}
.bot-bubble {
    background-color: #e4f0ff;
    color: #333;
}
.avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: inline-block;
    vertical-align: middle;
    margin-right: 8px;
}
.chat-row {
    display: flex;
    align-items: flex-start;
}
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(5px);}
    to {opacity: 1; transform: translateY(0);}
}

/* Falling sakura petals */
.petal {
    position: fixed;
    top: -10px;
    background: pink;
    border-radius: 150% 0 150% 0;
    opacity: 0.8;
    pointer-events: none;
    animation: fall linear infinite;
}
@keyframes fall {
    0% { transform: translateY(-10px) rotate(0deg); }
    100% { transform: translateY(110vh) rotate(360deg); }
}
</style>
""", unsafe_allow_html=True)

# --- PETALS GENERATOR ---
petals_html = ""
import random
for i in range(20):
    left = random.randint(0, 100)
    size = random.randint(8, 15)
    duration = random.randint(10, 20)
    delay = random.randint(0, 15)
    petals_html += f'<div class="petal" style="left:{left}%; width:{size}px; height:{size}px; animation-duration:{duration}s; animation-delay:{delay}s;"></div>'
st.markdown(petals_html, unsafe_allow_html=True)

# --- FUNCTIONS ---
def display_message(role, text):
    if role == "user":
        st.markdown(f"""
        <div class="chat-row" style="justify-content: flex-end;">
            <div class="chat-bubble user-bubble">{text}</div>
            <img src="https://i.ibb.co/znz7tbn/user.png" class="avatar">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-row">
            <img src="https://i.ibb.co/XZ7j5ML/robot.png" class="avatar">
            <div class="chat-bubble bot-bubble">{text}</div>
        </div>
        """, unsafe_allow_html=True)

# --- TITLE ---
st.markdown("<h1 style='text-align:center;'>📚 Cute Wikipedia Chatbot</h1>", unsafe_allow_html=True)

# --- MUSIC TOGGLE ---
if st.button("🎶 Toggle Music"):
    st.session_state.music_on = not st.session_state.music_on
if st.session_state.music_on:
    st.audio("https://www.bensound.com/bensound-music/bensound-sunny.mp3", autoplay=True)

# --- USER INPUT ---
user_input = st.text_input("Ask something...", placeholder="Type your question and press Enter...")

# --- CHAT LOGIC ---
if user_input:
    st.session_state.messages.append(("user", user_input))
    display_message("user", user_input)

    with st.spinner("Bot is typing..."):
        time.sleep(1)
        try:
            summary = wikipedia.summary(user_input, sentences=2)
        except wikipedia.exceptions.DisambiguationError as e:
            summary = f"Your query was too broad. Try one of these: {e.options[:5]}"
        except wikipedia.exceptions.PageError:
            summary = "Sorry, I couldn't find anything on Wikipedia for that topic."

    st.session_state.messages.append(("bot", summary))
    display_message("bot", summary)

    # Voice output
    tts = gTTS(text=summary, lang='en', tld='co.in')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tts.save(tmp_file.name)
        audio_bytes = open(tmp_file.name, "rb").read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        audio_html = f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)

# --- DISPLAY HISTORY ---
for role, text in st.session_state.messages:
    display_message(role, text)

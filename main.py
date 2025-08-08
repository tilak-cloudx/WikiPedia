import streamlit as st
import wikipedia
from gtts import gTTS
import tempfile
import base64
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="Cute Multi-Source Chatbot", page_icon="📚", layout="centered")

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "music_on" not in st.session_state:
    st.session_state.music_on = False

# --- CUTE BACKGROUND + PETALS CSS ---
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

/* Falling petals */
.petal {
    position: fixed;
    top: -10px;
    background: pink;
    border-radius: 150% 0 150% 0;
    opacity: 0.8;
    animation: fall linear infinite;
    z-index: 9999;
}
@keyframes fall {
    0% { transform: translateY(0) rotate(0deg); }
    100% { transform: translateY(110vh) rotate(360deg); }
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
</style>
""", unsafe_allow_html=True)

# --- PETALS HTML ---
if "petals_added" not in st.session_state:
    petals_html = "".join([
        f'<div class="petal" style="left:{i*10}%; width:10px; height:10px; animation-duration:{4+i%5}s; animation-delay:{i%3}s;"></div>'
        for i in range(10)
    ])
    st.markdown(petals_html, unsafe_allow_html=True)
    st.session_state.petals_added = True

# --- MUSIC TOGGLE ---
if st.button("🎶 Toggle Music"):
    st.session_state.music_on = not st.session_state.music_on

if st.session_state.music_on:
    st.markdown("""
        <audio autoplay loop>
            <source src="https://www.bensound.com/bensound-music/bensound-sunny.mp3" type="audio/mp3">
        </audio>
    """, unsafe_allow_html=True)

# --- DISPLAY CHAT BUBBLES ---
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
st.markdown("<h1 style='text-align:center;'>📚 Cute Multi-Source Chatbot</h1>", unsafe_allow_html=True)

# --- USER INPUT ---
user_input = st.text_input("Ask something...", placeholder="Type your question and press Enter...")

# --- PROCESS USER INPUT ---
if user_input:
    st.session_state.messages.append(("user", user_input))
    display_message("user", user_input)

    with st.spinner("Bot is typing..."):
        time.sleep(1)

        # Default to Wikipedia search
        try:
            summary = wikipedia.summary(user_input, sentences=2)
        except wikipedia.exceptions.DisambiguationError as e:
            summary = f"Your query was too broad. Try one of these: {e.options[:5]}"
        except wikipedia.exceptions.PageError:
            summary = "Sorry, I couldn't find anything on Wikipedia for that topic."

        # Add bot reply
        st.session_state.messages.append(("bot", summary))
        display_message("bot", summary)

        # Voice reply
        tts = gTTS(text=summary, lang='en', tld='co.in')
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tts.save(tmp_file.name)
            audio_bytes = open(tmp_file.name, "rb").read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
            st.markdown(f"""
                <audio autoplay>
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                </audio>
            """, unsafe_allow_html=True)

# --- DISPLAY CHAT HISTORY ---
for role, text in st.session_state.messages:
    display_message(role, text)

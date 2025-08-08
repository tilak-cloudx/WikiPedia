import streamlit as st
import wikipedia
from gtts import gTTS
import tempfile
import base64
import time

st.set_page_config(page_title="Ask Meh Anything Buddy...", page_icon="📚", layout="centered")

# --- Sidebar ---
with st.sidebar:
    st.markdown("<h2>💖 About Us</h2>", unsafe_allow_html=True)
    st.write("""
    Welcome to **Ask Meh Anything Buddy...**!  
    I'm your friendly bot that answers your questions from Wikipedia in the most adorable way possible 💕  
    You can listen to my answers, see images, and enjoy falling sakura petals 🌸.
    """)
    st.markdown("<h2>📌 User Guidance</h2>", unsafe_allow_html=True)
    st.write("""
    1. Type your question in the box.  
    2. Press **Enter** to ask.  
    3. Enjoy the petals, music 🎶, and images.  
    4. Toggle music on/off from the button.  
    """)
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit & Wikipedia API")

# --- Session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "music_on" not in st.session_state:
    st.session_state.music_on = False

# --- CSS for background, petals, chat bubbles ---
st.markdown("""
<style>
/* Animated gaming newspaper background */
body {
    background: black;
}
[data-testid="stAppViewContainer"] {
    background: url('https://www.transparenttextures.com/patterns/newspaper.png'), black;
    animation: scrollBg 30s linear infinite;
}
@keyframes scrollBg {
    from { background-position: 0 0; }
    to { background-position: 100% 100%; }
}

/* Glitching text background effect */
@keyframes glitch {
    0% { clip-path: inset(0 0 0 0); }
    20% { clip-path: inset(10% 0 85% 0); }
    40% { clip-path: inset(80% 0 5% 0); }
    60% { clip-path: inset(30% 0 50% 0); }
    80% { clip-path: inset(60% 0 30% 0); }
    100% { clip-path: inset(0 0 0 0); }
}
.glitch {
    font-size: 60px;
    font-weight: bold;
    text-align: center;
    color: white;
    animation: glitch 2s infinite;
}

/* Sakura petals */
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
    margin-right: 8px;
}
.chat-row {
    display: flex;
    align-items: flex-start;
}
</style>
""", unsafe_allow_html=True)

# --- Petals ---
petals_html = "".join([
    f'<div class="petal" style="left:{i*10}%; width:10px; height:10px; animation-duration:{4+i%5}s; animation-delay:{i%3}s;"></div>'
    for i in range(10)
])
st.markdown(petals_html, unsafe_allow_html=True)

# --- Music toggle ---
if st.button("🎶 Toggle Music"):
    st.session_state.music_on = not st.session_state.music_on

if st.session_state.music_on:
    music_html = """
        <audio autoplay loop>
            <source src="https://www.bensound.com/bensound-music/bensound-sunny.mp3" type="audio/mp3">
        </audio>
    """
    st.markdown(music_html, unsafe_allow_html=True)

# --- Chat bubble function ---
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

# --- Title ---
st.markdown('<div class="glitch">📚 Ask Meh Anything Buddy...</div>', unsafe_allow_html=True)

# --- User input ---
user_input = st.text_input("Ask something...", key="input_text", placeholder="Type your question and press Enter...")

if user_input:
    st.session_state.messages.append(("user", user_input))
    display_message("user", user_input)

    with st.spinner("Bot is typing..."):
        time.sleep(1)
        try:
            page = wikipedia.page(user_input)
            summary = page.summary[:500] + "..."
            image_url = next((img for img in page.images if img.lower().endswith((".jpg", ".jpeg", ".png")) and "svg" not in img.lower()), None)
        except wikipedia.exceptions.DisambiguationError as e:
            summary = f"Your query was too broad. Try: {', '.join(e.options[:5])}"
            image_url = None
        except wikipedia.exceptions.PageError:
            summary = "Sorry, I couldn't find anything on Wikipedia for that topic."
            image_url = None

    st.session_state.messages.append(("bot", summary))
    display_message("bot", summary)

    if image_url:
        st.image(image_url, width=300)

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

# --- Display history ---
for role, text in st.session_state.messages:
    display_message(role, text)

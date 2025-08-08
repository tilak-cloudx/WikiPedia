import streamlit as st
import wikipedia
from gtts import gTTS
import tempfile
import base64
import time

st.set_page_config(page_title="Ask Meh Anything Buddy...", page_icon="📚", layout="centered")

# --- Custom CSS for animated newspaper background & petals ---
st.markdown("""
<style>
/* Animated newspaper texture background for whole app */
[data-testid="stAppViewContainer"] {
    background: url('https://www.transparenttextures.com/patterns/newspaper.png') repeat;
    animation: scrollBg 60s linear infinite;
}
@keyframes scrollBg {
    from { background-position: 0 0; }
    to { background-position: 100% 100%; }
}

/* Transparent backgrounds so the texture shows */
[data-testid="stVerticalBlock"],
[data-testid="stChatMessage"] {
    background-color: transparent !important;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: rgba(0,0,0,0.6);
    color: white;
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
</style>
""", unsafe_allow_html=True)

# --- Floating Sakura Petals ---
petals_html = "".join([
    f'<div class="petal" style="left:{i*10}%; width:10px; height:10px; animation-duration:{4+i%5}s; animation-delay:{i%3}s;"></div>'
    for i in range(10)
])
st.markdown(petals_html, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("<h2>💖 About Us</h2>", unsafe_allow_html=True)
    st.write("""
    Welcome to **Ask Meh Anything Buddy**!  
    I'm your friendly bot that answers your questions from Wikipedia 💕  
    You can listen to my answers, see images, and enjoy petals 🌸.
    """)
    st.markdown("<h2>📌 User Guidance</h2>", unsafe_allow_html=True)
    st.write("""
    1. Type your question below.  
    2. Press Enter to ask.  
    3. Enjoy the petals, music 🎶, and images.  
    4. Toggle music with the button.  
    5. Have fun!
    """)
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit & Wikipedia API")

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "music_on" not in st.session_state:
    st.session_state.music_on = False

# --- Music Toggle ---
if st.button("🎶 Toggle Music"):
    st.session_state.music_on = not st.session_state.music_on
if st.session_state.music_on:
    st.markdown("""
        <audio autoplay loop>
            <source src="https://www.bensound.com/bensound-music/bensound-sunny.mp3" type="audio/mp3">
        </audio>
    """, unsafe_allow_html=True)

# --- Chat Display ---
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
st.markdown("<h1 style='text-align:center;'>📚 Ask Meh Anything Buddy...</h1>", unsafe_allow_html=True)

# --- Input ---
user_input = st.text_input("Ask something...", key="input_text", placeholder="Type your question here...")

# --- Wikipedia Search ---
if user_input:
    st.session_state.messages.append(("user", user_input))
    display_message("user", user_input)

    with st.spinner("Searching Wikipedia..."):
        time.sleep(1)
        try:
            page = wikipedia.page(user_input)
            summary = page.summary[:500] + "..."
            image_url = next((img for img in page.images if img.lower().endswith((".jpg", ".jpeg", ".png")) and "svg" not in img.lower()), None)
        except wikipedia.exceptions.DisambiguationError as e:
            summary = f"Too broad. Try one of these: {e.options[:5]}"
            image_url = None
        except wikipedia.exceptions.PageError:
            summary = "Sorry, I couldn't find anything."
            image_url = None

    st.session_state.messages.append(("bot", summary))
    display_message("bot", summary)

    if image_url:
        st.image(image_url, width=300)

    # Voice Output
    tts = gTTS(text=summary, lang='en', tld='co.in')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tts.save(tmp.name)
        audio_bytes = open(tmp.name, "rb").read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        st.markdown(f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        """, unsafe_allow_html=True)

# --- Show Chat History ---
for role, text in st.session_state.messages:
    display_message(role, text)

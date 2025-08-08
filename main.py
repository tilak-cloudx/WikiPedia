import streamlit as st
import wikipedia
from gtts import gTTS
import tempfile
import base64
import time
import random

st.set_page_config(page_title="Ask Meh Anything Buddy...", page_icon="🖥️", layout="centered")

with st.sidebar:
    st.markdown("<h2 style='color:#0ff; font-family: JetBrains Mono, monospace;'>💻 FULL STACKER BUDDY</h2>", unsafe_allow_html=True)
    st.write("""
    Your cyberpunk Wikipedia bot —  
    powered by neon lights, glitch effects & code vibes.  
    Ask your questions, get lightning-fast answers,  
    with voice and images in terminal style.
    """)
    st.markdown("---")
    st.markdown("<p style='font-family: JetBrains Mono, monospace; color:#0f0;'>1. Type your query.<br>2. Hit Enter.<br>3. Watch the bot work magic.<br>4. Toggle neon beats 🎵</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<p style='font-family: JetBrains Mono, monospace; color:#0ff;'>Built with ❤️ and caffeine.</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "music_on" not in st.session_state:
    st.session_state.music_on = False
if "new_bot_message" not in st.session_state:
    st.session_state.new_bot_message = False

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono&display=swap');

body, .stApp {
    background-color: #0d0f14 !important;
    background-image:
      linear-gradient(rgba(0, 255, 255, 0.05) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0, 255, 255, 0.05) 1px, transparent 1px);
    background-size: 20px 20px;
    color: #0ff !important;
    font-family: 'JetBrains Mono', monospace !important;
    overflow-x: hidden;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background-color: #11141a !important;
    border-right: 2px solid #0ff;
}

/* Chat container for flex alignment */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    max-width: 700px;
    margin: 0 auto 30px auto;
}

/* Chat bubbles with glitch/neon style */
.chat-bubble {
    padding: 12px 18px;
    border-radius: 4px;
    max-width: 80%;
    white-space: pre-wrap;
    box-shadow:
      0 0 5px #0ff,
      0 0 10px #0ff,
      0 0 20px #0ff;
    position: relative;
    font-size: 16px;
    line-height: 1.4;
    letter-spacing: 0.8px;
    user-select: text;
}

.user-bubble {
    background: #051517;
    border: 1px solid #0ff;
    color: #0ff;
    align-self: flex-end;
    font-weight: 600;
}

.bot-bubble {
    background: #011a27;
    border: 1px solid #39ff14;
    color: #39ff14;
    align-self: flex-start;
    font-family: 'Fira Code', monospace;
    font-size: 15px;
    /* glitch animation */
    animation: glitch-flicker 3s linear forwards;
}

/* Glitch flicker effect for bot */
@keyframes glitch-flicker {
  0%, 100% { opacity: 1; text-shadow: 0 0 4px #39ff14, 0 0 8px #39ff14; }
  20% { opacity: 0.7; text-shadow: 0 0 8px #39ff14, 0 0 16px #0f0; }
  40% { opacity: 1; text-shadow: 0 0 6px #39ff14, 0 0 10px #0f0; }
  60% { opacity: 0.9; text-shadow: 0 0 8px #39ff14, 0 0 15px #0f0; }
  80% { opacity: 1; text-shadow: 0 0 10px #39ff14, 0 0 18px #0f0; }
}

/* Typewriter effect with blinking cursor */
@keyframes typing {
    from { width: 0 }
    to { width: 100% }
}
@keyframes blink-caret {
    0%, 100% { border-color: transparent; }
    50% { border-color: #39ff14; }
}
.typewriter {
    overflow: hidden;
    white-space: nowrap;
    border-right: .15em solid #39ff14;
    animation: typing 3s steps(40, end), blink-caret 0.75s step-end infinite;
    font-family: 'Fira Code', monospace;
}

/* Input box style */
div.stTextInput > label {
    font-family: 'JetBrains Mono', monospace !important;
    color: #0ff !important;
    font-weight: 600;
}

input[type="text"] {
    background-color: #011a27 !important;
    border: 2px solid #39ff14 !important;
    color: #0f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 16px !important;
    padding: 8px !important;
    border-radius: 4px !important;
}

/* Button style */
.stButton>button {
    background-color: #0ff !important;
    color: #011a27 !important;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace !important;
    border-radius: 4px !important;
    border: none !important;
    padding: 8px 16px !important;
    cursor: pointer;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background-color: #39ff14 !important;
    color: #000 !important;
}

/* Hide Streamlit footer */
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Petals redesigned as glowing neon sparks instead ---
sparks_html = ""
for i in range(20):
    left = random.randint(0, 100)
    size = random.randint(4, 10)
    duration = random.uniform(3, 6)
    delay = random.uniform(0, 5)
    sparks_html += f'''
    <div style="
        position: fixed;
        top: -10px;
        left: {left}%;
        width: {size}px;
        height: {size}px;
        background: #0ff;
        border-radius: 50%;
        opacity: 0.7;
        box-shadow: 0 0 10px #0ff, 0 0 20px #0ff;
        animation: fall {duration}s linear infinite;
        animation-delay: {delay}s;
        z-index: 9999;
        filter: drop-shadow(0 0 5px #0ff);
    "></div>
    '''
st.markdown(sparks_html, unsafe_allow_html=True)

def display_message(role, text, animate=False):
    cls = "user-bubble" if role == "user" else "bot-bubble"
    typewriter_class = "typewriter" if animate else ""
    st.markdown(f"""
    <div class="chat-bubble {cls} {typewriter_class}">{text}</div>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; font-family: JetBrains Mono, monospace; color:#0ff; text-shadow: 0 0 5px #0ff;'>🖥️ FULL STACKER BUDDY</h1>", unsafe_allow_html=True)

user_input = st.text_input("Ask anything about Wikipedia...", key="input_text", placeholder="Type your question and press Enter...")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "music_on" not in st.session_state:
    st.session_state.music_on = False
if "new_bot_message" not in st.session_state:
    st.session_state.new_bot_message = False

if st.button("🎧 Toggle Neon Beats"):
    st.session_state.music_on = not st.session_state.music_on

if st.session_state.music_on:
    st.markdown("""
        <audio autoplay loop>
            <source src="https://www.bensound.com/bensound-music/bensound-epic.mp3" type="audio/mp3">
        </audio>
    """, unsafe_allow_html=True)

if user_input:
    st.session_state.messages.append(("user", user_input))
    display_message("user", user_input)

    with st.spinner("Crunching data..."):
        time.sleep(1)
        try:
            page = wikipedia.page(user_input)
            summary = page.summary[:500] + "..."
            image_url = None
            for img in page.images:
                if img.lower().endswith((".jpg", ".jpeg", ".png")) and "svg" not in img.lower():
                    image_url = img
                    break
        except wikipedia.exceptions.DisambiguationError as e:
            summary = f"Multiple results found! Try: {', '.join(e.options[:5])}"
            image_url = None
        except wikipedia.exceptions.PageError:
            summary = "Can't find anything on that. Try something else."
            image_url = None

    st.session_state.messages.append(("bot", summary))
    st.session_state.new_bot_message = True

    if image_url:
        st.image(image_url, width=320, caption="🖼️ Image from Wikipedia")

    tts = gTTS(text=summary, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tts.save(tmp_file.name)
        audio_bytes = open(tmp_file.name, "rb").read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        st.markdown(f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        """, unsafe_allow_html=True)

st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for i, (role, text) in enumerate(st.session_state.messages):
    animate = (role == "bot" and i == len(st.session_state.messages) - 1 and st.session_state.new_bot_message)
    display_message(role, text, animate=animate)
st.markdown('</div>', unsafe_allow_html=True)
st.session_state.new_bot_message = False

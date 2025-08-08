import streamlit as st
import wikipedia
from gtts import gTTS
import tempfile
import base64
import time
import random

# --- Page config ---
st.set_page_config(page_title="Ask Meh Anything Buddy...", page_icon="📚", layout="centered")

# --- Sidebar ---
with st.sidebar:
    st.markdown("<h2>💖 About Us</h2>", unsafe_allow_html=True)
    st.write("""
    Welcome to **Ask Meh Anything Buddy...**!  
    Your cute Wikipedia-powered chatbot with voice, images, music, and petals 🌸.  
    Now with a vintage newspaper vibe 📰.
    """)

    st.markdown("<h2>📌 User Guidance</h2>", unsafe_allow_html=True)
    st.write("""
    1. Type your question in the box.  
    2. Press **Enter** to ask.  
    3. Enjoy the petals 🌸, music 🎶, and newspaper-style background.  
    4. Toggle music from the button.  
    5. Relax and enjoy 💫.
    """)

    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit & Wikipedia API")

# --- Session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "music_on" not in st.session_state:
    st.session_state.music_on = False
if "new_bot_message" not in st.session_state:
    st.session_state.new_bot_message = False

# --- CSS for background & animations ---
st.markdown("""
<style>
body, .stApp {
    background-color: #fdf6e3 !important;
    background-image: url('https://www.transparenttextures.com/patterns/newsprint.png') !important;
    color: #222 !important;
    font-family: 'Times New Roman', serif !important;
    overflow-x: hidden;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background-color: #f8f5e1 !important;
}

/* Sakura petals */
.petal {
    position: fixed;
    top: -10px;
    background: pink;
    border-radius: 150% 0 150% 0;
    opacity: 0.8;
    animation-name: fall;
    animation-timing-function: linear;
    animation-iteration-count: infinite;
    z-index: 9999;
}
@keyframes fall {
    0% { transform: translateY(0) rotate(0deg); }
    100% { transform: translateY(110vh) rotate(360deg); }
}

/* Chat bubbles */
.chat-bubble {
    padding: 10px 15px;
    border-radius: 10px;
    margin: 8px 0;
    max-width: 80%;
    display: inline-block;
    word-wrap: break-word;
}
.user-bubble {
    background-color: #fce4ec;
    color: #222;
    align-self: flex-end;
}
.bot-bubble {
    background-color: #fff3e0;
    color: #222;
    font-family: 'Courier New', monospace;
    white-space: pre-wrap;
    align-self: flex-start;
}

/* Typewriter animation */
@keyframes typing {
    from { width: 0 }
    to { width: 100% }
}
.typewriter {
    overflow: hidden;
    border-right: .15em solid orange;
    white-space: nowrap;
    animation: typing 3s steps(40, end);
}
.chat-container {
    display: flex;
    flex-direction: column;
}

/* Hide Streamlit footer */
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Create petals with random positions, sizes and durations ---
petals_html = ""
for i in range(15):
    left = random.randint(0, 100)
    size = random.randint(8, 18)
    duration = random.uniform(4, 8)
    delay = random.uniform(0, 5)
    petals_html += f'<div class="petal" style="left:{left}%; width:{size}px; height:{size}px; animation-duration:{duration}s; animation-delay:{delay}s;"></div>'
st.markdown(petals_html, unsafe_allow_html=True)

# --- Music toggle ---
if st.button("🎶 Toggle Music"):
    st.session_state.music_on = not st.session_state.music_on

if st.session_state.music_on:
    st.markdown("""
        <audio autoplay loop>
            <source src="https://www.bensound.com/bensound-music/bensound-sunny.mp3" type="audio/mp3">
        </audio>
    """, unsafe_allow_html=True)

# --- Display message ---
def display_message(role, text, animate=False):
    cls = "user-bubble" if role == "user" else "bot-bubble"
    typewriter_class = "typewriter" if animate else ""
    st.markdown(f"""
    <div class="chat-bubble {cls} {typewriter_class}">{text}</div>
    """, unsafe_allow_html=True)

# --- Title ---
st.markdown("<h1 style='text-align:center;'>📚 Ask Meh Anything Buddy...</h1>", unsafe_allow_html=True)

# --- User Input ---
user_input = st.text_input("Ask something...", key="input_text", placeholder="Type your question and press Enter...")

# --- When user submits ---
if user_input:
    st.session_state.messages.append(("user", user_input))
    display_message("user", user_input)

    with st.spinner("Buddy is thinking..."):
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
            summary = f"Too many results! Try: {', '.join(e.options[:5])}"
            image_url = None
        except wikipedia.exceptions.PageError:
            summary = "Sorry buddy, I couldn't find anything for that."
            image_url = None

    st.session_state.messages.append(("bot", summary))
    st.session_state.new_bot_message = True

    # Show image if available
    if image_url:
        st.image(image_url, width=300)

    # Voice output
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

# --- Display chat history ---
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for i, (role, text) in enumerate(st.session_state.messages):
    # Animate only the latest bot message
    animate = (role == "bot" and i == len(st.session_state.messages) - 1 and st.session_state.new_bot_message)
    display_message(role, text, animate=animate)
st.markdown('</div>', unsafe_allow_html=True)

# Reset animation flag after displaying
st.session_state.new_bot_message = False

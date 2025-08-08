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
    5. Upload files with the glowing + button!  
    6. Relax and enjoy 💫.
    """)

    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit & Wikipedia API")

# --- Session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "music_on" not in st.session_state:
    st.session_state.music_on = False
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# --- CSS for background & animations ---
st.markdown("""
<style>
body {
    background-color: #fdf6e3;
    background-image: url('https://www.transparenttextures.com/patterns/newsprint.png');
    color: #222;
    font-family: 'Times New Roman', serif;
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
    border-radius: 10px;
    margin: 8px 0;
    max-width: 80%;
    display: inline-block;
    word-wrap: break-word;
}
.user-bubble {
    background-color: #fce4ec;
    color: #222;
}
.bot-bubble {
    background-color: #fff3e0;
    color: #222;
    font-family: 'Courier New', monospace;
    white-space: pre-wrap;
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

/* + upload button styles */
#upload-label {
    font-size: 28px;
    cursor: pointer;
    color: #ff00de;
    user-select: none;
    line-height: 1;
    padding-left: 6px;
    vertical-align: middle;
}
#file-uploader {
    display: none;
}

/* Responsive */
@media only screen and (max-width: 600px) {
    .chat-bubble {
        max-width: 95% !important;
        font-size: 14px !important;
        padding: 8px 12px !important;
        border-radius: 12px !important;
    }
    input[type="text"] {
        width: 95% !important;
        font-size: 16px !important;
        padding: 10px !important;
    }
    .stButton>button {
        width: 95% !important;
        font-size: 16px !important;
        padding: 10px !important;
    }
    section[data-testid="stSidebar"] {
        width: 100% !important;
        position: relative !important;
        border-right: none !important;
        border-bottom: 2px solid #ddd !important;
        margin-bottom: 1rem !important;
    }
}

/* Responsive images */
img {
    max-width: 90vw !important;
    height: auto !important;
    border-radius: 6px !important;
    margin: 10px 0 !important;
}
</style>
""", unsafe_allow_html=True)

# --- Create petals ---
petals_html = "".join([
    f'<div class="petal" style="left:{random.randint(0,100)}%; width:10px; height:10px; animation-duration:{4+i%5}s; animation-delay:{i%3}s;"></div>'
    for i in range(10)
])
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

# --- Title ---
st.markdown("<h1 style='text-align:center;'>📚 Ask Meh Anything Buddy...</h1>", unsafe_allow_html=True)

# --- Input and upload button ---
col1, col2 = st.columns([0.85, 0.15])

with col1:
    user_input = st.text_input("Ask something...", placeholder="Type your question and press Enter...", key="input_text")

with col2:
    # Hidden file uploader
    uploaded_files = st.file_uploader("", accept_multiple_files=True, type=["png", "jpg", "jpeg", "pdf", "txt"], key="file-uploader")

    # Plus sign label that triggers file uploader click
    st.markdown("""
    <label for="file-uploader" id="upload-label" title="Upload files or images">+</label>
    """, unsafe_allow_html=True)

# --- Handle uploaded files ---
if uploaded_files:
    if not isinstance(uploaded_files, list):
        uploaded_files = [uploaded_files]
    for uploaded_file in uploaded_files:
        if uploaded_file not in st.session_state.uploaded_files:
            st.session_state.uploaded_files.append(uploaded_file)

# --- Show uploaded files ---
if st.session_state.uploaded_files:
    st.markdown("### Uploaded files:")
    for f in st.session_state.uploaded_files:
        st.write(f.name)
        if f.type.startswith("image/"):
            st.image(f)

# --- When user submits question ---
if user_input:
    st.session_state.messages.append(("user", user_input))
    st.markdown(f"<div class='chat-bubble user-bubble'>{user_input}</div>", unsafe_allow_html=True)

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
            summary = f"Too many results! Try: {e.options[:5]}"
            image_url = None
        except wikipedia.exceptions.PageError:
            summary = "Sorry buddy, I couldn't find anything for that."
            image_url = None

    st.session_state.messages.append(("bot", summary))
    st.markdown(f"<div class='chat-bubble bot-bubble typewriter'>{summary}</div>", unsafe_allow_html=True)

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
for role, text in st.session_state.messages:
    if role == "user":
        st.markdown(f"<div class='chat-bubble user-bubble'>{text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble bot-bubble typewriter'>{text}</div>", unsafe_allow_html=True)

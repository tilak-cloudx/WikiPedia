import streamlit as st
import wikipedia
from gtts import gTTS
import tempfile
import base64
import time
import random

st.set_page_config(page_title="Ask Meh Anything Buddy...", page_icon="📚", layout="centered")

# Sidebar (unchanged)
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

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "music_on" not in st.session_state:
    st.session_state.music_on = False
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "last_audio_text" not in st.session_state:
    st.session_state.last_audio_text = ""

# CSS styles including hidden file uploader + big pink + label
st.markdown("""
<style>
body {
    background-color: #fdf6e3;
    background-image: url('https://www.transparenttextures.com/patterns/newsprint.png');
    color: #222;
    font-family: 'Times New Roman', serif;
}
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
.typewriter {
    overflow: hidden;
    border-right: .15em solid orange;
    white-space: nowrap;
    animation: typing 3s steps(40, end);
}
#upload-label {
    font-size: 36px;
    cursor: pointer;
    color: #ff00de;
    user-select: none;
    line-height: 1;
    padding-left: 10px;
    vertical-align: middle;
    font-weight: bold;
    transition: color 0.3s ease;
}
#upload-label:hover {
    color: #ff4eff;
}
#file-uploader {
    display: none;
}
img {
    max-width: 90vw !important;
    height: auto !important;
    border-radius: 6px !important;
    margin: 10px 0 !important;
}
@media only screen and (max-width: 600px) {
    .chat-bubble {
        max-width: 95% !important;
        font-size: 14px !important;
        padding: 8px 12px !important;
        border-radius: 12px !important;
    }
}
</style>
""", unsafe_allow_html=True)

# Petals animation
petals_html = "".join([
    f'<div class="petal" style="left:{random.randint(0,100)}%; width:10px; height:10px; animation-duration:{4+i%5}s; animation-delay:{i%3}s;"></div>'
    for i in range(10)
])
st.markdown(petals_html, unsafe_allow_html=True)

# Music toggle button
if st.button("🎶 Toggle Music"):
    st.session_state.music_on = not st.session_state.music_on

if st.session_state.music_on:
    st.markdown("""
        <audio autoplay loop>
            <source src="https://www.bensound.com/bensound-music/bensound-sunny.mp3" type="audio/mp3">
        </audio>
    """, unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align:center;'>📚 Ask Meh Anything Buddy...</h1>", unsafe_allow_html=True)

# Input and + upload button
col1, col2 = st.columns([0.85, 0.15])
with col1:
    user_input = st.text_input("Ask something...", placeholder="Type your question and press Enter...", key="input_text")

with col2:
    uploaded_files = st.file_uploader("", accept_multiple_files=True, type=["png","jpg","jpeg","pdf","txt"], key="file-uploader", label_visibility="collapsed")
    # The + sign label for hidden uploader
    st.markdown('<label for="file-uploader" id="upload-label" title="Upload files or images">+</label>', unsafe_allow_html=True)

# Handle uploaded files (store in session state)
if uploaded_files:
    if not isinstance(uploaded_files, list):
        uploaded_files = [uploaded_files]
    for f in uploaded_files:
        if f not in st.session_state.uploaded_files:
            st.session_state.uploaded_files.append(f)

# Show uploaded files names & images
if st.session_state.uploaded_files:
    st.markdown("### Uploaded files:")
    for f in st.session_state.uploaded_files:
        st.write(f.name)
        if f.type.startswith("image/"):
            st.image(f)

# When user submits input, query Wikipedia & respond
if user_input and (not st.session_state.messages or st.session_state.messages[-1][1] != user_input):
    st.session_state.messages.append(("user", user_input))
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
    st.session_state.last_audio_text = summary
    st.experimental_rerun()  # Clear input and refresh chat after submit

# Show chat messages
for role, text in st.session_state.messages:
    if role == "user":
        st.markdown(f"<div class='chat-bubble user-bubble'>{text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble bot-bubble typewriter'>{text}</div>", unsafe_allow_html=True)
        if 'image_url' in locals() and image_url:
            st.image(image_url, width=300)

# Play bot reply audio once
if st.session_state.last_audio_text:
    tts = gTTS(text=st.session_state.last_audio_text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tts.save(tmp_file.name)
        audio_bytes = open(tmp_file.name, "rb").read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        st.markdown(f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        """, unsafe_allow_html=True)
    st.session_state.last_audio_text = ""

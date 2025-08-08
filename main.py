import streamlit as st
import wikipedia
from gtts import gTTS
import tempfile
import base64

st.set_page_config(page_title="Wikipedia Chatbot", page_icon="📚", layout="centered")

# CSS-only floating emojis + cute gradient background
st.markdown("""
    <style>
    /* Pastel animated gradient background */
    body {
        background: linear-gradient(-45deg, #ffdde1, #ee9ca7, #c1c8e4, #fbc2eb, #a1c4fd);
        background-size: 400% 400%;
        animation: gradientShift 12s ease infinite;
        overflow-x: hidden;
    }
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Floating container */
    .floating-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        overflow: hidden;
        z-index: 0;
    }

    .emoji {
        position: absolute;
        bottom: -50px;
        animation: floatUp 10s linear infinite;
        opacity: 0.9;
    }

    @keyframes floatUp {
        0% { transform: translateY(0) rotate(0deg); opacity: 1; }
        100% { transform: translateY(-110vh) rotate(360deg); opacity: 0; }
    }

    /* Footer with strong white glow */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        text-align: center;
        padding: 8px;
        font-size: 14px;
        color: white;
        font-weight: bold;
        letter-spacing: 0.5px;
        text-shadow: 0px 0px 10px white, 0px 0px 14px white;
        z-index: 100;
    }
    </style>

    <!-- Floating emojis layer -->
    <div class="floating-bg">
        <div class="emoji" style="left:5%; animation-delay: 0s;">✨</div>
        <div class="emoji" style="left:20%; animation-delay: 2s; font-size:20px;">💖</div>
        <div class="emoji" style="left:35%; animation-delay: 4s;">🌸</div>
        <div class="emoji" style="left:50%; animation-delay: 1s;">💫</div>
        <div class="emoji" style="left:65%; animation-delay: 3s;">🌟</div>
        <div class="emoji" style="left:80%; animation-delay: 5s; font-size:22px;">💕</div>
        <div class="emoji" style="left:90%; animation-delay: 6s;">🦋</div>
    </div>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align:center; position: relative; z-index: 1;'>📚 Wikipedia Chatbot</h1>", unsafe_allow_html=True)

# Chat input
user_input = st.text_input(
    "Ask something...",
    key="chat_input",
    label_visibility="collapsed",
    placeholder="Type your question and press Enter..."
)

# Process query
if user_input.strip():
    try:
        summary = wikipedia.summary(user_input, sentences=2)
        st.write(f"**🤖 Bot:** {summary}")

        # Generate TTS
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

    except wikipedia.exceptions.DisambiguationError as e:
        st.error(f"Your query was too broad. Try one of these: {e.options[:5]}")
    except wikipedia.exceptions.PageError:
        st.error("Sorry, I couldn't find anything on Wikipedia for that topic.")

# Footer
st.markdown("""
    <div class="footer">
        Made with ❤️ by <b>Likhiii</b>
    </div>
""", unsafe_allow_html=True)

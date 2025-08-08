import streamlit as st
import wikipedia
from gtts import gTTS
import tempfile
import base64

st.set_page_config(page_title="Wikipedia Chatbot", page_icon="📚", layout="centered")

# CSS for mic + plus icons inside input & footer with sparkles ✨
st.markdown("""
    <style>
    .chat-input-wrapper {
        position: relative;
        width: 100%;
    }
    .chat-icons {
        position: absolute;
        right: 8px;
        top: 50%;
        transform: translateY(-50%);
        display: flex;
        gap: 6px;
    }
    .icon-btn {
        background: none;
        border: none;
        font-size: 18px;
        cursor: pointer;
        color: #555;
        padding: 4px;
    }
    .icon-btn:hover {
        color: black;
    }
    input[type="file"] {
        display: none;
    }

    /* Footer style with glow */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        text-align: center;
        padding: 8px;
        font-size: 16px;
        color: white;
        font-weight: bold;
        letter-spacing: 0.5px;
        text-shadow: 0 0 10px #ff80ab, 0 0 20px #ff80ab, 0 0 30px #ff80ab;
        animation: glow 1.5s ease-in-out infinite alternate;
        z-index: 10;
    }

    /* Glow animation */
    @keyframes glow {
        from {
            text-shadow: 0 0 5px #ff80ab, 0 0 10px #ff80ab, 0 0 15px #ff80ab;
        }
        to {
            text-shadow: 0 0 10px #ff4da6, 0 0 20px #ff4da6, 0 0 30px #ff4da6;
        }
    }

    /* Sparkle animation */
    .sparkle {
        position: fixed;
        width: 6px;
        height: 6px;
        background: white;
        border-radius: 50%;
        animation: sparkleAnim 3s linear infinite;
        opacity: 0.8;
        z-index: 5;
    }
    @keyframes sparkleAnim {
        0% { transform: translateY(0) scale(1); opacity: 0.8; }
        50% { transform: translateY(-20px) scale(1.5); opacity: 1; }
        100% { transform: translateY(0) scale(1); opacity: 0.8; }
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align:center;'>📚 Wikipedia Chatbot</h1>", unsafe_allow_html=True)

# Chat input with icons
st.markdown('<div class="chat-input-wrapper">', unsafe_allow_html=True)
user_input = st.text_input(
    "Ask something...",
    key="chat_input",
    label_visibility="collapsed",
    placeholder="Type your question and press Enter..."
)
st.markdown("""
    <div class="chat-icons">
        <button class="icon-btn" onclick="alert('🎤 Listening...')">🎤</button>
        <label for="file-upload" class="icon-btn">➕</label>
        <input id="file-upload" type="file" accept=".jpg,.jpeg,.png,.txt,.pdf">
    </div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Process input
if user_input.strip():
    try:
        summary = wikipedia.summary(user_input, sentences=2)
        st.write(f"**🤖 Bot:** {summary}")

        # Generate TTS
        tts = gTTS(text=summary, lang='en', tld='co.in')
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tts.save(tmp_file.name)

            # Auto-play audio without play button
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

# Floating sparkles
sparkles_html = "".join([
    f"<div class='sparkle' style='left:{i*5}%; top:{(i*37)%100}%; animation-delay:{i*0.3}s;'></div>"
    for i in range(15)
])
st.markdown(sparkles_html, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        ✨ Made with ❤️ by <b>Likhiii</b> ✨
    </div>
""", unsafe_allow_html=True)

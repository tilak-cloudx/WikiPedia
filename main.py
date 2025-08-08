import streamlit as st
import wikipedia
from gtts import gTTS
import tempfile
import base64

st.set_page_config(page_title="Wikipedia Chatbot", page_icon="📚", layout="centered")

# CSS for mic + plus icons, footer glow, and floating sparkles
st.markdown("""
    <style>
    /* Chat input styling */
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

    /* Footer style with white glow */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        text-align: center;
        padding: 8px;
        background-color: transparent;
        font-size: 14px;
        color: white;
        font-weight: bold;
        letter-spacing: 0.5px;
        text-shadow: 0px 0px 8px white, 0px 0px 12px white; /* Strong white glow */
        z-index: 100;
    }

    /* Sparkles container */
    .sparkle {
        position: fixed;
        bottom: -20px;
        font-size: 18px;
        animation: rise 6s linear infinite;
        opacity: 0.8;
        z-index: 0;
    }

    /* Floating animation */
    @keyframes rise {
        0% {
            transform: translateY(0) scale(1);
            opacity: 0.9;
        }
        100% {
            transform: translateY(-100vh) scale(0.8);
            opacity: 0;
        }
    }
    </style>

    <script>
    // Create sparkles dynamically
    document.addEventListener("DOMContentLoaded", function(){
        const sparkleCount = 15; // Number of sparkles
        for (let i = 0; i < sparkleCount; i++) {
            let sparkle = document.createElement("div");
            sparkle.className = "sparkle";
            sparkle.innerHTML = "✨";
            sparkle.style.left = Math.random() * 100 + "vw";
            sparkle.style.animationDuration = (4 + Math.random() * 4) + "s";
            sparkle.style.fontSize = (14 + Math.random() * 10) + "px";
            document.body.appendChild(sparkle);
        }
    });
    </script>
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

            # Auto-play audio
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

# Footer with white glow
st.markdown("""
    <div class="footer">
        Made with ❤️ by <b>Likhiii</b>
    </div>
""", unsafe_allow_html=True)

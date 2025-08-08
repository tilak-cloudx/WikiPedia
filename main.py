import streamlit as st
import wikipedia
from gtts import gTTS
import tempfile
import base64

st.set_page_config(page_title="Wikipedia Chatbot", page_icon="📚", layout="centered")

# CSS for cute animated background, sparkles, hearts, and glowing footer
st.markdown("""
    <style>
    /* Animated pastel gradient background */
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

    /* Floating emojis */
    .float-emoji {
        position: fixed;
        bottom: -20px;
        animation: floatUp linear infinite;
        opacity: 0.9;
        z-index: 0;
        pointer-events: none;
    }
    @keyframes floatUp {
        0% { transform: translateY(0) scale(1); opacity: 1; }
        100% { transform: translateY(-110vh) scale(0.8); opacity: 0; }
    }

    /* Footer with strong white glow */
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
        text-shadow: 0px 0px 10px white, 0px 0px 14px white;
        z-index: 100;
    }
    </style>

    <script>
    document.addEventListener("DOMContentLoaded", function(){
        const emojis = ["✨", "💖", "🌸", "💫", "🌟", "💕", "🦋"];
        const emojiCount = 25;

        function createEmoji(){
            let emoji = document.createElement("div");
            emoji.className = "float-emoji";
            emoji.innerHTML = emojis[Math.floor(Math.random() * emojis.length)];
            emoji.style.left = Math.random() * 100 + "vw";
            emoji.style.fontSize = (18 + Math.random() * 18) + "px";
            emoji.style.animationDuration = (5 + Math.random() * 5) + "s";
            document.body.appendChild(emoji);

            setTimeout(() => { emoji.remove(); }, 10000);
        }

        // Keep generating emojis forever
        setInterval(createEmoji, 500);
    });
    </script>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align:center;'>📚 Wikipedia Chatbot</h1>", unsafe_allow_html=True)

# Chat input with icons
st.markdown('<div class="chat-input-wrapper" style="position: relative; width: 100%;">', unsafe_allow_html=True)
user_input = st.text_input(
    "Ask something...",
    key="chat_input",
    label_visibility="collapsed",
    placeholder="Type your question and press Enter..."
)
st.markdown("""
    <div style="position: absolute; right: 8px; top: 50%; transform: translateY(-50%); display: flex; gap: 6px;">
        <button class="icon-btn" onclick="alert('🎤 Listening...')" style="background: none; border: none; font-size: 18px; cursor: pointer; color: #555; padding: 4px;">🎤</button>
        <label for="file-upload" style="background: none; border: none; font-size: 18px; cursor: pointer; color: #555; padding: 4px;">➕</label>
        <input id="file-upload" type="file" accept=".jpg,.jpeg,.png,.txt,.pdf" style="display: none;">
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

# Footer
st.markdown("""
    <div class="footer">
        Made with ❤️ by <b>Likhiii</b>
    </div>
""", unsafe_allow_html=True)

import streamlit as st
import wikipedia
from gtts import gTTS
import tempfile
import base64

st.set_page_config(page_title="Wikipedia Chatbot", page_icon="📚", layout="centered")

# 🌸 CSS styling
st.markdown("""
    <style>
    /* Input wrapper */
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
        color: #777;
        padding: 4px;
        transition: 0.3s;
    }
    .icon-btn:hover {
        color: #ff69b4;
        transform: scale(1.1);
    }
    input[type="file"] {
        display: none;
    }

    /* Bot chat bubble */
    .bot-bubble {
        background: #fce4ec;
        padding: 10px 15px;
        border-radius: 18px;
        display: inline-block;
        margin-top: 10px;
        font-size: 15px;
        animation: fadeIn 0.4s ease-in-out;
    }

    /* Fade in effect */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(5px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Footer style */
    .footer {
        position: fixed;
        bottom: 5px;
        left: 0;
        width: 100%;
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        letter-spacing: 0.5px;
        background: transparent;
        color: white;
        text-shadow: 0 0 6px rgba(255,255,255,0.8);
    }
    .footer span {
        background: linear-gradient(45deg, #ff66b2, #ffcc00, #66ffcc, #6699ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientMove 3s infinite linear;
        background-size: 300%;
    }
    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        100% { background-position: 100% 50%; }
    }

    /* Floating emojis */
    .floating-emoji {
        position: fixed;
        font-size: 20px;
        animation: floatUp 6s infinite ease-in-out;
        opacity: 0.6;
    }
    @keyframes floatUp {
        0% { transform: translateY(100vh); opacity: 0; }
        20% { opacity: 1; }
        100% { transform: translateY(-10vh); opacity: 0; }
    }
    </style>
""", unsafe_allow_html=True)

# 🎯 Title
st.markdown("<h1 style='text-align:center;'>📚 Wikipedia Chatbot</h1>", unsafe_allow_html=True)

# 💬 Chat input with icons
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

# 🤖 Process user input
if user_input.strip():
    try:
        summary = wikipedia.summary(user_input, sentences=2)
        st.markdown(f"<div class='bot-bubble'>🤖 {summary}</div>", unsafe_allow_html=True)

        # 🔊 TTS response
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

# 🌸 Floating emojis
emoji_positions = ["10%", "30%", "50%", "70%", "90%"]
for i, pos in enumerate(emoji_positions):
    st.markdown(
        f"<div class='floating-emoji' style='left:{pos}; animation-delay:{i}s;'>✨</div>",
        unsafe_allow_html=True
    )

# 💖 Footer
st.markdown("""
    <div class="footer">
        Made with ❤️ by <span>Likhiii</span>
    </div>
""", unsafe_allow_html=True)

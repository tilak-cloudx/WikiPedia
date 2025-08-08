import streamlit as st
import wikipedia
from gtts import gTTS
import tempfile
import base64

st.set_page_config(page_title="Wikipedia Chatbot", page_icon="📚", layout="centered")

# CSS for mic + plus icons inside input
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
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>📚 Wikipedia Chatbot</h1>", unsafe_allow_html=True)

# Wrap the input and icons together
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

# Process query when Enter is pressed
if user_input.strip():
    try:
        summary = wikipedia.summary(user_input, sentences=2)
        st.write(f"**🤖 Bot:** {summary}")

        # Generate female voice output
        tts = gTTS(text=summary, lang='en', tld='co.in', slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tts.save(tmp_file.name)
            audio_file = tmp_file.name

        # Encode audio to base64 for autoplay
        with open(audio_file, "rb") as f:
            audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()

        # Inject hidden autoplay audio
        st.markdown(f"""
            <audio autoplay style="display:none;">
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        """, unsafe_allow_html=True)

    except wikipedia.exceptions.DisambiguationError as e:
        st.error(f"Your query was too broad. Try one of these: {e.options[:5]}")
    except wikipedia.exceptions.PageError:
        st.error("Sorry, I couldn't find anything on Wikipedia for that topic.")

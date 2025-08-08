import streamlit as st
import wikipedia
import requests
import base64

# ------------------ CONFIG ------------------
ELEVEN_API_KEY = "sk_389dc307b469d3156f8ee173c2bc1b4a9b6be512c3a2618d"
VOICE_ID = "Xb7hH8MSUJpSbSDYk0k2"
# ---------------------------------------------

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

# Function to speak text via ElevenLabs
def speak_text(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVEN_API_KEY
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.8
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        audio_bytes = response.content
        b64 = base64.b64encode(audio_bytes).decode()
        audio_html = f"""
        <audio autoplay>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    else:
        st.error(f"❌ ElevenLabs Error {response.status_code}")
        try:
            st.write(response.json())  # show exact error
        except:
            st.write(response.text)

# If Enter is pressed and input is not empty
if user_input.strip():
    try:
        summary = wikipedia.summary(user_input, sentences=2)
        st.write(f"**🤖 Bot:** {summary}")
        speak_text(summary)  # Speak automatically
    except wikipedia.exceptions.DisambiguationError as e:
        st.error(f"Your query was too broad. Try one of these: {e.options[:5]}")
    except wikipedia.exceptions.PageError:
        st.error("Sorry, I couldn't find anything on Wikipedia for that topic.")

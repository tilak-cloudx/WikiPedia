import streamlit as st
import base64
from gtts import gTTS
import wikipedia

st.set_page_config(page_title="Wikipedia Chatbot", layout="centered")

st.title("📚 Wikipedia Chatbot")

query = st.text_input("Ask me anything:", key="input", on_change=lambda: st.session_state.submit_query())

if "messages" not in st.session_state:
    st.session_state.messages = []

def submit_query():
    query = st.session_state.input.strip()
    if query:
        try:
            answer = wikipedia.summary(query, sentences=2)
        except:
            answer = "Sorry, I couldn't find that."
        st.session_state.messages.append({"role": "user", "text": query})
        st.session_state.messages.append({"role": "bot", "text": answer})
        
        # Generate speech
        tts = gTTS(answer, lang="en", tld="co.in")
        tts.save("response.mp3")
        
        # Convert to base64
        with open("response.mp3", "rb") as f:
            audio_bytes = f.read()
        b64 = base64.b64encode(audio_bytes).decode()
        
        # Inject JS to autoplay
        st.markdown(f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """, unsafe_allow_html=True)

st.session_state.submit_query = submit_query

# Display messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**🧑 You:** {msg['text']}")
    else:
        st.markdown(f"**🤖 Bot:** {msg['text']}")

import streamlit as st
import wikipedia

# --- PAGE CONFIG ---
st.set_page_config(page_title="Wikipedia Chatbot", page_icon="📚", layout="centered")

# --- CUSTOM CSS ---
st.markdown("""
<style>
/* Center everything */
.main {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

/* Chat input */
.stTextInput > div > div > input {
    background-color: #1f2937;
    color: white;
    border-radius: 8px;
    border: 1px solid #4ade80;
}

/* Bot message style */
.bot-message {
    background-color: #1f2937;
    color: #f9fafb;
    padding: 12px 18px;
    border-radius: 15px;
    border: 1px solid #4ade80;
    box-shadow: 0 0 8px rgba(74, 222, 128, 0.4);
    font-size: 16px;
    line-height: 1.5;
    max-width: 500px;
    margin-top: 10px;
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 50px;
    font-size: 18px;
    color: white;
    font-weight: bold;
    text-shadow: 0px 0px 5px rgba(255,255,255,0.8);
}

/* Heart animation */
.heart {
    color: red;
    animation: pulse 1s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.3); }
    100% { transform: scale(1); }
}

/* Sparkles */
@keyframes sparkle {
    0% { opacity: 1; transform: translateY(0) rotate(0deg); }
    50% { opacity: 0.5; transform: translateY(-10px) rotate(45deg); }
    100% { opacity: 1; transform: translateY(0) rotate(0deg); }
}
.sparkle {
    position: fixed;
    width: 8px;
    height: 8px;
    background: gold;
    border-radius: 50%;
    animation: sparkle 2s infinite ease-in-out;
}
.sparkle:nth-child(1) { top: 20%; left: 15%; animation-delay: 0s; }
.sparkle:nth-child(2) { top: 60%; left: 80%; animation-delay: 0.5s; }
.sparkle:nth-child(3) { top: 40%; left: 50%; animation-delay: 1s; }
</style>
""", unsafe_allow_html=True)

# --- TITLE ---
st.markdown("<h1 style='text-align: center;'>📚 Wikipedia Chatbot</h1>", unsafe_allow_html=True)

# --- INPUT ---
query = st.text_input("")

# --- WIKIPEDIA SEARCH ---
if query:
    try:
        summary = wikipedia.summary(query, sentences=2)
        st.markdown(f"<div class='bot-message'>🤖 {summary}</div>", unsafe_allow_html=True)
    except:
        st.markdown("<div class='bot-message'>⚠️ Sorry, I couldn't find anything.</div>", unsafe_allow_html=True)

# --- SPARKLES ---
st.markdown("""
<div class="sparkle"></div>
<div class="sparkle"></div>
<div class="sparkle"></div>
""", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div class="footer">
    Made with <span class="heart">❤️</span> by <span style="color:#4ade80;">Likhiii</span>
</div>
""", unsafe_allow_html=True)

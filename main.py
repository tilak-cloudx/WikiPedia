import streamlit as st
import wikipedia

# --- Page Setup ---
st.set_page_config(
    page_title="Wikipedia Chatbot 🧠",
    page_icon="📚",
    layout="centered"
)

# --- Custom Font and Style ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Quicksand', sans-serif;
        }

        .message-box {
            padding: 10px 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            line-height: 1.5;
        }

        .user {
            background-color: #1e293b;
            color: #f0fdf4;
        }

        .bot {
            background-color: #334155;
            border-left: 4px solid #10b981;
            color: #e0f2f1;
        }

        .footer {
            margin-top: 50px;
            font-size: 0.8rem;
            color: #6b7280;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
    <div style='text-align: center; padding-bottom: 10px;'>
        <h1 style='font-size: 2.8rem;'>📚 Wikipedia Chatbot</h1>
        <p style='font-size: 1.1rem; color: #9ca3af;'>Your friendly fact-finder from the world's encyclopedia 🌐</p>
    </div>
""", unsafe_allow_html=True)

# --- Initialize Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Wikipedia Summary Function ---
def get_wikipedia_summary(query):
    try:
        results = wikipedia.search(query)
        if not results:
            return "😕 Sorry, I couldn't find anything on that topic."
        summary = wikipedia.summary(results[0], sentences=2, auto_suggest=False, redirect=True)
        return summary
    except wikipedia.DisambiguationError as e:
        return f"🤔 That was a bit ambiguous. Did you mean: {', '.join(e.options[:5])}?"
    except wikipedia.PageError:
        return "😢 Sorry, I couldn't find a page matching your query."
    except Exception:
        return "⚠️ Oops, something went wrong while searching Wikipedia."

# --- User Input ---
user_input = st.text_input("💬 Ask me anything... curious cat 🐱:")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    bot_response = get_wikipedia_summary(user_input)
    st.session_state.messages.append({"role": "bot", "content": bot_response})

# --- Display Chat History ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='message-box user'><strong>You:</strong> {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='message-box bot'><strong>Bot:</strong> {msg['content']}</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
    <div class='footer'>
        Made with ❤️ using <a href='https://streamlit.io' target='_blank'>Streamlit</a> and <a href='https://pypi.org/project/wikipedia/' target='_blank'>Wikipedia API</a>.
    </div>
""", unsafe_allow_html=True)

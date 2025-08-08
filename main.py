import streamlit as st

st.set_page_config(page_title="Wikipedia Chatbot", page_icon="📚", layout="centered")

# CSS for style and cuteness
st.markdown(
    """
    <style>
    .stTextInput > div {
        display: flex;
        align-items: center;
        position: relative;
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
        transform: scale(1.2);
        transition: 0.2s;
    }
    input[type="file"] {
        display: none;
    }
    .tagline {
        font-size: 14px;
        color: #888;
        text-align: center;
        margin-top: -10px;
        margin-bottom: 20px;
        font-style: italic;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Cute title
st.markdown("<h1 style='text-align:center;'>📚 Wikipedia Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p class='tagline'>✨ Made with 💖 & a sprinkle of Wikipedia magic ✨</p>", unsafe_allow_html=True)

# Input box
with st.container():
    user_input = st.text_input(
        "",
        key="chat_input",
        label_visibility="collapsed",
        placeholder="Type your question... 🦉"
    )

    # Icons with tooltips
    st.markdown(
        """
        <div class="chat-icons">
            <button class="icon-btn" title="🎤 Talk to me!">🎤</button>
            <label for="file-upload" class="icon-btn" title="➕ Add something fun!">➕</label>
            <input id="file-upload" type="file" accept=".jpg,.jpeg,.png,.txt,.pdf">
        </div>
        """,
        unsafe_allow_html=True
    )

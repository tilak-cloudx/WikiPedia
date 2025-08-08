import streamlit as st

st.set_page_config(page_title="Wikipedia Chatbot", page_icon="📚", layout="centered")

st.markdown(
    """
    <style>
    .stTextInput > div {
        display: flex;
        align-items: center;
        position: relative;
    }
    .chat-input-container {
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
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align:center;'>📚 Wikipedia Chatbot</h1>", unsafe_allow_html=True)

# Text input with icons inside
with st.container():
    user_input = st.text_input(
        "",
        key="chat_input",
        label_visibility="collapsed",
        placeholder="Type your question..."
    )

    # Inject mic and plus icons into the same input
    st.markdown(
        """
        <div class="chat-icons">
            <button class="icon-btn" onclick="alert('🎤 Listening...')">🎤</button>
            <label for="file-upload" class="icon-btn">➕</label>
            <input id="file-upload" type="file" accept=".jpg,.jpeg,.png,.txt,.pdf">
        </div>
        """,
        unsafe_allow_html=True
    )

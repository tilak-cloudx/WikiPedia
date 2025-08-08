import streamlit as st
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Wikipedia Chatbot", page_icon="📚", layout="centered")

st.markdown(
    """
    <style>
    .chat-input-row {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-top: 20px;
    }
    .chat-textbox {
        flex: 1;
    }
    .icon-btn {
        background: #2d2f38;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        font-size: 18px;
        color: white;
    }
    .icon-btn:hover {
        background: #3d3f48;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align:center;'>📚 Wikipedia Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Ask anything, talk it out 🎤, or add a file ➕ — let’s explore Wikipedia!</p>", unsafe_allow_html=True)

# --- Chat Input Row ---
st.markdown('<div class="chat-input-row">', unsafe_allow_html=True)

# Textbox (fixed: no duplicate label)
user_input = st.text_input(
    "",
    key="chat_input",
    label_visibility="collapsed",
    placeholder="Type your question...",
    help="Ask me something about Wikipedia"
)

# Mic Button
st.markdown('<div class="icon-btn" onclick="alert(\'Listening...\')">🎤</div>', unsafe_allow_html=True)

# Plus Button (hidden file uploader)
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png", "txt", "pdf"], key="file_upload", label_visibility="collapsed")
plus_icon_html = """
<script>
const uploader = window.parent.document.querySelector('input[type="file"]');
function triggerUpload(){ uploader.click(); }
</script>
<div class="icon-btn" onclick="triggerUpload()">➕</div>
"""
st.markdown(plus_icon_html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- Handle Uploaded File ---
if uploaded_file:
    st.success(f"📂 File '{uploaded_file.name}' uploaded!")
    if uploaded_file.type.startswith("image/"):
        img = Image.open(uploaded_file)
        st.image(img, caption=uploaded_file.name, use_column_width=True)
    else:
        st.write("File uploaded successfully.")

# --- Handle User Input ---
if user_input:
    st.write(f"🔍 Searching Wikipedia for: **{user_input}**")
    # Your Wikipedia API call here

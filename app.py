# =========================

# FILE : app.py
# =========================



from SRC.database import create_tables
from SRC.auth import login_user, register_user
from SRC.search_tracker import save_search
from Admin.analytics import show_analytics

create_tables()

import streamlit as st
from streamlit_option_menu import option_menu

from SRC.model import Chatbot

from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import tempfile
import subprocess

from PIL import Image
import fitz

# =========================
# CUSTOM MODULES
# =========================

from SRC.chat_history import (
    load_chat_history,
    save_chat_history
)

from SRC.translator import translate_text

from API.api_client import analyze_image

# =========================
# PAGE CONFIG
# =========================

st.set_page_config

# =========================
# LOGIN SESSION
# =========================
 
if "logged_in" not in st.session_state:
        
    st.session_state.logged_in = False

    page_title="AI College Assistant",

    page_icon="🤖",

    layout="wide"

# =========================
# PROFESSIONAL WHITE THEME
# =========================


st.markdown("""

<style>

/* =====================================================
MAIN APP
===================================================== */

.stApp {

    background-color: #F5F7FB !important;

    color: #1E293B !important;

    font-family: 'Segoe UI', sans-serif;
}

/* =====================================================
REMOVE DARK BACKGROUND
===================================================== */

html, body, [class*="css"] {

    background-color: #F5F7FB !important;

    color: #1E293B !important;
}

/* =====================================================
SIDEBAR
===================================================== */

[data-testid="stSidebar"] {

    background-color: #FFFFFF !important;

    border-right: 1px solid #E2E8F0;
}

/* Sidebar Text */

section[data-testid="stSidebar"] * {

    color: #0F172A !important;
}

/* =====================================================
HEADINGS
===================================================== */

h1, h2, h3 {

    color: #0F172A !important;

    font-weight: 700;
}

/* =====================================================
CHAT MESSAGES
===================================================== */

.stChatMessage {

    background-color: #FFFFFF !important;

    border: 1px solid #E2E8F0;

    border-radius: 18px;

    padding: 14px;

    margin-bottom: 14px;

    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
}

/* =====================================================
BUTTONS
===================================================== */

.stButton > button {

    background: linear-gradient(
        90deg,
        #2563EB,
        #3B82F6
    ) !important;

    color: white !important;

    border: none !important;

    border-radius: 12px !important;

    padding: 10px 18px !important;

    font-weight: 600 !important;
}

/* =====================================================
BUTTON HOVER
===================================================== */

.stButton > button:hover {

    transform: scale(1.02);

    background: linear-gradient(
        90deg,
        #1D4ED8,
        #2563EB
    ) !important;
}

/* =====================================================
TEXT INPUTS
===================================================== */

.stTextInput input {

    background-color: white !important;

    color: #0F172A !important;

    border-radius: 12px !important;

    border: 1px solid #CBD5E1 !important;

    padding: 12px !important;
}

/* =====================================================
CHAT INPUT
===================================================== */

[data-testid="stChatInput"] {

    background-color: white !important;

    border-radius: 15px !important;
}

/* =====================================================
FILE UPLOADER
===================================================== */

[data-testid="stFileUploader"] {

    background-color: white !important;

    border-radius: 15px !important;

    border: 1px solid #CBD5E1 !important;

    padding: 12px !important;
}

/* =====================================================
CAMERA BOX
===================================================== */

[data-testid="stCameraInput"] {

    background-color: white !important;

    border-radius: 15px !important;

    border: 1px solid #CBD5E1 !important;

    padding: 10px !important;
}

/* =====================================================
SUCCESS BOX
===================================================== */

.stSuccess {

    background-color: #DCFCE7 !important;

    color: #166534 !important;

    border-radius: 12px !important;
}

/* =====================================================
INFO BOX
===================================================== */

.stInfo {

    background-color: #DBEAFE !important;

    color: #1E40AF !important;

    border-radius: 12px !important;
}

/* =====================================================
FEATURE CARDS
===================================================== */

.element-container .stAlert {

    border-radius: 15px !important;
}

/* =====================================================
TABS
===================================================== */

.stTabs [role="tab"] {

    font-size: 17px !important;

    font-weight: 600 !important;

    color: #334155 !important;

    padding: 10px 18px !important;
}

/* =====================================================
SELECTED TAB
===================================================== */

.stTabs [aria-selected="true"] {

    background-color: #E0F2FE !important;

    border-radius: 10px !important;
}

/* =====================================================
HORIZONTAL LINE
===================================================== */

hr {

    border: 1px solid #E2E8F0 !important;
}

/* =====================================================
SCROLLBAR
===================================================== */

::-webkit-scrollbar {

    width: 10px;
}

::-webkit-scrollbar-thumb {

    background: #CBD5E1;

    border-radius: 10px;
}

/* =====================================================
REMOVE STREAMLIT HEADER
===================================================== */

#MainMenu {

    visibility: hidden;
}

footer {

    visibility: hidden;
}

header {

    visibility: hidden;
}

</style>

""", unsafe_allow_html=True)


if not st.session_state.logged_in:
 
    st.title("🔐 Login / Signup")
 
    menu = st.selectbox(
 
        "Select",
 
        ["Login", "Signup"]
 
    )
 
    username = st.text_input("Username")
 
    password = st.text_input(
        "Password",
        type="password"
    )
 
    # SIGNUP
    if menu == "Signup":
 
        if st.button("Create Account"):
 
            success = register_user(
                username,
                password
            )
 
            if success:
 
                st.success("Account Created Successfully")
 
            else:
 
                st.error("Username Already Exists")
 
    # LOGIN
    elif menu == "Login":
 
        if st.button("Login"):
 
            user = login_user(
                username,
                password
            )
 
            if user:
 
                st.session_state.logged_in = True
 
                st.session_state.username = username
 
                st.rerun()
 
            else:
 
                st.error("Invalid Credentials")
 
    st.stop()

# =========================
# LOAD CHATBOT
# =========================

bot = Chatbot("DATA/faq.csv")

# =========================
# CHAT HISTORY
# =========================

if "chat_history" not in st.session_state:

    st.session_state.chat_history = load_chat_history()

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.image("logo.png", width=120)

    st.markdown("# 🤖 AI Assistant")

    selected = option_menu(

        menu_title=None,

        options=[
"Chatbot",
"Analytics",
"Admin Portal"
],

        icons=[
            "chat-dots-fill",
            "shield-lock-fill"
        ],

        default_index=0
    )
 

    st.write("---")

    # =========================
    # LANGUAGE
    # =========================

    language = st.selectbox(

        "🌍 Select Language",

        [
            "English",
            "Hindi",
            "French",
            "Spanish",
            "German",
            "Tamil",
            "Telugu",
            "Bengali"
        ]
    )

    language_code = {

        "English": "en",
        "Hindi": "hi",
        "French": "fr",
        "Spanish": "es",
        "German": "de",
        "Tamil": "ta",
        "Telugu": "te",
        "Bengali": "bn"

    }[language]

    st.write("---")

    st.markdown("## ⚡ Features")

    st.success("🎤 Voice Assistant")
    st.success("📂 PDF Analysis")
    st.success("🖼 Image AI")
    st.success("📸 Camera AI")
    st.success("🌍 Translator")
    st.success("💬 Chat History")

    st.write("---")

    # =========================
    # CLEAR CHAT
    # =========================

    if st.button("🗑 Clear Chat"):

        st.session_state.chat_history = []

        save_chat_history([])

        st.success("Chat Cleared")

# =========================================================
# ANALYTICS PAGE
# =========================================================
 
if selected == "Analytics":
 
    show_analytics()

    
# =========================================================
# CHATBOT PAGE
# =========================================================

if selected == "Chatbot":

    # =========================
    # HEADER
    # =========================

    col1, col2 = st.columns([1, 5])

    with col1:

        st.image("logo.png", width=100)

    with col2:

        st.markdown("# 🤖 Smart AI College Assistant")

        st.markdown("""
        ### Voice + PDF + Image + Camera + Translator AI Chatbot
        """)

    st.write("")

    # =========================
    # FEATURE CARDS
    # =========================

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.info("🎤 Voice Assistant")

    with c2:
        st.info("📂 PDF Analysis")

    with c3:
        st.info("🖼 Image AI")

    with c4:
        st.info("🌍 Multi-language")

    st.write("---")

    # =========================
    # TABS
    # =========================

    tab1, tab2, tab3 = st.tabs([

        "💬 Chat",
        "📂 Upload",
        "📸 Camera"

    ])

    # =====================================================
    # CHAT TAB
    # =====================================================

    with tab1:

        st.subheader("💬 AI Conversation")

        # CHAT HISTORY

        for chat in st.session_state.chat_history:

            if chat["role"] == "user":

                with st.chat_message("user"):

                    st.write(chat["message"])

            else:

                with st.chat_message("assistant"):

                    st.write(chat["message"])

                    if "confidence" in chat:

                        st.caption(

                            f"Confidence: {chat['confidence']} | "

                            f"Level: {chat['confidence_level']} | "

                            f"Source: {chat['source']}"
                        )

        # =========================
        # VOICE INPUT
        # =========================

        st.write("### 🎤 Voice Input")

        audio = mic_recorder(

            start_prompt="🎤 Start Recording",

            stop_prompt="⏹ Stop Recording",

            just_once=True,

            use_container_width=True

        )

        if audio:

            webm_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".webm"
            )

            wav_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".wav"
            )

            with open(webm_file.name, "wb") as f:

                f.write(audio["bytes"])

            command = f'ffmpeg -i "{webm_file.name}" "{wav_file.name}" -y'

            subprocess.run(command, shell=True)

            recognizer = sr.Recognizer()

            try:

                with sr.AudioFile(wav_file.name) as source:

                    audio_data = recognizer.record(source)

                    text = recognizer.recognize_google(audio_data)

                    with st.chat_message("user"):

                        st.write(text)

                    translated_input = translate_text(
                        text,
                        "en"
                    )

                    with st.spinner("🤖 Thinking..."):

                        response = bot.get_response(
                            translated_input
                        )

                    translated_response = translate_text(

                        response["response"],
                        language_code
                    )

                    with st.chat_message("assistant"):

                        st.write(translated_response)

                        st.caption(

                            f"Confidence: {response['confidence']} | "

                            f"Level: {response['confidence_level']} | "

                            f"Source: {response['source']}"
                        )

                    # SAVE HISTORY

                    st.session_state.chat_history.append({

                        "role": "user",
                        "message": text
                    })

                    st.session_state.chat_history.append({

                        "role": "assistant",
                        "message": translated_response,
                        "confidence": response["confidence"],
                        "confidence_level": response["confidence_level"],
                        "source": response["source"]
                    })

                    save_chat_history(
                        st.session_state.chat_history
                    )

            except Exception as e:

                st.error(f"Error: {e}")

        # =========================
        # CHAT INPUT
        # =========================

        user_input = st.chat_input(
            "Type your message..."
        )

        if user_input:
 
            save_search(
 
        st.session_state.username,
 
        user_input
 
    )


    if user_input:

            with st.chat_message("user"):

                st.write(user_input)

            translated_input = translate_text(
                user_input,
                "en"
            )

            with st.spinner("🤖 Thinking..."):

                response = bot.get_response(
                    translated_input
                )

            translated_response = translate_text(

                response["response"],
                language_code
            )

            with st.chat_message("assistant"):

                st.write(translated_response)

                st.caption(

                    f"Confidence: {response['confidence']} | "

                    f"Level: {response['confidence_level']} | "

                    f"Source: {response['source']}"
                )

            # SAVE CHAT

            st.session_state.chat_history.append({

                "role": "user",
                "message": user_input
            })

            st.session_state.chat_history.append({

                "role": "assistant",
                "message": translated_response,
                "confidence": response["confidence"],
                "confidence_level": response["confidence_level"],
                "source": response["source"]
            })

            save_chat_history(
                st.session_state.chat_history
            )

    # =====================================================
    # UPLOAD TAB
    # =====================================================

    with tab2:

        st.subheader("📂 Upload PDF or Image")

        uploaded_file = st.file_uploader(

            "Upload File",

            type=[
                "png",
                "jpg",
                "jpeg",
                "pdf"
            ]
        )

        if uploaded_file is not None:

            file_type = uploaded_file.type

            # ================= IMAGE =================

            if "image" in file_type:

                image = Image.open(uploaded_file)

                st.image(
                    image,
                    use_container_width=True
                )

                image_question = st.text_input(
                    "Ask question about image"
                )

                if st.button("Analyze Image"):

                    with st.spinner(
                        "🖼 Analyzing image..."
                    ):

                        response = analyze_image(

                            image,
                            image_question
                        )

                    st.success(response)

            # ================= PDF =================

            elif "pdf" in file_type:

                pdf_text = ""

                pdf_document = fitz.open(

                    stream=uploaded_file.read(),
                    filetype="pdf"
                )

                for page in pdf_document:

                    pdf_text += page.get_text()

                st.success("✅ PDF Uploaded")

                pdf_question = st.text_input(
                    "Ask question from PDF"
                )

                if st.button("Ask PDF"):

                    full_prompt = f"""

                    PDF Content:
                    {pdf_text}

                    Question:
                    {pdf_question}

                    """

                    with st.spinner(
                        "📖 Reading PDF..."
                    ):

                        response = bot.get_response(
                            full_prompt
                        )

                    st.success(
                        response["response"]
                    )

    # =====================================================
    # CAMERA TAB
    # =====================================================

    with tab3:

        st.subheader("📸 Camera AI")

        camera_image = st.camera_input(
            "Take a picture"
        )

        if camera_image is not None:

            image = Image.open(camera_image)

            st.image(
                image,
                use_container_width=True
            )

            camera_question = st.text_input(
                "Ask question about image"
            )

            if st.button("Analyze Camera Image"):

                with st.spinner(
                    "📸 Analyzing..."
                ):

                    response = analyze_image(

                        image,
                        camera_question
                    )

                st.success(response)

# =========================================================
# ADMIN PORTAL
# =========================================================

elif selected == "Admin Portal":

    exec(open(
        "Admin/admin.py",
        encoding="utf-8"
    ).read())
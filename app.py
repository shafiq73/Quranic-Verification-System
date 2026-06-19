import streamlit as st
from streamlit_mic_recorder import mic_recorder

st.set_page_config(
    page_title="Quran Verification System",
    page_icon="📖"
)

st.title("📖 AI Quran Verification System")

st.write("Mic test for Streamlit Cloud")

audio = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="⏹ Stop Recording",
    key="recorder"
)

if audio:
    st.success("✅ Audio Recorded Successfully")

    st.audio(
        audio["bytes"],
        format="audio/wav"
    )

    st.write("Audio Size:", len(audio["bytes"]), "bytes")

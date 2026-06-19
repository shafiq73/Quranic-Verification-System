import streamlit as st
from mic_recorder import mic_recorder
from faster_whisper import WhisperModel
from diff_match_patch import diff_match_patch
import tempfile
import os

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Quran Verification System",
    page_icon="📖",
    layout="centered"
)

# -----------------------------
# QURAN TEXT
# -----------------------------
REFERENCE_TEXT = """
بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ
الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ
الرَّحْمَٰنِ الرَّحِيمِ
مَالِكِ يَوْمِ الدِّينِ
إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ
اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ
صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ
"""

# -----------------------------
# LOAD WHISPER MODEL
# -----------------------------
@st.cache_resource
def load_model():
    return WhisperModel(
        "small",
        device="cpu",
        compute_type="int8"
    )

model = load_model()

# -----------------------------
# HEADER
# -----------------------------
st.title("📖 AI Quran Verification System")

st.markdown("### 🟢 Reference Text")
st.info(REFERENCE_TEXT)

# -----------------------------
# OPTIONAL QARI AUDIO
# -----------------------------
if os.path.exists("audio/fatiha.mp3"):
    st.markdown("### 🔊 Correct Recitation")
    with open("audio/fatiha.mp3", "rb") as f:
        st.audio(f.read(), format="audio/mp3")

st.markdown("---")

# -----------------------------
# MIC RECORDER
# -----------------------------
st.subheader("🎤 Record Your Recitation")

audio = mic_recorder(
    start_prompt="🎙 Start Recording",
    stop_prompt="⏹ Stop Recording",
    key="recorder"
)

# -----------------------------
# PROCESS AUDIO
# -----------------------------
if audio:

    st.success("Audio Recorded Successfully")

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    ) as tmp:

        tmp.write(audio["bytes"])
        audio_path = tmp.name

    with st.spinner("Analyzing Recitation..."):

        segments, info = model.transcribe(
            audio_path,
            language="ar"
        )

        transcript = ""

        for segment in segments:
            transcript += segment.text + " "

    st.markdown("### 📝 Recognized Text")
    st.write(transcript)

    st.markdown("---")

    # -------------------------
    # VERIFICATION
    # -------------------------
    if transcript.strip() == REFERENCE_TEXT.strip():

        st.success(
            "🎉 MashaAllah! Recitation Matches The Reference Text."
        )

    else:

        st.error(
            "⚠️ Recitation Difference Detected"
        )

        dmp = diff_match_patch()

        diffs = dmp.diff_main(
            REFERENCE_TEXT,
            transcript
        )

        dmp.diff_cleanupSemantic(diffs)

        html_output = ""

        for op, text in diffs:

            if op == 0:

                html_output += (
                    f"<span style='font-size:22px;'>"
                    f"{text}"
                    f"</span>"
                )

            elif op == -1:

                html_output += (
                    f"<span style='background:#00aa00;"
                    f"color:white;"
                    f"font-size:22px;"
                    f"padding:3px;'>"
                    f"{text}"
                    f"</span>"
                )

            elif op == 1:

                html_output += (
                    f"<span style='background:#cc0000;"
                    f"color:white;"
                    f"font-size:22px;"
                    f"padding:3px;'>"
                    f"{text}"
                    f"</span>"
                )

        st.markdown(
            "### 🔍 Error Analysis"
        )

        st.markdown(
            html_output,
            unsafe_allow_html=True
        )

        # Play Correct Audio If Available
        if os.path.exists("audio/fatiha.mp3"):

            st.markdown(
                "### 🔊 Listen To Correct Recitation"
            )

            with open(
                "audio/fatiha.mp3",
                "rb"
            ) as f:

                st.audio(
                    f.read(),
                    format="audio/mp3"
                )

    os.remove(audio_path)

st.markdown("---")

st.caption(
    "Developed by Shafiq Ahmed | AI Quran Verification System"
)

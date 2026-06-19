import streamlit as st
from diff_match_patch import diff_match_patch
from gtts import gTTS
import io

# Page Configuration
st.set_page_config(page_title="Quranic Verification System", page_icon="📖", layout="centered")

st.title("📖 AI Quranic Verification System")
st.write("Is app mein poori Surah Al-Fatiha ki tilawat ek sath suni ja sakti hai.")

# Complete Surah Al-Fatiha Text (Ek sath jora hua taake gTTS poori surah parhay)
complete_surah_text = (
    "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ . "
    "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ . "
    "الرَّحْمَٰنِ الرَّحِيمِ . "
    "مَالِكِ يَوْمِ الدِّينِ . "
    "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ . "
    "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ . "
    "صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ"
)

# Reference Text Display
st.markdown("### 🟢 Reference Text (Poori Surah Al-Fatiha):")
st.info(complete_surah_text)

# 🔊 AI Audio Generation for the WHOLE Surah
with st.spinner("Poori Surah ki audio generate ho rahi hai..."):
    try:
        # Lang='ar' rakha hai taake Arabic accent mein parhay
        tts = gTTS(text=complete_surah_text, lang='ar', slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        
        st.markdown("### 🔊 Complete Surah Audio (Play to listen full Surah):")
        st.audio(fp, format='audio/mp3')
    except Exception as e:
        st.warning("Audio generate karne mein thoda masla aa raha hai, please page refresh karein.")

st.markdown("---")

# 🎤 AUDIO INPUT SECTION (Using Streamlit Native Audio Input)
st.subheader("🎤 Apni Tilawat Record Ya Upload Karein")
st.write("Aap mobile ya laptop ke recorder se apni aawaz record kar ke yahan file upload kar sakte hain:")

# File uploader widget
uploaded_audio = st.file_uploader("Apni voice file (.mp3, .wav, .m4a) yahan select karein:", type=["mp3", "wav", "m4a"])

if uploaded_audio is not None:
    st.audio(uploaded_audio)
    st.success("🎉 Aap ki audio file kamyabi se load ho gayi hai!")

st.markdown("---")

# Verification Engine (Simulation)
st.subheader("🔍 Verification Engine Simulation")
st.write("Galti check karne ke liye niche test text ko verify karein:")

# Default input mein thodi galti daali hai testing ke liye
default_user_text = (
    "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ . "
    "الْحَمْدُ لِلَّهِ رَبِّ الْغَفُورِينَ . "  # Galti: Al-Alameen ki jagah Al-Ghafooreen
    "الرَّحْمَٰنِ الرَّحِيمِ . "
    "مَالِكِ يَوْمِ الدُّنْيَا"  # Galti: Yawm id-Deen ki jagah Yawm id-Dunya
)

user_input_text = st.text_area("Aap ki recitation ka text input:", value=default_user_text, height=150)

# Analysis Button
if st.button("Verify Recitation"):
    u_text = user_input_text.strip()
    c_text = complete_surah_text.strip()
    
    if u_text == c_text:
        st.success("🎉 MashaAllah! Aap ki tilawat bilkul sahi hai.")
    else:
        st.error("⚠️ Recitation Error Detected!")
        
        # Text Diff Engine
        dmp = diff_match_patch()
        diffs = dmp.diff_main(c_text, u_text)
        dmp.diff_cleanupSemantic(diffs)
        
        # Generate Visual Feedback HTML
        html_output = ""
        for diff in diffs:
            if diff[0] == 0:  # Match
                html_output += f"<span style='color: #E0E0E0; font-size: 22px;'>{diff[1]} </span>"
            elif diff[0] == 1:  # User Error
                html_output += f"<span style='color: #FF4B4B; font-weight: bold; font-size: 24px; text-decoration: line-through; background-color: #331A1A; padding: 2px 5px; border-radius: 3px;'>{diff[1]}</span> "
            elif diff[0] == -1:  # What it should have been
                html_output += f"<span style='color: #00E676; font-weight: bold; font-size: 24px; background-color: #1A3322; padding: 2px 5px; border-radius: 3px;'>{diff[1]}</span> "
        
        st.markdown("### 🔍 Advanced Analytics Dashboard:")
        st.markdown(f"<div style='background-color: #111111; padding: 20px; border-radius: 8px; text-align: right; line-height: 2; border: 1px solid #333;'>{html_output}</div>", unsafe_allow_code=True)

st.markdown("---")
st.caption("Developed by Shafiq Ahmed | Data Science & AI Portfolio Project")

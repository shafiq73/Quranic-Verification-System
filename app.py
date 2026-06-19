import streamlit as st
from diff_match_patch import diff_match_patch
from gtts import gTTS
import io

# Page Configuration
st.set_page_config(page_title="Quranic Verification System", page_icon="📖", layout="centered")

st.title("📖 AI Quranic Verification System")
st.write("Is app mein audio on-the-spot generate hogi, isiliye yeh hamesha chalegi!")

# Complete Surah Al-Fatiha Dataset
surah_fatiha = {
    "Ayat 1": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
    "Ayat 2": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
    "Ayat 3": "الرَّحْمَٰنِ الرَّحِيمِ",
    "Ayat 4": "مَالِكِ يَوْمِ الدِّينِ",
    "Ayat 5": "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ",
    "Ayat 6": "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ",
    "Ayat 7": "صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ"
}

# UI: Dropdown Selection
selected_ayat = st.selectbox("Kaunsi Ayat ki tilawat check karni hai?", list(surah_fatiha.keys()))
correct_text = surah_fatiha[selected_ayat]

# Reference Text
st.markdown("### 🟢 Reference Text (Sahi Text):")
st.info(correct_text)

# 🔥 AUDIO GENERATION LOGIC: Yeh audio player hamesha samne rahega aur chalega!
try:
    tts = gTTS(text=correct_text, lang='ar', slow=False)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    
    st.markdown("### 🔊 Reference Audio:")
    st.audio(fp, format='audio/mp3')
    st.caption("Aap is play (▶️) button ko dba kar aawaz sun sakte hain.")
except Exception as e:
    st.warning("Audio generate karne mein thodi pareshani huiwi hai.")

st.markdown("---")

# Simulation Input Area
st.subheader("🎤 Recitation Input Simulation")
default_user_text = correct_text
if selected_ayat == "Ayat 2":
    default_user_text = "الْحَمْدُ لِلَّهِ رَبِّ الْغَفُورِينَ"
elif selected_ayat == "Ayat 4":
    default_user_text = "مَالِكِ يَوْمِ الدُّنْيَا"

user_input_text = st.text_input("Aap ki recitation ka text:", value=default_user_text)

# Analysis Button
if st.button("Analyze Recitation"):
    u_text = user_input_text.strip()
    c_text = correct_text.strip()
    
    if u_text == c_text:
        st.success("🎉 MashaAllah! Aap ki tilawat bilkul sahi hai.")
    else:
        st.error("⚠️ Recitation Error Detected!")
        
        # Text Diff Engine
        dmp = diff_match_patch()
        diffs = dmp.diff_main(c_text, u_text)
        dmp.diff_cleanupSemantic(diffs)
        
        # Generate Advanced Visual Feedback HTML
        html_output = ""
        for diff in diffs:
            if diff[0] == 0:  # Match
                html_output += f"<span style='color: #E0E0E0; font-size: 24px;'>{diff[1]} </span>"
            elif diff[0] == 1:  # Insertion / User Error
                html_output += f"<span style='color: #FF4B4B; font-weight: bold; font-size: 26px; text-decoration: line-through; background-color: #331A1A; padding: 2px 5px; border-radius: 3px;'>{diff[1]}</span> "
            elif diff[0] == -1:  # Deletion / What it should have been
                html_output += f"<span style='color: #00E676; font-weight: bold; font-size: 26px; background-color: #1A3322; padding: 2px 5px; border-radius: 3px;'>{diff[1]}</span> "
        
        st.markdown("### 🔍 Advanced Analytics Dashboard:")
        st.markdown(f"<div style='background-color: #111111; padding: 20px; border-radius: 8px; text-align: right; line-height: 2; border: 1px solid #333;'>{html_output}</div>", unsafe_allow_code=True)

st.markdown("---")
st.caption("Developed by Shafiq Ahmed | Data Science & AI Portfolio Project")

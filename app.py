import streamlit as st
from diff_match_patch import diff_match_patch
import os

# Page Configuration
st.set_page_config(page_title="Quranic Recitation Checker", page_icon="📖", layout="centered")

st.title("📖 Quranic Error Detection & Correction")
st.write("Apne folder mein saved audio files ke zariye tilawat check aur correct karein.")

# 1. Poori Surah Al-Fatiha ka Data aur Local File Paths
# Hum ne isme internet link ke bajaye aap ke folder ka path ('audio/ayatX.mp3') de diya hai
surah_fatiha = {
    "Ayat 1": {
        "text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
        "file_path": "audio/ayat1.mp3"
    },
    "Ayat 2": {
        "text": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
        "file_path": "audio/ayat2.mp3"
    },
    "Ayat 3": {
        "text": "الرَّحْمَٰنِ الرَّحِيمِ",
        "file_path": "audio/ayat3.mp3"
    },
    "Ayat 4": {
        "text": "مَالِكِ يَوْمِ الدِّينِ",
        "file_path": "audio/ayat4.mp3"
    },
    "Ayat 5": {
        "text": "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ",
        "file_path": "audio/ayat5.mp3"
    },
    "Ayat 6": {
        "text": "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ",
        "file_path": "audio/ayat6.mp3"
    },
    "Ayat 7": {
        "text": "صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ",
        "file_path": "audio/ayat7.mp3"
    }
}

# UI: Ayat Selector Dropdown
selected_ayat = st.selectbox("Kaunsi Ayat ki tilawat check karni hai?", list(surah_fatiha.keys()))

correct_text = surah_fatiha[selected_ayat]["text"]
local_audio_path = surah_fatiha[selected_ayat]["file_path"]

# Display Reference Text
st.markdown("### 🟢 Reference Text (Sahi Tarika):")
st.info(correct_text)

st.markdown("---")

# 2. Simulation & Testing Box
st.subheader("🎤 Simulation & Testing")
default_user_text = correct_text
if selected_ayat == "Ayat 2":
    default_user_text = "الْحَمْدُ لِلَّهِ رَبِّ الْغَفُورِينَ"  # Galti ki simulation

user_input_text = st.text_input("Aap ki tilawat ka input (Yahan galti kar ke check karein):", value=default_user_text)

# 3. Verification Logic
if st.button("Verify My Recitation"):
    
    u_text = user_input_text.strip()
    c_text = correct_text.strip()
    
    if u_text == c_text:
        st.success("🎉 MashaAllah! Aap ki tilawat bilkul sahi hai.")
    else:
        st.error("⚠️ Tilawat mein galti pakri gayi hai!")
        
        # Text Comparison
        dmp = diff_match_patch()
        diffs = dmp.diff_main(c_text, u_text)
        dmp.diff_cleanupSemantic(diffs)
        
        st.markdown("### 🔍 Correction Feedback:")
        st.write("Sahi tarika sunne ke liye niche di gayi audio ko ghaur se sunye:")
        
        # 4. Local Audio Play Karne ka Logic
        # System pehle check karega ke file folder mein maujood hai ya nahi
        if os.path.exists(local_audio_path):
            st.audio(local_audio_path, start_time=0)
            st.caption(f"🔊 Aap ke save kiye huay folder se '{local_audio_path}' play ho rahi hai.")
        else:
            st.warning(f"❌ Error: Aap ke folder mein '{local_audio_path}' file nahi mili! Meherbani kar ke file check karein.")

st.markdown("---")
# Poori Surah ki save ki hui file chalane ke liye
if st.checkbox("Poori Surah Al-Fatiha Ek Sath Sunye (Saved File)"):
    full_surah_path = "audio/full_surah.mp3"
    if os.path.exists(full_surah_path):
        st.audio(full_surah_path)
    else:
        st.warning("❌ Error: 'audio/full_surah.mp3' file folder mein nahi mili.")

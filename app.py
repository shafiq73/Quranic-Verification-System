import streamlit as st
from diff_match_patch import diff_match_patch
import os

# Page Configuration
st.set_page_config(page_title="Quranic Recitation Checker", page_icon="📖", layout="centered")

st.title("📖 Quranic Error Detection & Correction")
st.write("Surah Al-Fatiha ki ayat select karein, tilawat check karein aur correction sunein.")

# 1. Poori Surah Al-Fatiha ka Data (Ayat, Text, aur Audio Links)
# Hum ne Mishary Rashid Al-Afasy ki official high-quality audio links use kiye hain jo har ayat ke liye alag hain
surah_fatiha = {
    "Ayat 1": {
        "text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
        "audio": "https://everyayah.com/data/Alafasy_128kbps/001001.mp3"
    },
    "Ayat 2": {
        "text": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
        "audio": "https://everyayah.com/data/Alafasy_128kbps/001002.mp3"
    },
    "Ayat 3": {
        "text": "الرَّحْمَٰنِ الرَّحِيمِ",
        "audio": "https://everyayah.com/data/Alafasy_128kbps/001003.mp3"
    },
    "Ayat 4": {
        "text": "مَالِكِ يَوْمِ الدِّينِ",
        "audio": "https://everyayah.com/data/Alafasy_128kbps/001004.mp3"
    },
    "Ayat 5": {
        "text": "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ",
        "audio": "https://everyayah.com/data/Alafasy_128kbps/001005.mp3"
    },
    "Ayat 6": {
        "text": "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ",
        "audio": "https://everyayah.com/data/Alafasy_128kbps/001006.mp3"
    },
    "Ayat 7": {
        "text": "صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ",
        "audio": "https://everyayah.com/data/Alafasy_128kbps/001007.mp3"
    }
}

# 2. UI: Ayat Selector Dropdown
selected_ayat = st.selectbox("Kaunsi Ayat ki tilawat check karni hai?", list(surah_fatiha.keys()))

# Sahi text aur audio ko nikalna selection ke mutabiq
correct_text = surah_fatiha[selected_ayat]["text"]
sahi_audio_url = surah_fatiha[selected_ayat]["audio"]

# Display Reference Text
st.markdown("### 🟢 Reference Text (Sahi Tarika):")
st.info(correct_text)

st.markdown("---")

# 3. User Input & Simulation Section
st.subheader("🎤 Simulation & Testing")
st.write("Real app mein yahan mic ka model lagta hai. Abhi testing ke liye niche diye gaye box mein Arabic text likhein.")

# Default fake user text banana testing ke liye taake galti detect ho sake
default_user_text = correct_text
if selected_ayat == "Ayat 2":
    default_user_text = "الْحَمْدُ لِلَّهِ رَبِّ الْغَفُورِينَ" # 'العالمين' ki jagah galti ki
elif selected_ayat == "Ayat 4":
    default_user_text = "مَالِكِ يَوْمِ الدُّنْيَا" # 'الدين' ki jagah galti ki

user_input_text = st.text_input("Aap ki tilawat ka input (Yahan galti kar ke check karein):", value=default_user_text)

# 4. Core Analytics: Verification Logic
if st.button("Verify My Recitation"):
    
    # Dono texts ko clean karna taake extra spaces ka masla na ho
    u_text = user_input_text.strip()
    c_text = correct_text.strip()
    
    if u_text == c_text:
        st.success("🎉 MashaAllah! Aap ki tilawat bilkul sahi hai.")
    else:
        st.error("⚠️ Tilawat mein galti pakri gayi hai!")
        
        # Text Comparison Tool
        dmp = diff_match_patch()
        diffs = dmp.diff_main(c_text, u_text)
        dmp.diff_cleanupSemantic(diffs)
        
        # Galti ko highlight karne ka tareeqa
        st.markdown("### 🔍 Correction Feedback:")
        st.write("Sahi tarika sunne ke liye niche di gayi audio ko ghaur se sunye:")
        
        # Auto-play correct audio for that specific Ayat
        st.audio(sahi_audio_url, start_time=0)
        st.caption(f"🔊 {selected_ayat} ki sahi tilawat (Qari Mishary Rashid Al-Afasi)")

st.markdown("---")
# Poori Surah ek sath sunne ke liye ek bonus button
if st.checkbox("Poori Surah Al-Fatiha Ek Sath Sunye"):
    st.audio("https://download.quranicaudio.com/quran/mishaari_raashid_al_afasi/001.mp3")

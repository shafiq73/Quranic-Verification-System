import streamlit as st
from diff_match_patch import diff_match_patch

# Page Configuration
st.set_page_config(page_title="Quranic Recitation Checker", page_icon="📖", layout="centered")

st.title("📖 Quranic Error Detection & Correction")
st.write("Is app mein audio direct Quran.com ke server se play hogi.")

# Poori Surah Al-Fatiha ka Data (Quran.com High-Quality Audio Links)
surah_fatiha = {
    "Ayat 1": {
        "text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
        "audio_url": "https://audio.qurancdn.com/reciters/7/001001.mp3"
    },
    "Ayat 2": {
        "text": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
        "audio_url": "https://audio.qurancdn.com/reciters/7/001002.mp3"
    },
    "Ayat 3": {
        "text": "الرَّحْمَٰنِ الرَّحِيمِ",
        "audio_url": "https://audio.qurancdn.com/reciters/7/001003.mp3"
    },
    "Ayat 4": {
        "text": "مَالِكِ يَوْمِ الدِّينِ",
        "audio_url": "https://audio.qurancdn.com/reciters/7/001004.mp3"
    },
    "Ayat 5": {
        "text": "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ",
        "audio_url": "https://audio.qurancdn.com/reciters/7/001005.mp3"
    },
    "Ayat 6": {
        "text": "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ",
        "audio_url": "https://audio.qurancdn.com/reciters/7/001006.mp3"
    },
    "Ayat 7": {
        "text": "صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ",
        "audio_url": "https://audio.qurancdn.com/reciters/7/001007.mp3"
    }
}

# UI: Dropdown
selected_ayat = st.selectbox("Kaunsi Ayat ki tilawat check karni hai?", list(surah_fatiha.keys()))

correct_text = surah_fatiha[selected_ayat]["text"]
audio_link = surah_fatiha[selected_ayat]["audio_url"]

st.markdown("### 🟢 Reference Text (Sahi Tarika):")
st.info(correct_text)

st.markdown("---")

# Simulation Input
st.subheader("🎤 Simulation & Testing")
default_user_text = correct_text
if selected_ayat == "Ayat 2":
    default_user_text = "الْحَمْدُ لِلَّهِ رَبِّ الْغَفُورِينَ"

user_input_text = st.text_input("Aap ki tilawat ka input (Yahan galti kar ke check karein):", value=default_user_text)

# Verification Logic
if st.button("Verify My Recitation"):
    u_text = user_input_text.strip()
    c_text = correct_text.strip()
    
    if u_text == c_text:
        st.success("🎉 MashaAllah! Aap ki tilawat bilkul sahi hai.")
    else:
        st.error("⚠️ Tilawat mein galti pakri gayi hai!")
        dmp = diff_match_patch()
        diffs = dmp.diff_main(c_text, u_text)
        dmp.diff_cleanupSemantic(diffs)
        
        st.markdown("### 🔍 Correction Feedback:")
        st.write("Sahi tarika sunne ke liye niche di gayi audio ko ghaur se sunye:")
        st.audio(audio_link, start_time=0)

st.markdown("---")
if st.checkbox("Poori Surah Al-Fatiha Ek Sath Sunye"):
    st.audio("https://audio.qurancdn.com/reciters/7/high.mp3")

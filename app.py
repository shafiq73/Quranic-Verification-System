import streamlit as st
from diff_match_patch import diff_match_patch

# Page Configuration
st.set_page_config(page_title="Quranic Recitation Checker", page_icon="📖", layout="centered")

st.title("📖 Quranic Error Detection & Correction")
st.write("Is app mein aap ko koi audio file download nahi karni paregi. Yeh internet se khud hi sahi tilawat chalayegi.")

# Poori Surah Al-Fatiha ka Data (Internet links ke sath)
surah_fatiha = {
    "Ayat 1": {
        "text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
        "audio_url": "https://everyayah.com/data/Alafasy_128kbps/001001.mp3"
    },
    "Ayat 2": {
        "text": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
        "audio_url": "https://everyayah.com/data/Alafasy_128kbps/001002.mp3"
    },
    "Ayat 3": {
        "text": "الرَّحْمَٰنِ الرَّحِيمِ",
        "audio_url": "https://everyayah.com/data/Alafasy_128kbps/001003.mp3"
    },
    "Ayat 4": {
        "text": "مَالِكِ يَوْمِ الدِّينِ",
        "audio_url": "https://everyayah.com/data/Alafasy_128kbps/001004.mp3"
    },
    "Ayat 5": {
        "text": "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ",
        "audio_url": "https://everyayah.com/data/Alafasy_128kbps/001005.mp3"
    },
    "Ayat 6": {
        "text": "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ",
        "audio_url": "https://everyayah.com/data/Alafasy_128kbps/001006.mp3"
    },
    "Ayat 7": {
        "text": "صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ",
        "audio_url": "https://everyayah.com/data/Alafasy_128kbps/001007.mp3"
    }
}

# UI: Ayat Selector Dropdown
selected_ayat = st.selectbox("Kaunsi Ayat ki tilawat check karni hai?", list(surah_fatiha.keys()))

correct_text = surah_fatiha[selected_ayat]["text"]
audio_link = surah_fatiha[selected_ayat]["audio_url"]

# Display Reference Text
st.markdown("### 🟢 Reference Text (Sahi Tarika):")
st.info(correct_text)

st.markdown("---")

# Simulation & Testing Box
st.subheader("🎤 Simulation & Testing")
default_user_text = correct_text
if selected_ayat == "Ayat 2":
    default_user_text = "الْحَمْدُ لِلَّهِ رَبِّ الْغَفُورِينَ"  # Galti ki simulation ki hui hai

user_input_text = st.text_input("Aap ki tilawat ka input (Yahan galti kar ke check karein):", value=default_user_text)

# Verification Logic
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
        
        # Internet se direct audio play hogi, koi local file nahi chahiye
        st.audio(audio_link, start_time=0)
        st.caption(f"🔊 Internet se Qari Mishary Rashid Al-Afasi ki aawaz mein {selected_ayat} play ho rahi hai.")

st.markdown("---")
# Poori Surah ek sath sunne ke liye ek bonus button
if st.checkbox("Poori Surah Al-Fatiha Ek Sath Sunye"):
    st.audio("https://download.quranicaudio.com/quran/mishaari_raashid_al_afasi/001.mp3")

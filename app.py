import streamlit as st
from diff_match_patch import diff_match_patch

# Page Configuration
st.set_page_config(page_title="Quranic Recitation Checker", page_icon="📖", layout="centered")

st.title("📖 Quranic Error Detection & Correction")
st.write("Is app mein galti hone par sahi tilawat ka text aur audio aap ke samne highlight ho jayegi.")

# Surah Al-Fatiha Data
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

# Reference Text (Sahi Tarika)
st.markdown("### 🟢 Reference Text (Sahi Tarika):")
st.info(correct_text)

# Reference Audio Jo Hamesha Visible Hogi
st.markdown("### 🔊 Saved Reference Audio:")
st.audio(audio_link, start_time=0)
st.caption("Aap is play button par click kar ke saved audio kisi bhi waqt sun sakte hain.")

st.markdown("---")

# Simulation Input
st.subheader("🎤 Simulation & Testing")
default_user_text = correct_text
if selected_ayat == "Ayat 2":
    default_user_text = "الْحَمْدُ لِلَّهِ رَبِّ الْغَفُورِينَ"  # Galti ki hui hai testing ke liye
elif selected_ayat == "Ayat 4":
    default_user_text = "مَالِكِ يَوْمِ الدُّنْيَا"

user_input_text = st.text_input("Aap ki tilawat ka input:", value=default_user_text)

# Verification Button Logic
if st.button("Verify My Recitation"):
    u_text = user_input_text.strip()
    c_text = correct_text.strip()
    
    if u_text == c_text:
        st.success("🎉 MashaAllah! Aap ki tilawat bilkul sahi hai.")
    else:
        st.error("⚠️ Tilawat mein galti pakri gayi hai!")
        
        # Text Match logic aur HTML Formatting Lal (Red) color ke liye
        dmp = diff_match_patch()
        diffs = dmp.diff_main(c_text, u_text)
        dmp.diff_cleanupSemantic(diffs)
        
        # HTML Text Banana galti highlight karne ke liye
        html_output = ""
        for diff in diffs:
            if diff[0] == 0:  # Sahi word
                html_output += f"<span style='color: white; font-size: 24px;'>{diff[1]} </span>"
            elif diff[0] == 1:  # Galt word jo user ne parha/likha
                html_output += f"<span style='color: #ff4b4b; font-weight: bold; font-size: 28px; text-decoration: underline;'>{diff[1]}</span> "
        
        # UI par Lal text show karna
        st.markdown("### 🔍 Aap Ki Galti (Highlighted in Red):")
        st.markdown(f"<div style='background-color: #1e1e1e; padding: 15px; border-radius: 5px; text-align: right;'>{html_output}</div>", unsafe_allow_code=True)
        
        # Correction Audio section ko alag se samne lana
        st.markdown("### 🎯 Sahi Correction Audio:")
        st.write("Browser policy ki wajah se auto-play block ho sakti hai. Meherbani kar ke niche diye gaye player ka **Play (▶️)** button dabayein aur sahi tilawat sunein:")
        st.audio(audio_link)

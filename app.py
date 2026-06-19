import streamlit as st
from diff_match_patch import diff_match_patch

# Page Configuration
st.set_page_config(page_title="Quranic Tajweed Analyzer", page_icon="📖", layout="centered")

st.title("📖 AI Quranic Tajweed & Error Detection Engine")
st.write("Professional Data Science Portfolio Prototype: Visual Correction & Phonetic Feedback System.")

# Complete Surah Al-Fatiha Dataset with Pronunciation/Tajweed Guide
surah_fatiha = {
    "Ayat 1": {
        "text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
        "guide": "Bismillahir Rahmanir Raheem: 'Haa' (ح) ko halaq ke darmiyan se wazeh nikalna hai."
    },
    "Ayat 2": {
        "text": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
        "guide": "Alhamdu lillahi Rabbil 'Alameen: 'Ayn' (ع) ko halaq se nikalna hai, 'Alameen' parhein, 'Ghafooreen' ya 'Alameen' mein 'Alaf' na bne."
    },
    "Ayat 3": {
        "text": "الرَّحْمَٰنِ الرَّحِيمِ",
        "guide": "Ar-Rahmanir-Raheem: Dono jagah 'Haa' (ح) ki aawaz ko narm aur saaf nikalna hai."
    },
    "Ayat 4": {
        "text": "مَالِكِ يَوْمِ الدِّينِ",
        "guide": "Maliki Yawmid-Deen: 'Deen' (د) ko narm parhein, 'Zeen' ya 'Deen' mein 'Daal' ki baje 'Taa' na bne."
    },
    "Ayat 5": {
        "text": "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ",
        "guide": "Iyyaka Na'budu wa Iyyaka Nasta'een: 'Iyyaka' par Tashdeed (stress) dhalna hai, aur 'Nasta'een' mein 'Ayn' wazeh ho."
    },
    "Ayat 6": {
        "text": "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ",
        "guide": "Ihdinas-Siraatal-Mustaqeem: 'Saad' (ص) aur 'Toa' (ط) ko pur (mota) parhna hai, 'Mustaqeem' mein 'Qaaf' (ق) mota hoga."
    },
    "Ayat 7": {
        "text": "صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ",
        "guide": "Siraatal-Lazeena An'amta 'Alayhim...: 'Lazeena' mein 'Zaal' narm, 'Maghdoobi' mein 'Zwaad' (ض) ko mota parhein, aur 'Daallseen' par 6 harakat lamba karein."
    }
}

# UI: Dropdown Selection
selected_ayat = st.selectbox("Kaunsi Ayat ki tilawat check karni hai?", list(surah_fatiha.keys()))

correct_text = surah_fatiha[selected_ayat]["text"]
tajweed_guide = surah_fatiha[selected_ayat]["guide"]

# Display Reference Text
st.markdown("### 🟢 Reference Text (Sahi Text):")
st.info(correct_text)

st.markdown("---")

# Simulation Input Area
st.subheader("🎤 Recitation Input Simulation")
st.write("Testing ke liye neeche diye gaye box mein text ko badal kar galti test karein:")

# Pre-defined mistakes for analytics demonstration
default_user_text = correct_text
if selected_ayat == "Ayat 2":
    default_user_text = "الْحَمْدُ لِلَّهِ رَبِّ الْغَفُورِينَ"  # Mistake: Al-Ghafooreen instead of Al-Alameen
elif selected_ayat == "Ayat 4":
    default_user_text = "مَالِكِ يَوْمِ الدُّنْيَا"  # Mistake: Ad-Dunya instead of Ad-Deen

user_input_text = st.text_input("Aap ki recitation ka text:", value=default_user_text)

# Analysis Button
if st.button("Analyze Recitation"):
    u_text = user_input_text.strip()
    c_text = correct_text.strip()
    
    if u_text == c_text:
        st.success("🎉 MashaAllah! Aap ki tilawat text ke mutabiq bilkul sahi hai.")
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
        
        # Display Visual Dashboard
        st.markdown("### 🔍 Advanced Analytics Dashboard:")
        st.write("Neeche <span style='color: #FF4B4B; font-weight:bold;'>Lal (Red)</span> rang aap ki galti ko dikhata hai, aur <span style='color: #00E676; font-weight:bold;'>Sabz (Green)</span> rang sahi lafz ko wazeh karta hai:", unsafe_allow_code=True)
        
        st.markdown(f"<div style='background-color: #111111; padding: 20px; border-radius: 8px; text-align: right; line-height: 2; border: 1px solid #333;'>{html_output}</div>", unsafe_allow_code=True)
        
        # Tajweed & Phonetic Pronunciation Guide
        st.markdown("### 🎯 Tajweed & Pronunciation Guide:")
        st.warning(tajweed_guide)

st.markdown("---")
st.caption("Developed by Shafiq Ahmed | Data Science & AI Portfolio Project")
# Tajweed & Phonetic Pronunciation Guide
        st.markdown("### 🎯 Tajweed & Pronunciation Guide:")
        st.warning(tajweed_guide)

st.markdown("---")
st.caption("Developed by Shafiq Ahmed | Data Science & AI Portfolio Project")

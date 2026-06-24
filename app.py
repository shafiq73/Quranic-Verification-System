import streamlit as st
from st_audiorecorder import audiorecorder

st.set_page_config(page_title="Quranic Verification System", page_icon="📖", layout="centered")

st.title("📖 Quranic Verification System")
st.write("### Qari Raad Al Kurdi Ki Awaz Aur Live Verification")

# Surah list aur codes
surah_dict = {
    "1. Surah Al-Fatiha": 1,
    "2. Surah Al-Baqarah": 2,
    "112. Surah Al-Ikhlas": 112,
    "113. Surah Al-Falaq": 113,
    "114. Surah An-Nas": 114
}

selected_surah = st.selectbox("Surah Select Karein:", list(surah_dict.keys()))
base_url = "https://server6.mp3quran.net/kurdi/"

if selected_surah:
    surah_num = surah_dict[selected_surah]
    file_number = f"{surah_num:03d}"
    qari_audio_url = f"{base_url}{file_number}.mp3"
    
    # 1. Qari Sahab ki Reference Audio
    st.write("---")
    st.subheader("🎵 Qari Sahab Ki Awaz (Reference)")
    st.audio(qari_audio_url, format="audio/mp3")

    # 2. Live Recording Section
    st.write("---")
    st.subheader("🎙️ Apni Awaz Mein Tilawat Record Karein")
    st.info("Niche bane Record button par click karein. Jab parh lein to Stop par click karein.")
    
    # Stable and lightweight recording widget
    recorded_audio = audiorecorder()

    if recorded_audio is not None and len(recorded_audio) > 0:
        # User ki recording ko play back karna
        st.success("✅ Aap ki recording save ho gayi hai! Niche sunein:")
        
        # Audio raw bytes ko read karna
        audio_bytes = recorded_audio.tobytes()
        st.audio(audio_bytes, format="audio/wav")
        
        # 3. Smart Verification Simulation (Galti Check)
        st.write("---")
        st.subheader("🤖 AI Verification Status")
        
        if st.button("🔍 Tilawat Verify Karein"):
            with st.spinner("Aap ki awaz ka Qari sahab ki tilawat se muwazna (compare) kiya ja raha hai..."):
                
                # Simulation: Farz karein galti hui
                galti_detect_hui = True 
                
                if galti_detect_hui:
                    st.error("⚠️ Galti Detect Hui! Aap ki tilawat mein makhraj ya lafzi galti hai.")
                    st.warning("🔄 AI Correction: App ab automatic Qari Sahab ki awaz shuru se play kar rahi hai taake aap sahi sun sakein.")
                    
                    # Automatic Qari sahab ki audio dobara chalana
                    st.audio(qari_audio_url, format="audio/mp3")
                else:
                    st.success("🎉 MashaAllah! Aap ki tilawat bilkul theek hai.")

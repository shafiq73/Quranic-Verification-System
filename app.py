import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Quranic Verification System", page_icon="📖", layout="centered")

st.title("📖 Quranic Verification System (Live Fix)")
st.write("### Real-Time Automatic Correction")

# OpenAI Client Setup
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error("⚠️ Secrets mein OPENAI_API_KEY check karein.")

# Surah aur sahi text ka data
quran_data = {
    "1. Surah Al-Fatiha": {
        "num": 1,
        "correct_text": "الحمد لله رب العالمين"
    },
    "112. Surah Al-Ikhlas": {
        "num": 112,
        "correct_text": "قل هو الله أحد"
    }
}

selected_surah = st.selectbox("Surah Select Karein:", list(quran_data.keys()))
base_url = "https://server6.mp3quran.net/kurdi/"

if selected_surah:
    surah_info = quran_data[selected_surah]
    file_number = f"{surah_info['num']:03d}"
    qari_audio_url = f"{base_url}{file_number}.mp3"
    
    st.write("---")
    st.subheader("🎵 Qari Sahab Ki Awaz (Reference)")
    st.audio(qari_audio_url, format="audio/mp3")

    st.write("---")
    st.subheader("🎙️ Apni Awaz Mein Tilawat Karein")
    
    # Live Microphone Input
    recorded_file = st.audio_input("Record karein, rokte hi automatic check hoga:")

    # Jaise hi user recording stop karega, yeh niche wala code KHUD chal parega (bina button ke)
    if recorded_file is not None:
        with st.spinner("AI live check kar raha hai..."):
            try:
                # Whisper AI se text lena
                transcription = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=recorded_file,
                    language="ar"
                )
                
                user_text = transcription.text.strip()
                sahi_text = surah_info["correct_text"]
                
                # 🛠️ Makhraj ki galti khatam karne ke liye narm checking (Clean Text)
                # Hum i'raab (zer, zabar, pesh) aur extra spaces ko ignore kar rahe hain
                def clean_arabic(text):
                    # Khali spaces aur aam tabdeeli ko saaf karna
                    return "".join([c for c in text if c not in ["\u064b", "\u064c", "\u064d", "\u064e", "\u0650", "\u064f", "\u0651", "\u0652", " "]])

                st.write(f"🗣️ **Aap ne parha:** {user_text}")
                
                # Agar saaf karne ke baad bhi lafz bilkul farq hain (Galat Lafz)
                if clean_arabic(user_text) != clean_arabic(sahi_text):
                    st.error("⚠️ Lafzi Galti Detect Hui!")
                    st.warning("🔄 Automatic Correction: Qari Sahab ki awaz suniye:")
                    
                    # Live user ke rokte hi Qari sahab ki audio automatic chal paregi
                    st.audio(qari_audio_url, format="audio/mp3", autoplay=True)
                else:
                    st.success("🎉 MashaAllah! Aap ki tilawat bilkul theek hai.")
                    
            except Exception as e:
                st.error(f"Error: {e}")

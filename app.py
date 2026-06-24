import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import io

st.set_page_config(page_title="Quranic Verification System", page_icon="📖", layout="centered")

st.title("📖 Quranic Verification System (Free AI)")
st.write("### Real-Time Automatic Correction (No API Key Needed)")

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
    
    recorded_file = st.audio_input("Record karein, rokte hi automatic check hoga:")

    if recorded_file is not None:
        with st.spinner("Free AI live check kar raha hai..."):
            try:
                # Audio file ko WAV format mein convert karna jo Google AI samajhta hai
                audio_bytes = recorded_file.read()
                audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
                wav_io = io.BytesIO()
                audio_segment.export(wav_io, format="wav")
                wav_io.seek(0)
                
                # Google Speech Recognition Setup
                recognizer = sr.Recognizer()
                with sr.AudioFile(wav_io) as source:
                    audio_data = recognizer.record(source)
                    # Arabic language select ki hai
                    user_text = recognizer.recognize_google(audio_data, language="ar-AE")
                
                sahi_text = surah_info["correct_text"]
                
                # Makhraj filter logic
                def clean_arabic(text):
                    return "".join([c for c in text if c not in ["\u064b", "\u064c", "\u064d", "\u064e", "\u0650", "\u064f", "\u0651", "\u0652", " "]])

                st.write(f"🗣️ **Aap ne parha:** {user_text}")
                
                if clean_arabic(user_text) != clean_arabic(sahi_text):
                    st.error("⚠️ Lafzi Galti Detect Hui!")
                    st.warning("🔄 Automatic Correction: Qari Sahab ki awaz suniye:")
                    st.audio(qari_audio_url, format="audio/mp3", autoplay=True)
                else:
                    st.success("🎉 MashaAllah! Aap ki tilawat bilkul theek hai.")
                    
            except sr.UnknownValueError:
                st.error("⚠️ AI aap ki awaz samajh nahi saka. Koshish karein ke mic ke kareeb ho kar saaf parhein.")
            except Exception as e:
                st.error(f"Error: {e}")

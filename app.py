import streamlit as st
import speech_recognition as sr
import io

st.set_page_config(page_title="Quranic Verification System", page_icon="📖", layout="centered")

st.title("📖 Quranic Verification System (Free AI)")
st.write("### Real-Time Automatic Correction (No Error Setup)")

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
    recorded_file = st.audio_input("Record karne ke liye mic icon par click karein:")

    if recorded_file is not None:
        with st.spinner("Free AI live check kar raha hai..."):
            try:
                # Direct file bytes ko read karna (No ffmpeg/ffprobe required)
                audio_bytes = recorded_file.read()
                
                # Speech Recognition ko direct audio stream dena
                recognizer = sr.Recognizer()
                with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
                    audio_data = recognizer.record(source)
                    # Google Free Arabic recognition engine use karna
                    user_text = recognizer.recognize_google(audio_data, language="ar-AE")
                
                sahi_text = surah_info["correct_text"]
                
                # Makhraj/Zabar-Zer filter logic
                def clean_arabic(text):
                    return "".join([c for c in text if c not in ["\u064b", "\u064c", "\u064d", "\u064e", "\u0650", "\u064f", "\u0651", "\u0652", " "]])

                st.write(f"🗣️ **Aap ne parha:** {user_text}")
                
                # Comparison logic
                if clean_arabic(user_text) != clean_arabic(sahi_text):
                    st.error("⚠️ Lafzi Galti Detect Hui!")
                    st.warning("🔄 Automatic Correction: Qari Sahab ki awaz suniye:")
                    # User ke rokte hi Qari sahab ki audio autoplay ho jayegi
                    st.audio(qari_audio_url, format="audio/mp3", autoplay=True)
                else:
                    st.success("🎉 MashaAllah! Aap ki tilawat bilkul theek hai. Koi lafzi galti nahi mili.")
                    
            except sr.UnknownValueError:
                st.error("⚠️ AI aap ki awaz thik se samajh nahi saka. Koshish karein ke mic ke thora kareeb ho kar saaf parhein.")
            except Exception as e:
                st.error(f"Error: {e}")

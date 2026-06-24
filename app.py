import streamlit as st
import speech_recognition as sr
import io

st.set_page_config(page_title="Quranic Real-Time Verification", page_icon="📖", layout="centered")

st.title("📖 Quranic Automatic Word-Correction")
st.write("### 🎙️ Surah Al-Fatiha Live Word-Targeted Correction")

# Surah Al-Fatiha ke shuruati alfaz aur un ke exact audio timestamps (seconds mein)
# Taake galti hote hi Qari sahab theek usi second se parhna shuru karein
fatiha_words = [
    {"word": "الحمد", "start_time": 0, "end_time": 2},
    {"word": "لله", "start_time": 2, "end_time": 3},
    {"word": "رب", "start_time": 3, "end_time": 4},
    {"word": "العالمين", "start_time": 4, "end_time": 7},
    {"word": "الرحمن", "start_time": 7, "end_time": 9},
    {"word": "الرحيم", "start_time": 9, "end_time": 12},
    {"word": "مالك", "start_time": 12, "end_time": 14},
    {"word": "يوم", "start_time": 14, "end_time": 15},
    {"word": "الدين", "start_time": 15, "end_time": 18}
]

correct_full_text = "الحمد لله رب العالمين الرحمن الرحيم مالك يوم الدين"
qari_audio_url = "https://server6.mp3quran.net/kurdi/001.mp3"

st.subheader("📖 Target: Surah Al-Fatiha (Ayat 1-4)")
st.info(f"Sahi Text: **{correct_full_text}**")

# Arabi alfaz ko saaf karne ka function (Makhraj ki sakhti khatam karne ke liye)
def clean_word(w):
    return "".join([c for c in w if c not in ["\u064b", "\u064c", "\u064d", "\u064e", "\u0650", "\u064f", "\u0651", "\u0652", " "]])

st.write("---")
st.write("### 🛠️ Apni Tilawat Test Karein")
recorded_file = st.audio_input("Mic daba kar parhein (Galti check karne ke liye koi lafz badal kar dekhain):")

if recorded_file is not None:
    audio_bytes = recorded_file.read()
    recognizer = sr.Recognizer()
    
    with st.spinner("AI Surah Al-Fatiha ke lafzoon ka muwazna kar raha hai..."):
        try:
            with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
                audio_data = recognizer.record(source)
                user_text = recognizer.recognize_google(audio_data, language="ar-AE")
            
            st.write(f"🗣️ **Aap ne parha:** {user_text}")
            
            user_words = user_text.split()
            galti_mili = False
            galti_wala_lafz = ""
            jump_to_seconds = 0
            
            # Word-by-Word checking logic
            for i, target in enumerate(fatiha_words):
                cleaned_target = clean_word(target["word"])
                
                # Agar user ne lafz chora ya galat parha
                if i >= len(user_words) or clean_word(user_words[i]) != cleaned_target:
                    galti_mili = True
                    galti_wala_lafz = user_words[i] if i < len(user_words) else "Lafz Chora"
                    jump_to_seconds = target["start_time"] # Exact second jahan galti hui
                    break
            
            if galti_mili:
                st.error(f"⚠️ Lafzi Galti Detect Hui! Aap ki tilawat yahan galat hui: '{galti_wala_lafz}'")
                st.warning(f"🔄 Automatic Correction: Qari Raad Al Kurdi exact **{jump_to_seconds} seconds** se parhna shuru kar rahe hain:")
                
                # Qari Sahab ki audio exact timestamp par autoplay hogi
                st.audio(qari_audio_url, format="audio/mp3", start_time=jump_to_seconds, autoplay=True)
            else:
                st.success("🎉 MashaAllah! Aap ke parhe gaye saare alfaz bilkul darust hain. Qari sahab khamosh hain!")
                
        except sr.UnknownValueError:
            st.error("⚠️ AI awaz saaf nahi sun saka, thora mic ke kareeb ho kar dobara parhein.")
        except Exception as e:
            st.error(f"System Error: {e}")

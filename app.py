import streamlit as st
import speech_recognition as sr
import io

st.set_page_config(page_title="Quranic Real-Time Verification", page_icon="📖", layout="centered")

st.title("📖 Quranic Automatic Word-Correction")
st.write("### 🎙️ Lafzi Galti Par Qari Sahab Ka Auto-Start System")

# Surah Al-Ikhlas ke har lafz ka exact sahi text aur us ka audio timing (seconds mein)
# Taake Qari sahab sirf galti wale lafz se hi bolna shuru karein
ikhlas_words = [
    {"word": "قل", "start_time": 0, "end_time": 1},
    {"word": "هو", "start_time": 1, "end_time": 2},
    {"word": "الله", "start_time": 2, "end_time": 4},
    {"word": "أحد", "start_time": 4, "end_time": 6}
]

correct_full_text = "قل هو الله أحد"
qari_audio_url = "https://server6.mp3quran.net/kurdi/112.mp3"

st.subheader("📖 Target Verses: Surah Al-Ikhlas")
st.info(f"Sahi Lafz: **{correct_full_text}**")

# Clean Arabic function to ignore basic spaces/diacritics
def clean_word(w):
    return "".join([c for c in w if c not in ["\u064b", "\u064c", "\u064d", "\u064e", "\u0650", "\u064f", "\u0651", "\u0652", " "]])

st.write("---")
st.write("### 🛠️ Step 1: Apni Tilawat Test Karein")
recorded_file = st.audio_input("Mic daba kar parhein (Example: Galti check karne ke liye 'قل هو الله صمد' parh kar dekhein):")

if recorded_file is not None:
    audio_bytes = recorded_file.read()
    recognizer = sr.Recognizer()
    
    with st.spinner("AI aap ke lafzoon ka muwazna (comparison) kar raha hai..."):
        try:
            with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
                audio_data = recognizer.record(source)
                user_text = recognizer.recognize_google(audio_data, language="ar-AE")
            
            st.write(f"🗣️ **Aap ne parha:** {user_text}")
            
            user_words = user_text.split()
            galti_mili = False
            galti_wala_lafz = ""
            jump_to_seconds = 0
            
            # Har lafz ko aik aik kar ke check karna ke galti kahan hui
            for i, target in enumerate(ikhlas_words):
                cleaned_target = clean_word(target["word"])
                
                # Agar user ke lafz khatam ho gaye ya match nahi kiya
                if i >= len(user_words) or clean_word(user_words[i]) != cleaned_target:
                    galti_mili = True
                    galti_wala_lafz = user_words[i] if i < len(user_words) else "Lafz Chora"
                    jump_to_seconds = target["start_time"] # Galti ka exact waqt
                    break
            
            if galti_mili:
                st.error(f"⚠️ Lafzi Galti Mili! Aap ne '{galti_wala_lafz}' parha, jo ke galat hai.")
                st.warning(f"🔄 Qari Sahab automatic correction ke liye exact **{jump_to_seconds} seconds** se parhna shuru kar rahe hain:")
                
                # Qari Sahab ki audio ko exact galti wale timestamp se play karna
                st.audio(qari_audio_url, format="audio/mp3", start_time=jump_to_seconds, autoplay=True)
            else:
                st.success("🎉 MashaAllah! Aap ke saare alfaz bilkul darust hain. Qari sahab khamosh hain!")
                
        except sr.UnknownValueError:
            st.error("⚠️ AI awaz saaf nahi sun saka, dobara koshish karein.")
        except Exception as e:
            st.error(f"System Error: {e}")

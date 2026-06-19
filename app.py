import streamlit as st
from diff_match_patch import diff_match_patch

# Page Configuration
st.set_page_config(page_title="Quranic Recitation Checker", page_icon="📖", layout="centered")

st.title("📖 Quranic Error Detection & Correction")
st.write("اس ایپ میں سیو شدہ آڈیو ہمیشہ سامنے نظر آئے گی تاکہ آپ اسے سن سکیں۔")

# ہر آیت کا ٹیکسٹ اور انٹرنیٹ پر سیو شدہ آڈیو کا پکا لنک
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

# 1. UI: Dropdown سے آیت سلیکٹ کریں
selected_ayat = st.selectbox("کونسی آیت کی تلاوت چیک کرنی ہے؟", list(surah_fatiha.keys()))

correct_text = surah_fatiha[selected_ayat]["text"]
audio_link = surah_fatiha[selected_ayat]["audio_url"]

# 2. ریفرنس ٹیکسٹ (صحیح طریقہ) جو سامنے سکرین پر دیکھے گا
st.markdown("### 🟢 Reference Text (صحیح طریقہ):")
st.info(correct_text)

# 🔥 آپ کی ڈیمانڈ کے مطابق: یہ آڈیو پلیئر اب ہر وقت سکرین پر سامنے شو ہوگا!
st.markdown("### 🔊 اس آیت کی سیو شدہ آڈیو (Reference Audio):")
st.audio(audio_link, start_time=0)
st.caption("آپ مائیک کے بغیر بھی اس پلے بٹن کو دبا کر یہ آڈیو کسی بھی وقت سن سکتے ہیں۔")

st.markdown("---")

# 3. Simulation Input (مائیک کا متبادل ٹیسٹنگ کے لیے)
st.subheader("🎤 Simulation & Testing")
st.write("ابھی ٹیسٹنگ کے لیے نیچے والے باکس میں تلاوت کا ٹیکسٹ لکھیں۔ غلطی چیک کرنے کے لیے کوئی لفظ بدل دیں۔")

# خود بخود غلطی والا ٹیکسٹ سیٹ کرنا ٹیسٹنگ کو آسان بنانے کے لیے
default_user_text = correct_text
if selected_ayat == "Ayat 2":
    default_user_text = "الْحَمْدُ لِلَّهِ رَبِّ الْغَفُورِينَ"  # یہاں 'العالمين' کی جگہ 'الغفورين' لکھا ہے تاکہ گنتی پکڑی جائے
elif selected_ayat == "Ayat 4":
    default_user_text = "مَالِكِ يَوْمِ الدُّنْيَا"  # یہاں 'الدين' کی جگہ 'الدنيا' لکھا ہے

user_input_text = st.text_input("آپ کی تلاوت کا ان پٹ (یہاں ٹیکسٹ ایڈٹ کریں):", value=default_user_text)

# 4. ویریفیکیشن لاجک (بٹن دبانے پر)
if st.button("Verify My Recitation"):
    u_text = user_input_text.strip()
    c_text = correct_text.strip()
    
    if u_text == c_text:
        st.success("🎉 ماشاءاللہ! آپ کی تلاوت بالکل صحیح ہے۔")
    else:
        st.error("⚠️ تلاوت میں غلطی پکڑی گئی ہے!")
        
        # دونوں ٹیکسٹ کا موازنہ کرنا اور غلطی سامنے لانا
        dmp = diff_match_patch()
        diffs = dmp.diff_main(c_text, u_text)
        dmp.diff_cleanupSemantic(diffs)
        
        st.markdown("### 🔍 Correction Feedback:")
        st.write("آپ کے لکھے ہوئے ٹیکسٹ اور صحیح ٹیکسٹ میں فرق ہے۔ تصحیح کے لیے اوپر دی گئی آڈیو کو دوبارہ غور سے سنیں۔")
        
        # جیسے ہی بٹن دبے گا اور غلطی ہوگی، یہ آڈیو نیچے بھی خود بخود دوبارہ پلے ہونا شروع ہو جائے گی
        st.audio(audio_link, start_time=0)
        st.caption("🔊 غلطی کی وجہ سے صحیح تلاوت کی آڈیو خود بخود چل پڑی ہے۔")

st.markdown("---")
# پوری سورہ ایک ساتھ سننے کے لیے نیچے آپشن
if st.checkbox("پوری سورہ فاتحہ ایک ساتھ سنیں"):
    st.audio("https://audio.qurancdn.com/reciters/7/high.mp3")

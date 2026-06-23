import streamlit as st
import librosa
import numpy as np
import requests
import io
from scipy.spatial.distance import cdist
import nltk
from nltk.metrics.distance import edit_distance

# ایپ کی بنیادی سیٹنگز
st.set_page_config(page_title="القرآن - تجوید اور تلاوت مانیٹر", page_icon="📖", layout="centered")

st.title("📖 تلاوت اور تجوید اسسٹنٹ")
st.write("یہ ایپ آپ کی تلاوت کا قاری صاحب کی تلاوت سے ریل ٹائم موازنہ کرے گی۔")

# سورہ فاتحہ کی تمام آیات کا ڈیٹا (ٹیکسٹ اور آڈیو لنکس)
SURA_FATIHA = {
    "آیت 1": {"text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ", "url": "https://audio.qurancdn.com/Alafasy/mp3/1.mp3"},
    "آیت 2": {"text": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ", "url": "https://audio.qurancdn.com/Alafasy/mp3/2.mp3"},
    "آیت 3": {"text": "الرَّحْمَٰنِ الرَّحِيمِ", "url": "https://audio.qurancdn.com/Alafasy/mp3/3.mp3"},
    "آیت 4": {"text": "مَالِكِ يَوْمِ الدِّينِ", "url": "https://audio.qurancdn.com/Alafasy/mp3/4.mp3"},
    "آیت 5": {"text": "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ", "url": "https://audio.qurancdn.com/Alafasy/mp3/5.mp3"},
    "آیت 6": {"text": "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ", "url": "https://audio.qurancdn.com/Alafasy/mp3/6.mp3"},
    "آیت 7": {"text": "صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ", "url": "https://audio.qurancdn.com/Alafasy/mp3/7.mp3"}
}

# آیت سلیکٹ کرنے کے لیے ڈراپ ڈاؤن مینو (پورا قرآن کور کرنے کے لیے پہلا قدم)
selected_ayyah = st.selectbox("📖 تلاوت کے لیے آیت کا انتخاب کریں:", list(SURA_FATIHA.keys()))

current_ayyah_text = SURA_FATIHA[selected_ayyah]["text"]
current_ayyah_url = SURA_FATIHA[selected_ayyah]["url"]

# عربی ٹیکسٹ اسکرین پر بڑا دکھانا
st.markdown(f"<h2 style='text-align: center; color: #1E88E5; direction: rtl;'>{current_ayyah_text}</h2>", unsafe_allow_html=True)

st.write("---")

# 1. قاری صاحب کی آڈیو پلے کرنے کا فکسڈ طریقہ
st.markdown("### 1. قاری صاحب کی تلاوت سنیں:")

@st.cache_data
def download_audio(url):
    """آڈیو کو کلاؤڈ پر بلاک ہونے سے بچانے کے لیے پہلے ڈاؤن لوڈ کرنے کا فنکشن"""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
    except Exception as e:
        return None
    return None

qari_audio_bytes = download_audio(current_ayyah_url)

if qari_audio_bytes:
    # اب آڈیو ڈائریکٹ بائٹس سے پلے ہوگی، جو کلاؤڈ پر فیل نہیں ہوتی
    st.audio(qari_audio_bytes, format="audio/mp3")
else:
    st.error("قاری صاحب کی آڈیو لوڈ کرنے میں مسئلہ آ رہا ہے۔ انٹرنیٹ کنکشن چیک کریں۔")

st.write("---")

# 2. لائیو مائیکروفون ان پٹ (Live Mic Audio)
st.markdown("### 2. مائیکروفون سے اپنی لائیو تلاوت ریکارڈ کریں:")
st.info(" نیچے دیے گئے مائیک بٹن پر کلک کریں، براؤزر میں مائیک کی اجازت (Allow) دیں اور تلاوت شروع کریں۔")

# لائیو مائیک ان پٹ وزٹ
user_audio_file = st.audio_input("یہاں کلک کر کے ریکارڈنگ شروع کریں:")

# 3. آڈیو موازنہ کا انجن (Audio Comparison Engine)
def compare_audio_live(qari_bytes, user_file):
    try:
        # قاری صاحب کی آڈیو لوڈ کرنا
        qari_audio_data, qari_sr = librosa.load(io.BytesIO(qari_bytes), sr=16000)
        
        # صارف کی لائیو آڈیو لوڈ کرنا
        user_audio_data, user_sr = librosa.load(user_file, sr=16000)
        
        # آواز کے فیچرز (MFCCs) نکالنا
        qari_mfcc = librosa.feature.mfcc(y=qari_audio_data, sr=qari_sr, n_mfcc=13)
        user_mfcc = librosa.feature.mfcc(y=user_audio_data, sr=user_sr, n_mfcc=13)
        
        # فیچرز کو نارملائز کرنا
        qari_mfcc = (qari_mfcc - np.mean(qari_mfcc)) / (np.std(qari_mfcc) + 1e-8)
        user_mfcc = (user_mfcc - np.mean(user_mfcc)) / (np.std(user_mfcc) + 1e-8)
        
        # موازنہ (Cosine Distance)
        dist_matrix = cdist(qari_mfcc.T, user_mfcc.T, metric='cosine')
        matching_score = np.mean(np.min(dist_matrix, axis=1))
        
        # اسکور کیلکولیشن
        accuracy = max(0, min(100, int((1 - matching_score) * 100)))
        return accuracy

    except Exception as e:
        st.error(f"آڈیو پروسیسنگ میں ایرر: {e}")
        return None

# اگر صارف مائیک سے ریکارڈنگ مکمل کر لے
if user_audio_file is not None:
    st.success("🎤 آواز کامیابی سے ریکارڈ ہو گئی ہے!")
    st.info("🔄 آپ کی لائیو آواز کا قاری صاحب کی تلاوت سے موازنہ کیا جا رہا ہے...")
    
    # موازنہ رن کریں
    score = compare_audio_live(qari_audio_bytes, user_audio_file)
    
    if score is not None:
        st.write("---")
        st.markdown("### 📊 رزلٹ اور فیڈ بیک:")
        
        # تجوید کی بنیاد پر فیڈ بیک
        if score >= 80:
            st.success(f"ماشاءاللہ! آپ کی تلاوت قاری صاحب سے {score}% میچ کرتی ہے۔ تجوید بہترین ہے۔")
        elif score >= 55:
            st.warning(f"بہتر کوشش ہے! آپ کا میچنگ اسکور {score}% ہے۔ کچھ مخارج پر مزید توجہ دیں۔")
        else:
            st.error(f"دوبارہ کوشش کریں! آپ کا اسکور {score}% ہے۔ قاری صاحب کے تلفظ کو غور سے سن کر دوبارہ پڑھیں۔")
            
        st.progress(score / 100)

import streamlit as st
import librosa
import numpy as np
import requests
import io
import soundfile as sf
from scipy.spatial.distance import cdist

# ایپ کا ٹائٹل اور تعارف
st.set_page_config(page_title="القرآن - تجوید اور تلاوت مانیٹر", page_icon="📖", layout="centered")
st.title("📖 تلاوت اور تجوید اسسٹنٹ")
st.subheader("سورہ فاتحہ - آیت نمبر 1")

# قاری صاحب کی آڈیو کا یو آر ایل (لائٹ ویٹ MP3)
QARI_AUDIO_URL = "https://audio.qurancdn.com/Alafasy/mp3/1.mp3"

# 1. قاری صاحب کی آڈیو پلے کرنے کا بٹن
st.markdown("### 1. قاری صاحب کی تلاوت سنیں:")
if st.button("▶️ قاری صاحب کی آڈیو پلے کریں"):
    st.audio(QARI_AUDIO_URL)

st.write("---")

# 2. صارف کی تلاوت ریکارڈ کرنے کا سیکشن
st.markdown("### 2. اپنی تلاوت ریکارڈ یا اپلوڈ کریں:")
st.caption("بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ")

# اسٹریملیٹ کا ڈیفالٹ آڈیو ان پٹ وزٹ (یہ مائیکروفون سے لائیو ریکارڈ کرتا ہے)
user_audio_file = st.audio_input("اپنی آواز ریکارڈ کرنے کے لیے نیچے مائیک کے آئیکن پر کلک کریں:")

# 3. آڈیو موازنہ کا مین لاجک (Audio Comparison Engine)
def compare_audio(qari_url, user_file):
    try:
        # قاری صاحب کی آڈیو ڈاؤن لوڈ اور لوڈ کرنا
        response = requests.get(qari_url)
        qari_audio_data, qari_sr = librosa.load(io.BytesIO(response.content), sr=None)
        
        # صارف کی ریکارڈ شدہ آڈیو لوڈ کرنا
        user_audio_data, user_sr = librosa.load(user_file, sr=None)
        
        # دونوں آڈیوز کے MFCC فیچرز نکالنا (یہ آواز کے مخارج اور اتار چڑھاؤ کو ماپتے ہیں)
        qari_mfcc = librosa.feature.mfcc(y=qari_audio_data, sr=qari_sr, n_mfcc=13)
        user_mfcc = librosa.feature.mfcc(y=user_audio_data, sr=user_sr, n_mfcc=13)
        
        # فیچرز کو نارملائز کرنا
        qari_mfcc = (qari_mfcc - np.mean(qari_mfcc)) / np.std(qari_mfcc)
        user_mfcc = (user_mfcc - np.mean(user_mfcc)) / np.std(user_mfcc)
        
        # Dynamic Time Warping (DTW) کا استعمال کرتے ہوئے موازنہ (یہ سپیڈ کے فرق کو ایڈجسٹ کرتا ہے)
        # یہاں ہم ایک سادہ کاسٹ میٹرکس ڈسٹنس نکال رہے ہیں پروٹو ٹائپ کے لیے
        dist_matrix = cdist(qari_mfcc.T, user_mfcc.T, metric='cosine')
        matching_score = np.mean(np.min(dist_matrix, axis=1))
        
        # اسکور کو فیصد (Percentage) میں تبدیل کرنا (یہ ایک فرضی میپنگ ہے، جسے ہم بعد میں فائن ٹیون کریں گے)
        accuracy = max(0, min(100, int((1 - matching_score) * 100)))
        return accuracy

    except Exception as e:
        st.error(f"آڈیو پروسیسنگ میں مسئلہ آیا: {e}")
        return None

# اگر صارف نے آڈیو ریکارڈ کر لی ہے تو پروسیس کریں
if user_audio_file is not None:
    st.info("🔄 آپ کی تلاوت کا قاری صاحب کی تلاوت سے موازنہ کیا جا رہا ہے...")
    
    # موازنہ رن کریں
    score = compare_audio(QARI_AUDIO_URL, user_audio_file)
    
    if score is not None:
        st.write("---")
        st.markdown("### 📊 رزلٹ اور فیڈ بیک:")
        
        # اسکور کی بنیاد پر رنگ تبدیل کرنا اور فیڈ بیک دینا
        if score >= 85:
            st.success(f"Excellent! آپ کی تلاوت قاری صاحب سے {score}% میچ کرتی ہے۔ تجوید بہترین ہے۔")
        elif score >= 60:
            st.warning(f"Good Effort! آپ کا میچنگ اسکور {score}% ہے۔ کچھ مخارج یا صفات میں بہتری کی گنجائش ہے۔")
        else:
            st.error(f"توجہ کی ضرورت! آپ کا اسکور {score}% ہے۔ دوبارہ کوشش کریں اور قاری صاحب کے تلفظ کو غور سے سنیں۔")
            
        # پروگریس بار دکھانا
        st.progress(score / 100)

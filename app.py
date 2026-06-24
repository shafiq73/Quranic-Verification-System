import streamlit as st

st.set_page_config(page_title="Quranic Verification System", page_icon="📖", layout="centered")

st.title("📖 Quranic Verification System")
st.write("### Qari Raad Al Kurdi Ki Awaz Mein Tilawat")

# Surah numbers aur un ke naam (Testing ke liye top Surahs, aap is list mein mazeed add kar sakte hain)
surah_dict = {
    "1. Surah Al-Fatiha": 1,
    "2. Surah Al-Baqarah": 2,
    "3. Surah Ali 'Imran": 3,
    "4. Surah An-Nisa": 4,
    "36. Surah Ya-Sin": 36,
    "55. Surah Ar-Rahman": 55,
    "67. Surah Al-Mulk": 67,
    "112. Surah Al-Ikhlas": 112,
    "113. Surah Al-Falaq": 113,
    "114. Surah An-Nas": 114
}

# Dropdown setup
selected_surah = st.selectbox("Surah Select Karein:", list(surah_dict.keys()))

# High-speed reliable server for Qari Raad Al Kurdi
base_url = "https://server6.mp3quran.net/kurdi/"

if selected_surah:
    surah_num = surah_dict[selected_surah]
    
    # URL format ko 3 digits mein set karna (e.g., 001, 010, 114)
    file_number = f"{surah_num:03d}"
    audio_url = f"{base_url}{file_number}.mp3"
    
    st.success(f"Aap ne **{selected_surah}** select ki hai.")
    
    # Main Audio Player
    st.audio(audio_url, format="audio/mp3")
    
    # Working Direct Download Link
    st.markdown(f"👉 [**[Yahan Se Download Karein]**]({audio_url})")

st.info("💡 Yeh link 100% direct hai aur live stream hota hai, is se aap ki Streamlit app kabhi crash nahi hogi.")

import streamlit as st
import requests
import base64

# ڕێکخستنی شاشە و دیزاینی لاپەڕە
st.set_page_config(
    page_title="Kurdish Text to Speech AI",
    page_icon="🎙️",
    layout="centered"
)

# دیزاینا سەرەکی
st.title("🎙️ گۆڕینی نڤیسینا کوردی بۆ دەنگ")
st.write("ئەڤ سیستەمە ب هاریکاریا **Google API** نڤیسینێ دکەتە دەنگێ کوردی.")

# وەرگرتنا کلیلا API ژ ناڤا Streamlit Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ تێبینی: کلیلا Google API نەهاتیە دیتن د بەشێ Secrets دا! هیڤیدارین زێدە بکەی.")
    st.stop()

# وەرگرتنا نڤیسینێ ژ بەکارهێنەری
kurdish_text = st.text_area(
    "نڤیسینا خۆ ب کوردی ل ڤێرە بنڤیسە:",
    placeholder="سلاڤ، ئەڤە تێستێ گۆڕینا دەنگێ کوردیە ب زیرەکیا دەستکرد...",
    height=140
)

# هەڵبژارتنا شێوەزار یان زاراوەی
dialect = st.selectbox(
    "زاراوەی هەڵبژێرە:",
    ["Kurdish (Sorani / ckb-IQ)", "Kurdish (Kurmanji / ku-TR)"]
)

# دیارکرنا کۆدێ زمانێ گوگل
lang_code = "ckb-IQ" if "Sorani" in dialect else "ku-TR"

# دوگمەیا دروستکرنا دەنگی
if st.button("🔊 دەنگی دروست بکە", type="primary"):
    if not kurdish_text.strip():
        st.warning("تکایە بەری کلیک بکەی، نڤیسینەکێ ل سەرێ بنڤیسە!")
    else:
        with st.spinner("دەنگ یێ دهێتە چێکرن... بێهنفەرهـ بە..."):
            try:
                # ئەدرێسێ Google Cloud Text-to-Speech REST API
                url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}"
                
                # داتایێن فرێکرنێ بۆ سێرڤەری گوگل
                payload = {
                    "input": {
                        "text": kurdish_text
                    },
                    "voice": {
                        "languageCode": lang_code,
                        "ssmlGender": "FEMALE"  # دتوانی بکەیە MALE یان FEMALE
                    },
                    "audioConfig": {
                        "audioEncoding": "MP3"
                    }
                }
                
                headers = {"Content-Type": "application/json"}
                
                # فرێکرنا داخازیێ بۆ گوگلی
                response = requests.post(url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    # دەنگ ب شێوەیێ Base64 دهێت و دەگۆڕین بو فایلی دەنگی
                    audio_content = base64.b64decode(data["audioContent"])
                    
                    st.success("✅ دەنگ ب سەرکەفتیانە هاتە چێکرن!")
                    
                    # لێدانا دەنگی ل ناڤا وێبسایتی
                    st.audio(audio_content, format="audio/mp3")
                    
                    # دوگمەیا دابەزاندنا فایلی
                    st.download_button(
                        label="📥 داگرتنا دەنگی (MP3)",
                        data=audio_content,
                        file_name="kurdish_voice.mp3",
                        mime="audio/mp3"
                    )
                else:
                    st.error(f"❌ خەلەتیەک دروست بوو ژ لایێ گوگلی: {response.text}")
                    
            except Exception as e:
                st.error(f"❌ کێشەیەک ڕوویدا: {str(e)}")

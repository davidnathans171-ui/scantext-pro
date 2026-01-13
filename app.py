import streamlit as st
import pytesseract
from PIL import Image

# Lokasi Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ======================
# KONFIGURASI HALAMAN
# ======================
st.set_page_config(
    page_title="ScanText Pro",
    page_icon="📄",
    layout="centered"
)

# ======================
# STYLE TAMBAHAN
# ======================
st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}
.main-title {
    text-align: center;
    font-size: 36px;
    font-weight: bold;
}
.sub-title {
    text-align: center;
    color: gray;
    margin-bottom: 20px;
}
.card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
.footer {
    text-align: center;
    color: gray;
    font-size: 12px;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# ======================
# HEADER
# ======================
st.markdown("<div class='main-title'>📄 ScanText Pro</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Aplikasi AI OCR untuk mengubah gambar menjadi teks</div>", unsafe_allow_html=True)

# ======================
# SISTEM LIMIT SCAN
# ======================
if "scan_count" not in st.session_state:
    st.session_state.scan_count = 0

MAX_FREE_SCAN = 5
sisa_scan = MAX_FREE_SCAN - st.session_state.scan_count

if sisa_scan > 0:
    st.success(f"🎁 Kamu masih punya {sisa_scan} scan gratis")
else:
    st.error("❌ Scan gratis kamu sudah habis. Silakan upgrade ke versi Pro.")

# ======================
# CARD: UPLOAD
# ======================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📤 Upload Gambar")
uploaded_file = st.file_uploader("Pilih gambar dengan teks", type=["png", "jpg", "jpeg"])
st.markdown("</div>", unsafe_allow_html=True)

# ======================
# PROSES OCR
# ======================
if uploaded_file:
    image = Image.open(uploaded_file)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🖼️ Preview Gambar")
    st.image(image, use_column_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🔍 Proses OCR")

    if st.button("🚀 Baca Teks Sekarang"):
        if st.session_state.scan_count >= MAX_FREE_SCAN:
            st.error("Scan gratis sudah habis. Upgrade ke ScanText Pro untuk lanjut.")
        else:
            text = pytesseract.image_to_string(image, lang="eng+ind")

            st.text_area("📄 Hasil Teks:", text, height=300)
            st.session_state.scan_count += 1

            sisa = MAX_FREE_SCAN - st.session_state.scan_count
            st.success(f"✅ Berhasil! Sisa scan gratis: {sisa}")

            st.write("💡 Tips: Blok teks di atas lalu tekan **Ctrl + C** untuk menyalin.")
    st.markdown("</div>", unsafe_allow_html=True)

# ======================
# FOOTER
# ======================
st.markdown("""
<div class='footer'>
© 2026 ScanText Pro • Powered by AI OCR<br>
Versi Demo – Untuk penggunaan komersial hubungi admin
</div>
""", unsafe_allow_html=True)

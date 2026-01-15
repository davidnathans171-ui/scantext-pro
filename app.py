import streamlit as st
from PIL import Image
import os

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="ScanText Pro - Safe Mode",
    layout="centered"
)

# =========================
# LOGO
# =========================
LOGO_PATH = "logo.png"

if os.path.exists(LOGO_PATH):
    try:
        logo = Image.open(LOGO_PATH)
        st.image(logo, width=150)
    except:
        st.warning("⚠️ Logo ada, tapi tidak bisa dibuka.")
else:
    st.warning("⚠️ Logo belum ditemukan. Pastikan ada file logo.png")

# =========================
# TITLE
# =========================
st.title("ScanText Pro - SAFE MODE")
st.caption("Versi aman untuk cek stabilitas sebelum OCR diaktifkan.")

st.info("""
Jika aplikasi ini bisa dibuka di HP ayah kamu tanpa error,
berarti:
- Hosting Streamlit normal
- Akses publik normal
- Masalah sebelumnya murni dari kode OCR
""")

# =========================
# UPLOAD GAMBAR
# =========================
st.subheader("📷 Upload Gambar")

uploaded_file = st.file_uploader(
    "Upload gambar (PNG, JPG, JPEG)",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.success("Gambar berhasil diupload!")
    st.image(image, caption="Preview gambar", use_column_width=True)

    st.warning("⚠️ OCR belum aktif. Ini masih SAFE MODE.")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("© 2026 • ScanText Pro • Safe Mode")
st.subheader("🔍 OCR (TEST MODE)")


uploaded_file = st.file_uploader(
    "Upload gambar untuk OCR",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    st.image(uploaded_file, caption="Gambar yang diupload", use_container_width=True)

    if st.button("Proses OCR"):
        st.info("OCR sedang diproses...")

        try:
            import easyocr
            reader = easyocr.Reader(['en'], gpu=False)

            from PIL import Image
            import numpy as np

            image = Image.open(uploaded_file).convert("RGB")
            img_array = np.array(image)

            results = reader.readtext(img_array)

            text = ""
            for r in results:
                text += r[1] + "\n"

            st.success("OCR selesai!")
            st.text_area("Hasil OCR:", text, height=200)

        except Exception as e:
            st.error("OCR gagal dijalankan:")
            st.code(str(e))


if uploaded_file is not None:
    if st.button("Proses OCR (TEST)"):
        st.info("OCR akan diaktifkan di tahap berikutnya.")
        st.warning("Saat ini OCR masih dimatikan untuk menjaga stabilitas.")


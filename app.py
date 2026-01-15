import streamlit as st
import os

# ============================
# KONFIGURASI
# ============================
SAFE_MODE = False  # Ubah ke False jika OCR mau diaktifkan
LOGO_PATH = "logo.png"

st.set_page_config(
    page_title="ScanText Pro",
    layout="centered"
)

# ============================
# LOGO
# ============================
if os.path.exists(LOGO_PATH) and os.path.isfile(LOGO_PATH):
    try:
        st.image(LOGO_PATH, width=140)
    except:
        st.warning("⚠ Logo ditemukan tapi gagal dibuka.")
else:
    st.warning("⚠ Logo belum ditemukan. Pastikan ada file logo.png di folder yang sama.")

# ============================
# JUDUL
# ============================
st.title("📄 ScanText Pro - SAFE MODE")
st.caption("Versi aman untuk cek stabilitas sebelum OCR diaktifkan.")

st.info("""
Jika aplikasi ini bisa dibuka tanpa error:
- Hosting Streamlit normal  
- Akses publik normal  
- Masalah sebelumnya murni dari kode OCR
""")

# ============================
# UPLOAD GAMBAR
# ============================
st.subheader("📷 Upload Gambar")

uploaded_file = st.file_uploader(
    "Upload gambar (PNG, JPG, JPEG)",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    st.image(uploaded_file, caption="Preview gambar", use_container_width=True)

# ============================
# OCR TEST MODE
# ============================
st.markdown("---")
st.subheader("🔍 OCR (TEST MODE)")

if uploaded_file is not None:

    if SAFE_MODE:
        st.warning("⚠ OCR belum aktif. Ini masih SAFE MODE.")
        st.write("Untuk mengaktifkan OCR, ubah:")
        st.code("SAFE_MODE = False", language="python")

    else:
        if st.button("🚀 Proses OCR"):
            st.info("OCR sedang diproses...")

            try:
                import easyocr
                import numpy as np
                from PIL import Image

                reader = easyocr.Reader(['en', 'id'], gpu=False)
                image = Image.open(uploaded_file)
                result = reader.readtext(np.array(image), detail=0)

                text = "\n".join(result)

                st.success("OCR selesai!")
                st.text_area("📄 Hasil OCR", text, height=250)

            except Exception as e:
                st.error(f"Terjadi error saat OCR: {e}")

else:
    st.info("Silakan upload gambar terlebih dahulu.")

# ============================
# FOOTER
# ============================
st.markdown("---")
st.markdown("© 2026 • ScanText Pro • Safe Mode")

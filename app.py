import streamlit as st
from PIL import Image
import pytesseract

st.set_page_config(page_title="ScanText Pro", layout="centered")

st.title("ScanText Pro – STEP 2 (OCR ACTIVE)")
st.success("Upload gambar dan tekan tombol Proses OCR.")

st.markdown("### 📷 Upload Gambar")
uploaded_file = st.file_uploader(
    "Upload gambar (PNG, JPG, JPEG)",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Preview gambar", use_container_width=True)

    if st.button("🔍 Proses OCR"):
        with st.spinner("Sedang memproses OCR..."):
            try:
                text = pytesseract.image_to_string(image, lang="eng+ind")

                if text.strip() == "":
                    st.warning("Tidak ada teks terdeteksi.")
                else:
                    st.success("OCR berhasil!")
                    st.text_area(
                        "Hasil OCR:",
                        text,
                        height=300
                    )

            except Exception as e:
                st.error("Terjadi error saat OCR:")
                st.code(str(e))

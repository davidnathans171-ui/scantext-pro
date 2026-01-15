import streamlit as st

st.set_page_config(page_title="ScanText Pro", layout="centered")

st.title("ScanText Pro – STEP 1")
st.success("Hosting normal. Sekarang kita aktifkan upload gambar dulu.")

st.markdown("### 📷 Upload Gambar")
uploaded_file = st.file_uploader(
    "Upload gambar (PNG, JPG, JPEG)",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:
    st.image(uploaded_file, caption="Preview gambar", use_container_width=True)
    st.info("Gambar berhasil diupload. OCR akan diaktifkan di tahap berikutnya.")

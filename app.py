import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import io
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ===============================
# CONFIG
# ===============================
st.set_page_config(page_title="ScanText Pro", layout="centered")

# ===============================
# LOGO NATHANS AI
# ===============================
logo_path = "logo.png"

if os.path.isfile(logo_path):
    logo = Image.open(logo_path)
    st.image(logo, width=120)
else:
    st.warning("⚠️ Logo 'logo.png' tidak ditemukan. Pastikan file ada di folder yang sama dengan app.py")

# ===============================
# JUDUL
# ===============================
st.title("📄 ScanText Pro")
st.caption("Aplikasi AI OCR untuk mengubah gambar menjadi teks, bisa diedit, dan di-download")

# ===============================
# LOAD OCR MODEL (CACHE)
# ===============================
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en', 'id'], gpu=False)

reader = load_reader()

# ===============================
# SESSION STATE
# ===============================
if "ocr_text" not in st.session_state:
    st.session_state.ocr_text = ""

if "image" not in st.session_state:
    st.session_state.image = None

# ===============================
# AMBIL GAMBAR
# ===============================
st.subheader("📷 Ambil Gambar")

tab1, tab2 = st.tabs(["📂 Upload Gambar", "📸 Kamera Langsung"])

with tab1:
    uploaded_file = st.file_uploader(
        "Upload gambar",
        type=["png", "jpg", "jpeg"]
    )
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.session_state.image = image

with tab2:
    camera_image = st.camera_input("Ambil foto dari kamera")
    if camera_image:
        image = Image.open(camera_image)
        st.session_state.image = image

# ===============================
# TAMPILKAN GAMBAR
# ===============================
if st.session_state.image is not None:
    st.image(st.session_state.image, caption="Gambar yang digunakan", use_column_width=True)

    if st.button("🔍 Baca Teks dari Gambar"):
        with st.spinner("Membaca teks dari gambar..."):
            result = reader.readtext(np.array(st.session_state.image), detail=0)
            st.session_state.ocr_text = "\n".join(result)

# ===============================
# HASIL TEKS (BISA DIEDIT)
# ===============================
st.subheader("✏️ Hasil Teks (Bisa Diedit)")

edited_text = st.text_area(
    "Edit teks hasil OCR di sini:",
    value=st.session_state.ocr_text,
    height=250
)

st.session_state.ocr_text = edited_text

# ===============================
# BUTTON ACTION
# ===============================
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🧹 Reset / Hapus Teks"):
        st.session_state.ocr_text = ""
        st.session_state.image = None
        st.experimental_rerun()

with col2:
    txt_bytes = st.session_state.ocr_text.encode("utf-8")
    st.download_button(
        label="📄 Download TXT",
        data=txt_bytes,
        file_name="scantext.txt",
        mime="text/plain"
    )

with col3:
    # Generate PDF
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    text_object = c.beginText(40, height - 40)
    for line in st.session_state.ocr_text.split("\n"):
        text_object.textLine(line)

    c.drawText(text_object)
    c.showPage()
    c.save()

    buffer.seek(0)

    st.download_button(
        label="📑 Download PDF",
        data=buffer,
        file_name="scantext.pdf",
        mime="application/pdf"
    )

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.markdown("💡 **Nathans AI – ScanText Pro**")

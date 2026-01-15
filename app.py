import os
import io
import streamlit as st
from PIL import Image
import easyocr
import numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# =============================
# CONFIG HALAMAN
# =============================
st.set_page_config(
    page_title="ScanText Pro - Nathans AI",
    layout="centered"
)

# =============================
# LOGO NATHANS AI
# =============================
LOGO_PATH = "logo.png"

if os.path.isfile(LOGO_PATH):
    logo = Image.open(LOGO_PATH)
    st.image(logo, width=120)
else:
    st.warning("⚠️ Logo Nathans AI tidak ditemukan. Pastikan file logo.png ada di folder yang sama dengan app.py")

# =============================
# JUDUL APLIKASI
# =============================
st.title("📄 ScanText Pro")
st.caption("Aplikasi AI OCR untuk mengubah gambar menjadi teks, bisa diedit, dan di-download")

# =============================
# LOAD OCR (CACHE AGAR CEPAT)
# =============================
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en', 'id'], gpu=False)

reader = load_reader()

# =============================
# SESSION STATE
# =============================
if "ocr_text" not in st.session_state:
    st.session_state.ocr_text = ""

if "image" not in st.session_state:
    st.session_state.image = None

# =============================
# AMBIL GAMBAR (UPLOAD / KAMERA)
# =============================
st.subheader("📸 Ambil Gambar")

tab1, tab2 = st.tabs(["📁 Upload Gambar", "📷 Kamera Langsung"])

with tab1:
    uploaded_file = st.file_uploader(
        "Upload gambar",
        type=["png", "jpg", "jpeg"]
    )
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.session_state.image = image
        st.image(image, caption="Gambar yang diupload", use_container_width=True)

with tab2:
    camera_image = st.camera_input("Ambil gambar dari kamera")
    if camera_image:
        image = Image.open(camera_image)
        st.session_state.image = image
        st.image(image, caption="Gambar dari kamera", use_container_width=True)

# =============================
# PROSES OCR
# =============================
if st.session_state.image is not None:
    if st.button("🔍 Baca Teks dari Gambar"):
        with st.spinner("Sedang membaca teks..."):
            img_array = np.array(st.session_state.image)
            result = reader.readtext(img_array, detail=0)
            st.session_state.ocr_text = "\n".join(result)

# =============================
# HASIL TEKS (BISA DIEDIT)
# =============================
st.subheader("✏️ Hasil Teks (Bisa Diedit)")

edited_text = st.text_area(
    "Edit teks hasil OCR di sini:",
    value=st.session_state.ocr_text,
    height=250
)

st.session_state.ocr_text = edited_text

# =============================
# TOMBOL RESET
# =============================
if st.button("♻️ Reset / Hapus Teks"):
    st.session_state.ocr_text = ""
    st.session_state.image = None
    st.success("Teks dan gambar berhasil direset!")

# =============================
# DOWNLOAD TXT
# =============================
if st.session_state.ocr_text.strip() != "":
    st.download_button(
        label="📄 Download sebagai TXT",
        data=st.session_state.ocr_text,
        file_name="hasil_ocr.txt",
        mime="text/plain"
    )

# =============================
# DOWNLOAD PDF
# =============================
def create_pdf(text):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    x_margin = 40
    y_margin = 800
    line_height = 14

    y = y_margin
    for line in text.split("\n"):
        if y <= 40:
            c.showPage()
            y = y_margin
        c.drawString(x_margin, y, line)
        y -= line_height

    c.save()
    buffer.seek(0)
    return buffer

if st.session_state.ocr_text.strip() != "":
    pdf_file = create_pdf(st.session_state.ocr_text)
    st.download_button(
        label="📕 Download sebagai PDF",
        data=pdf_file,
        file_name="hasil_ocr.pdf",
        mime="application/pdf"
    )

# =============================
# FOOTER
# =============================
st.markdown("---")
st.markdown("🚀 **ScanText Pro - Nathans AI** | OCR App with Camera, Edit, Reset & Download")

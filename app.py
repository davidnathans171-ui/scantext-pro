import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import io
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ======================
# LOGO NATHANS AI (AMAN)
# ======================
LOGO_PATH = "logo.png"

st.set_page_config(page_title="ScanText Pro", layout="centered")

if os.path.exists(LOGO_PATH) and os.path.isfile(LOGO_PATH):
    try:
        logo = Image.open(LOGO_PATH)
        st.image(logo, width=120)
    except:
        st.warning("⚠ Logo ditemukan tapi tidak bisa dibuka.")
else:
    st.warning("⚠ Logo Nathans AI belum ditemukan. Pastikan file bernama logo.png berada di satu folder dengan app.py")

st.title("📄 ScanText Pro")
st.caption("Aplikasi AI OCR untuk mengubah gambar menjadi teks, bisa diedit, dan di-download")

# ======================
# LOAD OCR
# ======================
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en', 'id'], gpu=False)

reader = load_reader()

# ======================
# SESSION STATE
# ======================
if "ocr_text" not in st.session_state:
    st.session_state.ocr_text = ""

if "image" not in st.session_state:
    st.session_state.image = None

# ======================
# AMBIL GAMBAR
# ======================
st.header("📸 Ambil Gambar")
tab1, tab2 = st.tabs(["📂 Upload Gambar", "📷 Kamera Langsung"])

with tab1:
    uploaded_file = st.file_uploader(
        "Upload gambar", type=["png", "jpg", "jpeg"]
    )
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.session_state.image = image
        st.image(image, caption="Gambar diupload", use_column_width=True)

with tab2:
    camera_image = st.camera_input("Ambil gambar dari kamera")
    if camera_image:
        image = Image.open(camera_image)
        st.session_state.image = image
        st.image(image, caption="Gambar dari kamera", use_column_width=True)

# ======================
# OCR
# ======================
if st.session_state.image is not None:
    if st.button("🔍 Baca Teks dari Gambar"):
        with st.spinner("Membaca teks..."):
            result = reader.readtext(np.array(st.session_state.image), detail=0)
            st.session_state.ocr_text = "\n".join(result)

# ======================
# HASIL TEKS
# ======================
st.header("✏ Hasil Teks (Bisa Diedit)")

st.session_state.ocr_text = st.text_area(
    "Edit teks OCR di sini:",
    st.session_state.ocr_text,
    height=250
)

# ======================
# TOMBOL RESET
# ======================
if st.button("🧹 Reset / Hapus Teks"):
    st.session_state.ocr_text = ""
    st.session_state.image = None
    st.experimental_rerun()

# ======================
# DOWNLOAD TXT
# ======================
if st.session_state.ocr_text.strip():
    st.download_button(
        "⬇ Download TXT",
        data=st.session_state.ocr_text,
        file_name="scantext.txt",
        mime="text/plain"
    )

# ======================
# DOWNLOAD PDF
# ======================
def generate_pdf(text):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    x, y = 40, height - 40

    for line in text.split("\n"):
        c.drawString(x, y, line)
        y -= 14
        if y < 40:
            c.showPage()
            y = height - 40

    c.save()
    buffer.seek(0)
    return buffer

if st.session_state.ocr_text.strip():
    pdf_data = generate_pdf(st.session_state.ocr_text)
    st.download_button(
        "⬇ Download PDF",
        data=pdf_data,
        file_name="scantext.pdf",
        mime="application/pdf"
    )

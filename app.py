import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import io
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="ScanText Pro", layout="centered")

# =========================
# LOGO NATHANS AI (AMAN 100%)
# =========================
LOGO_PATH = os.path.join(os.path.dirname(__file__), "logo.png")

try:
    if os.path.isfile(LOGO_PATH):
        st.image(LOGO_PATH, width=150)
    else:
        st.warning("⚠️ Logo tidak ditemukan. Pastikan file bernama logo.png berada satu folder dengan app.py")
except Exception as e:
    st.warning(f"⚠️ Gagal menampilkan logo: {e}")

# =========================
# TITLE
# =========================
st.title("📄 ScanText Pro")
st.caption("Aplikasi AI OCR untuk mengubah gambar menjadi teks, bisa diedit, reset, dan di-download.")

# =========================
# LOAD OCR MODEL
# =========================
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en', 'id'], gpu=False)

reader = load_reader()

# =========================
# IMAGE INPUT
# =========================
st.header("📸 Ambil Gambar")
tabs = st.tabs(["📁 Upload Gambar", "📷 Kamera Langsung"])

image = None

with tabs[0]:
    uploaded_file = st.file_uploader("Upload gambar", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Gambar diupload", use_container_width=True)

with tabs[1]:
    camera_image = st.camera_input("Ambil foto")
    if camera_image:
        image = Image.open(camera_image)
        st.image(image, caption="Gambar dari kamera", use_container_width=True)

# =========================
# OCR PROCESS
# =========================
ocr_text = ""

if image:
    with st.spinner("🔍 Sedang memproses OCR..."):
        img_np = np.array(image)
        result = reader.readtext(img_np)
        ocr_text = "\n".join([text for _, text, _ in result])

# =========================
# TEXT EDITOR
# =========================
st.header("📝 Hasil Teks (Bisa Diedit)")

if "text_result" not in st.session_state:
    st.session_state.text_result = ""

if ocr_text:
    st.session_state.text_result = ocr_text

text_area = st.text_area(
    "Edit teks hasil OCR di sini:",
    value=st.session_state.text_result,
    height=250
)

st.session_state.text_result = text_area

# =========================
# BUTTONS
# =========================
col1, col2 = st.columns(2)

with col1:
    if st.button("🧹 Reset / Hapus Teks"):
        st.session_state.text_result = ""
        st.experimental_rerun()

with col2:
    st.success("Siap di-download")

# =========================
# DOWNLOAD TXT
# =========================
st.subheader("⬇️ Download TXT")

st.download_button(
    label="📄 Download TXT",
    data=st.session_state.text_result,
    file_name="scantex_result.txt",
    mime="text/plain"
)

# =========================
# DOWNLOAD PDF
# =========================
st.subheader("⬇️ Download PDF")

def generate_pdf(text):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    x = 40
    y = height - 50
    for line in text.split("\n"):
        if y < 40:
            c.showPage()
            y = height - 50
        c.drawString(x, y, line)
        y -= 15

    c.save()
    buffer.seek(0)
    return buffer

pdf_data = generate_pdf(st.session_state.text_result)

st.download_button(
    label="📑 Download PDF",
    data=pdf_data,
    file_name="scantex_result.pdf",
    mime="application/pdf"
)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("🚀 **ScanText Pro - Nathans AI** | OCR App dengan Kamera, Edit, Reset & Download")

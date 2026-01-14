import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="ScanText Pro", layout="centered")

st.title("📄 ScanText Pro")
st.caption("Aplikasi AI OCR untuk mengubah gambar menjadi teks, bisa diedit, dan di-download")

# =========================
# LOAD OCR (CACHE AGAR CEPAT)
# =========================
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en', 'id'], gpu=False)

reader = load_reader()

# =========================
# SESSION STATE
# =========================
if "ocr_text" not in st.session_state:
    st.session_state.ocr_text = ""

# =========================
# INPUT GAMBAR (UPLOAD / KAMERA)
# =========================
st.subheader("📸 Ambil Gambar")

tab1, tab2 = st.tabs(["📁 Upload Gambar", "📷 Kamera Langsung"])

image = None

with tab1:
    uploaded_file = st.file_uploader("Upload gambar", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Gambar dari Upload", use_column_width=True)

with tab2:
    camera_file = st.camera_input("Ambil foto dengan kamera")
    if camera_file:
        image = Image.open(camera_file)
        st.image(image, caption="Gambar dari Kamera", use_column_width=True)

# =========================
# OCR PROCESS
# =========================
if image is not None:
    if st.button("🔍 Baca Teks dari Gambar"):
        with st.spinner("Membaca teks dari gambar..."):
            result = reader.readtext(np.array(image), detail=0)
            st.session_state.ocr_text = "\n".join(result)
        st.success("OCR selesai!")

# =========================
# EDIT TEKS
# =========================
st.subheader("✏️ Hasil Teks (Bisa Diedit)")
edited_text = st.text_area(
    "Edit teks hasil OCR di sini:",
    value=st.session_state.ocr_text,
    height=300
)
st.session_state.ocr_text = edited_text

# =========================
# DOWNLOAD TXT
# =========================
st.download_button(
    label="⬇️ Download TXT",
    data=st.session_state.ocr_text,
    file_name="hasil_ocr.txt",
    mime="text/plain"
)

# =========================
# GENERATE PDF
# =========================
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

pdf_file = generate_pdf(st.session_state.ocr_text)

st.download_button(
    label="⬇️ Download PDF",
    data=pdf_file,
    file_name="hasil_ocr.pdf",
    mime="application/pdf"
)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown(
    "<center>© 2026 ScanText Pro • Powered by AI OCR<br>Versi Demo – Untuk penggunaan komersial hubungi admin</center>",
    unsafe_allow_html=True
)

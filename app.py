import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ==========================
# CONFIG
# ==========================
st.set_page_config(page_title="ScanText Pro", layout="centered")

# Logo Nathans AI
st.image("logo.png", width=120)

st.title("📄 ScanText Pro")
st.caption("Aplikasi AI OCR untuk mengubah gambar menjadi teks, bisa diedit, di-reset, dan di-download")

# ==========================
# LOAD OCR (CACHE AGAR CEPAT)
# ==========================
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en', 'id'], gpu=False)

reader = load_reader()

# ==========================
# SESSION STATE
# ==========================
if "ocr_text" not in st.session_state:
    st.session_state.ocr_text = ""

if "image" not in st.session_state:
    st.session_state.image = None

# ==========================
# AMBIL GAMBAR
# ==========================
st.subheader("📸 Ambil Gambar")

tab1, tab2 = st.tabs(["📂 Upload Gambar", "📷 Kamera Langsung"])

with tab1:
    uploaded_file = st.file_uploader(
        "Upload gambar (PNG, JPG, JPEG)",
        type=["png", "jpg", "jpeg"]
    )
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.session_state.image = image
        st.image(image, caption="Gambar yang diupload", use_column_width=True)

with tab2:
    camera_image = st.camera_input("Ambil gambar langsung dari kamera")
    if camera_image:
        image = Image.open(camera_image)
        st.session_state.image = image
        st.image(image, caption="Gambar dari kamera", use_column_width=True)

# ==========================
# PROSES OCR
# ==========================
if st.session_state.image is not None:
    if st.button("🔍 Baca Teks dari Gambar"):
        with st.spinner("Membaca teks dari gambar..."):
            result = reader.readtext(np.array(st.session_state.image), detail=0)
            st.session_state.ocr_text = "\n".join(result)

# ==========================
# HASIL TEKS (BISA DIEDIT)
# ==========================
st.subheader("✏️ Hasil Teks (Bisa Diedit)")

st.session_state.ocr_text = st.text_area(
    "Edit teks hasil OCR di sini:",
    value=st.session_state.ocr_text,
    height=250
)

# ==========================
# TOMBOL RESET / HAPUS TEKS
# ==========================
col1, col2 = st.columns(2)

with col1:
    if st.button("🗑️ Reset / Hapus Teks"):
        st.session_state.ocr_text = ""
        st.session_state.image = None
        st.experimental_rerun()

with col2:
    st.write("")

# ==========================
# DOWNLOAD TXT
# ==========================
if st.session_state.ocr_text.strip():
    st.download_button(
        label="⬇️ Download sebagai TXT",
        data=st.session_state.ocr_text,
        file_name="scantext_pro.txt",
        mime="text/plain"
    )

# ==========================
# DOWNLOAD PDF
# ==========================
def generate_pdf(text):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    x, y = 40, height - 40

    for line in text.split("\n"):
        c.drawString(x, y, line)
        y -= 15
        if y < 40:
            c.showPage()
            y = height - 40

    c.save()
    buffer.seek(0)
    return buffer

if st.session_state.ocr_text.strip():
    pdf_file = generate_pdf(st.session_state.ocr_text)
    st.download_button(
        label="⬇️ Download sebagai PDF",
        data=pdf_file,
        file_name="scantext_pro.pdf",
        mime="application/pdf"
    )

# ==========================
# FOOTER
# ==========================
st.markdown("---")
st.caption("© 2026 Nathans AI • ScanText Pro")

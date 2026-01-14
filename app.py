import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ==============================
# CONFIG
# ==============================
st.set_page_config(page_title="ScanText Pro", layout="centered")

st.title("📄 ScanText Pro")
st.caption("Aplikasi AI OCR untuk mengubah gambar menjadi teks")

# ==============================
# LOAD OCR (CACHE BIAR CEPAT)
# ==============================
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en', 'id'], gpu=False)

reader = load_reader()

# ==============================
# SESSION STATE
# ==============================
if "ocr_text" not in st.session_state:
    st.session_state.ocr_text = ""

# ==============================
# UPLOAD GAMBAR
# ==============================
uploaded_file = st.file_uploader(
    "Upload gambar",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Gambar yang diupload", use_column_width=True)

    if st.button("🔍 Baca Teks"):
        with st.spinner("Membaca teks dari gambar..."):
            result = reader.readtext(np.array(image), detail=0)
            st.session_state.ocr_text = "\n".join(result)

# ==============================
# HASIL OCR
# ==============================
st.subheader("Hasil Teks:")
text_result = st.text_area(
    "Teks hasil OCR",
    st.session_state.ocr_text,
    height=300
)

# ==============================
# DOWNLOAD KE TXT
# ==============================
if text_result.strip() != "":
    st.download_button(
        label="⬇️ Download TXT",
        data=text_result,
        file_name="scantext_result.txt",
        mime="text/plain"
    )

# ==============================
# DOWNLOAD KE PDF
# ==============================
def create_pdf(text):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    x = 40
    y = height - 40
    for line in text.split("\n"):
        if y < 40:
            c.showPage()
            y = height - 40
        c.drawString(x, y, line)
        y -= 14

    c.save()
    buffer.seek(0)
    return buffer

if text_result.strip() != "":
    pdf_file = create_pdf(text_result)

    st.download_button(
        label="⬇️ Download PDF",
        data=pdf_file,
        file_name="scantext_result.pdf",
        mime="application/pdf"
    )

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.caption("© 2026 ScanText Pro • Powered by AI OCR • Versi Demo")

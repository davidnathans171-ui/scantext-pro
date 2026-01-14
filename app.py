import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ===============================
# CONFIG
# ===============================
st.set_page_config(page_title="ScanText Pro", layout="centered")
st.title("📄 ScanText Pro")
st.caption("Aplikasi AI OCR untuk membaca dan mengedit teks dari gambar struk / dokumen")

# ===============================
# LOAD OCR (CACHE AGAR CEPAT)
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

# ===============================
# UPLOAD GAMBAR
# ===============================
uploaded_file = st.file_uploader(
    "Upload gambar",
    type=["png", "jpg", "jpeg"],
    help="Upload gambar struk, nota, atau dokumen"
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Gambar yang diupload", use_column_width=True)

    if st.button("🔍 Baca Teks"):
        with st.spinner("Membaca teks dari gambar..."):
            result = reader.readtext(np.array(image), detail=0)
            st.session_state.ocr_text = "\n".join(result)
        st.success("OCR selesai! Teks bisa diedit di bawah.")

# ===============================
# EDIT TEKS
# ===============================
st.subheader("📝 Hasil Teks (Bisa Diedit)")
edited_text = st.text_area(
    "Edit teks di bawah ini sesuai kebutuhan:",
    value=st.session_state.ocr_text,
    height=300
)

# Simpan hasil edit ke session
st.session_state.ocr_text = edited_text

# ===============================
# DOWNLOAD TXT
# ===============================
def generate_txt(text):
    return text.encode("utf-8")

st.download_button(
    label="⬇️ Download sebagai TXT",
    data=generate_txt(st.session_state.ocr_text),
    file_name="hasil_ocr.txt",
    mime="text/plain"
)

# ===============================
# DOWNLOAD PDF
# ===============================
def generate_pdf(text):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    x_margin = 40
    y_margin = height - 40
    y = y_margin

    for line in text.split("\n"):
        if y < 40:
            c.showPage()
            y = y_margin
        c.drawString(x_margin, y, line)
        y -= 14

    c.save()
    buffer.seek(0)
    return buffer

st.download_button(
    label="⬇️ Download sebagai PDF",
    data=g

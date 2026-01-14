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
st.set_page_config(
    page_title="ScanText Pro - Nathans AI",
    layout="centered"
)

# =========================
# LOGO + HEADER
# =========================
col1, col2 = st.columns([1, 4])
with col1:
    st.image("logo.png", width=90)
with col2:
    st.markdown("<h1>ScanText Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p><b>Powered by Nathans AI</b></p>", unsafe_allow_html=True)

st.caption(
    "Aplikasi AI OCR untuk mengubah gambar menjadi teks, bisa diedit, di-reset, "
    "scan dari kamera, dan di-download ke TXT / PDF"
)

st.divider()

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

if "image" not in st.session_state:
    st.session_state.image = None

# =========================
# AMBIL GAMBAR
# =========================
st.subheader("📸 Ambil Gambar")

tab1, tab2 = st.tabs(["📂 Upload Gambar", "📷 Kamera Langsung"])

with tab1:
    uploaded_file = st.file_uploader(
        "Upload gambar",
        type=["png", "jpg", "jpeg"]
    )
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.session_state.image = image
        st.image(image, caption="Gambar yang diupload", use_column_width=True)

with tab2:
    camera_image = st.camera_input("Ambil foto langsung dari kamera")
    if camera_image:
        image = Image.open(camera_image)
        st.session_state.image = image
        st.image(image, caption="Foto dari kamera", use_column_width=True)

# =========================
# OCR BUTTON
# =========================
if st.button("🔍 Baca Teks dari Gambar"):
    if st.session_state.image is None:
        st.warning("Silakan upload gambar atau ambil dari kamera dulu.")
    else:
        with st.spinner("Membaca teks dari gambar..."):
            result = reader.readtext(
                np.array(st.session_state.image),
                detail=0
            )
            st.session_state.ocr_text = "\n".join(result)
        st.success("OCR selesai!")

# =========================
# HASIL TEKS (BISA DIEDIT)
# =========================
st.subheader("✏️ Hasil Teks (Bisa Diedit)")

st.session_state.ocr_text = st.text_area(
    "Edit teks hasil OCR di sini:",
    value=st.session_state.ocr_text,
    height=250
)

# =========================
# TOMBOL RESET
# =========================
if st.button("🗑 Reset / Hapus Teks"):
    st.session_state.ocr_text = ""
    st.success("Teks berhasil dihapus.")

# =========================
# DOWNLOAD TXT
# =========================
if st.session_state.ocr_text.strip() != "":
    txt_data = st.session_state.ocr_text.encode("utf-8")

    st.download_button(
        label="⬇️ Download TXT",
        data=txt_data,
        file_name="scantext_pro_result.txt",
        mime="text/plain"
    )

# =========================
# DOWNLOAD PDF
# =========================
def generate_pdf(text):
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

if st.session_state.ocr_text.strip() != "":
    pdf_file = generate_pdf(st.session_state.ocr_text)

    st.download_button(
        label="⬇️ Download PDF",
        data=pdf_file,
        file_name="scantext_pro_result.pdf",
        mime="application/pdf"
    )

# =========================
# FOOTER
# =========================
st.divider()
st.markdown(
    "<center>© 2026 ScanText Pro • Powered by <b>Nathans AI</b></center>",
    unsafe_allow_html=True
)

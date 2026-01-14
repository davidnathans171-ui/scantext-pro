import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import io
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# =========================
# LOGO NATHANS AI
# =========================
logo_path = "logo.png"
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.image(logo, width=120)
else:
    st.warning("⚠️ Logo Nathans AI tidak ditemukan (logo.png)")

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="ScanText Pro", layout="centered")

st.title("📄 ScanText Pro")
st.caption("Aplikasi AI OCR untuk mengubah gambar menjadi teks, bisa diedit, dan di-download")

# =========================
# LOAD OCR (CACHE)
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
# INPUT MODE
# =========================
st.subheader("📸 Ambil Gambar")
mode = st.radio(
    "Pilih metode input gambar:",
    ["📂 Upload Gambar", "📷 Kamera Langsung"],
    horizontal=True
)

image = None

if mode == "📂 Upload Gambar":
    uploaded_file = st.file_uploader(
        "Upload gambar",
        type=["png", "jpg", "jpeg"]
    )
    if uploaded_file:
        image = Image.open(uploaded_file)

elif mode == "📷 Kamera Langsung":
    camera_image = st.camera_input("Ambil gambar langsung dari kamera")
    if camera_image:
        image = Image.open(camera_image)

# =========================
# TAMPILKAN GAMBAR
# =========================
if image:
    st.session_state.image = image
    st.image(image, caption="Gambar yang digunakan", use_column_width=True)

# =========================
# OCR BUTTON
# =========================
if st.button("🔍 Baca Teks dari Gambar"):
    if st.session_state.image is None:
        st.warning("⚠️ Silakan upload gambar atau ambil dari kamera terlebih dahulu.")
    else:
        with st.spinner("Membaca teks dari gambar..."):
            result = reader.readtext(np.array(st.session_state.image), detail=0)
            st.session_state.ocr_text = "\n".join(result)
        st.success("✅ OCR selesai!")

# =========================
# EDITABLE TEXT
# =========================
st.subheader("✏️ Hasil Teks (Bisa Diedit)")
edited_text = st.text_area(
    "Edit teks hasil OCR di sini:",
    value=st.session_state.ocr_text,
    height=250
)
st.session_state.ocr_text = edited_text

# =========================
# RESET BUTTON
# =========================
if st.button("🗑️ Reset / Hapus Semua"):
    st.session_state.ocr_text = ""
    st.session_state.image = None
    st.success("🧹 Data berhasil di-reset. Refresh halaman jika perlu.")

# =========================
# DOWNLOAD TXT
# =========================
st.subheader("⬇️ Download Hasil")

if st.session_state.ocr_text.strip() != "":
    txt_bytes = st.session_state.ocr_text.encode("utf-8")
    st.download_button(
        label="📄 Download TXT",
        data=txt_bytes,
        file_name="scantext_result.txt",
        mime="text/plain"
    )

    # =========================
    # DOWNLOAD PDF
    # =========================
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    textobject = c.beginText(40, 800)

    for line in st.session_state.ocr_text.split("\n"):
        textobject.textLine(line)

    c.drawText(textobject)
    c.showPage()
    c.save()

    pdf_bytes = buffer.getvalue()
    buffer.close()

    st.download_button(
        label="📕 Download PDF",
        data=pdf_bytes,
        file_name="scantext_result.pdf",
        mime="application/pdf"
    )
else:
    st.info("📌 Belum ada teks untuk di-download.")

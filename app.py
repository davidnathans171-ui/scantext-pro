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
st.caption("Aplikasi AI OCR untuk mengubah gambar menjadi teks dan mengedit hasilnya")

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
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Gambar yang diupload", use_column_width=True)

    if st.button("🔍 Baca Teks dari Gambar"):
        with st.spinner("Membaca teks dari gambar..."):
            result = reader.readtext(np.array(image), detail=0)
            st.session_state.ocr_text = "\n".join(result)
        st.success("OCR selesai!")

# ===============================
# HASIL OCR (EDITABLE)
# ===============================
st.subheader("✏️ Hasil Teks (Bisa Diedit)")
st.session_state.ocr_text = st.text_area(
    "Edit teks hasil OCR di sini:",
    st.session_state.ocr_text,
    height=250
)

# ===============================
# DOWNLOAD BUTTON
# ===============================
if st.session_state.ocr_text.strip() != "":
    st.subheader("⬇️ Download Hasil")

    col1, col2 = st.columns(2)

    # --- Download TXT ---
    with col1:
        st.download_button(
            label="⬇️ Download TXT",
            data=st.session_state.ocr_text,
            file_name="hasil_ocr.txt",
            mime="text/plain"
        )

    # --- Download PDF ---
    with col2:
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=A4)
        textobject = c.beginText(40, 800)

        for line in st.session_state.ocr_text.split("\n"):
            textobject.textLine(line)

        c.drawText(textobject)
        c.showPage()
        c.save()
        pdf_buffer.seek(0)

        st.download_button(
            label="⬇️ Download PDF",
            data=pdf_buffer,
            file_name="hasil_ocr.pdf",
            mime="application/pdf"
        )

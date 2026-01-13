import io
import streamlit as st
from PIL import Image
import easyocr
import numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# OCR Reader
reader = easyocr.Reader(['en', 'id'])

# Page config
st.set_page_config(page_title="ScanText Pro", layout="centered")

st.title("📄 ScanText Pro")
st.caption("Aplikasi AI OCR untuk mengubah gambar menjadi teks")

# Upload gambar
uploaded_file = st.file_uploader("Upload gambar", type=["png", "jpg", "jpeg"])

text_result = ""

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Gambar yang diupload", use_column_width=True)

    if st.button("Baca Teks"):
        with st.spinner("Membaca teks dari gambar..."):
            result = reader.readtext(np.array(image), detail=0)
            text_result = "\n".join(result)

# Tampilkan hasil
st.subheader("Hasil Teks:")
text_area = st.text_area("", text_result, height=300)

# =======================
# DOWNLOAD KE TXT
# =======================
if text_area:
    txt_bytes = text_area.encode("utf-8")
    st.download_button(
        label="⬇️ Download sebagai .TXT",
        data=txt_bytes,
        file_name="hasil_ocr.txt",
        mime="text/plain"
    )

# =======================
# DOWNLOAD KE PDF
# =======================
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

    pdf_buffer = create_pdf(text_area)

    st.download_button(
        label="⬇️ Download sebagai .PDF",
        data=pdf_buffer,
        file_name="hasil_ocr.pdf",
        mime="application/pdf"
    )

st.markdown("---")
st.caption("© 2026 ScanText Pro • Powered by AI OCR • Versi Demo")

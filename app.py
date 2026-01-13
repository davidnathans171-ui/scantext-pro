import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import streamlit as st
from PIL import Image
import easyocr
import numpy as np

reader = easyocr.Reader(['en','id'])

st.set_page_config(page_title="ScanText Pro", layout="centered")

st.title("📄 ScanText Pro")
st.caption("Aplikasi AI OCR untuk mengubah gambar menjadi teks")

uploaded_file = st.file_uploader("Upload gambar", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Gambar yang diupload", use_column_width=True)

    if st.button("🔍 Baca Teks"):
        with st.spinner("Membaca teks dari gambar..."):
            result = reader.readtext(np.array(image), detail=0)
            text = "\n".join(result)

        st.subheader("Hasil Teks:")
        st.text_area("", text, height=300)

        # ======================
        # DOWNLOAD KE TXT
        # ======================
        txt_data = text.encode("utf-8")
        st.download_button(
            label="⬇️ Download sebagai TXT",
            data=txt_data,
            file_name="hasil_ocr.txt",
            mime="text/plain"
        )

        # ======================
        # DOWNLOAD KE PDF
        # ======================
        def create_pdf(text):
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=A4)
            width, height = A4
            x = 40
            y = height - 40

            for line in text.split("\n"):
                c.drawString(x, y, line)
                y -= 14
                if y < 40:
                    c.showPage()
                    y = height - 40

            c.save()
            buffer.seek(0)
            return buffer

        pdf_file = create_pdf(text)

        st.download_button(
            label="⬇️ Download sebagai PDF",
            data=pdf_file,
            file_name="hasil_ocr.pdf",
            mime="application/pdf"
        )

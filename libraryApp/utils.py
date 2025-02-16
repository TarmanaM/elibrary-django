import fitz  # PyMuPDF
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from .models import BookPage

def convert_pdf_to_images(book):
    """Mengonversi PDF menjadi gambar dan menyimpannya sebagai BookPage."""
    if not book.pdf_file:
        return
    
    pdf_path = book.pdf_file.path
    doc = fitz.open(pdf_path)

    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        img_io = BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)

        # Simpan gambar sebagai BookPage
        book_page = BookPage(book=book, page_number=page_number + 1)
        book_page.image.save(f'book_{book.id}_page_{page_number + 1}.png', ContentFile(img_io.getvalue()), save=True)

from django.db import models
import fitz  # PyMuPDF
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image
import os
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.CharField(max_length=100)
    published_year = models.IntegerField()
    total_pages = models.IntegerField()
    is_favorite = models.BooleanField(default=False)  # Untuk fitur favorit
    created_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='books/pdfs/',default='default.pdf')

    def __str__(self):
        return self.title
    
    def convert_pdf_to_images(self):
        """Mengonversi PDF menjadi gambar dan menyimpannya sebagai BookPage."""
        if not self.pdf_file:
            return
        
        pdf_path = self.pdf_file.path
        doc = fitz.open(pdf_path)

        for page_number in range(len(doc)):
            page = doc.load_page(page_number)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            img_io = BytesIO()
            img.save(img_io, format='PNG')
            img_io.seek(0)

            # Simpan gambar sebagai BookPage
            book_page = BookPage(book=self, page_number=page_number + 1)
            book_page.image.save(f'book_{self.id}_page_{page_number + 1}.png', ContentFile(img_io.getvalue()), save=True)
    def delete(self, *args, **kwargs):
        """Hapus file PDF dan semua gambar sebelum menghapus objek buku."""
        
        # Hapus semua file gambar dari book_pages/
        for page in self.pages.all():
            if page.image:
                image_path = os.path.join(settings.MEDIA_ROOT, page.image.name)
                if os.path.exists(image_path):
                    os.remove(image_path)

        # Hapus file PDF jika ada
        if self.pdf_file:
            pdf_path = os.path.join(settings.MEDIA_ROOT, self.pdf_file.name)
            if os.path.exists(pdf_path):
                os.remove(pdf_path)

        # Hapus objek buku dari database
        super().delete(*args, **kwargs)


class BookPage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="pages")
    image = models.ImageField(upload_to="book_pages/")
    page_number = models.PositiveIntegerField()

    class Meta: 
        ordering = ["page_number"]

    def __str__(self):
        return f"{self.book.title} - Page {self.page_number}"



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="profile_pics/", default="profile_pics/default.jpg")

    def __str__(self):
        return f"Profile of {self.user.username}"

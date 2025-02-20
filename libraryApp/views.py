from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .models import Book, BookPage
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password

from .forms import CustomPasswordChangeForm

from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Book
import os
from django.conf import settings
from .utils import convert_pdf_to_images 


def home(request):
    
    return render(request, 'libraryApp/home.html')




def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("home")  # Redirect ke katalog setelah login
        else:
            messages.error(request, "Email atau password salah!")

    return render(request, "libraryApp/login.html")

def user_register(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request, "Password dan Konfirmasi Password tidak cocok!")
        elif len(password) < 8:
            messages.error(request, "Password minimal 8 karakter!")
        elif not any(char.isupper() for char in password):
            messages.error(request, "Password harus mengandung huruf besar!")
        elif not any(char.islower() for char in password):
            messages.error(request, "Password harus mengandung huruf kecil!")
        elif not any(char.isdigit() for char in password):
            messages.error(request, "Password harus mengandung angka!")
        else:
            if User.objects.filter(username=email).exists():
                messages.error(request, "Email sudah terdaftar!")
            else:
                user = User.objects.create_user(username=email, email=email, password=password)
                messages.success(request, "Akun berhasil dibuat! Silakan login.")
                return redirect("login")

    return render(request, "libraryApp/register.html")

@login_required
def catalog(request):
    filter_favorite = request.GET.get('favorite', 'all')
    books = Book.objects.all().prefetch_related("pages")

    if filter_favorite == 'yes':
        books = books.filter(is_favorite=True)

    for book in books:
        book.cover_page = book.pages.first()  # Ambil halaman pertama

    paginator = Paginator(books, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'libraryApp/catalog.html', {'page_obj': page_obj, 'filter_favorite': filter_favorite})



@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Anda telah keluar.")
    return redirect('login')

@login_required
def search_view(request):
    query = request.GET.get('q')
    books = Book.objects.all()
    
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(published_year__icontains=query)
        )
        for book in books:
            book.cover_page = book.pages.first()  # Ambil halaman pertama
    

    paginator = Paginator(books, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'libraryApp/catalog.html', {'page_obj': page_obj, 'query': query})

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST" and "analyze" in request.POST:
        book.analyze_keywords()
    cover_page = book.pages.first()  # Ambil halaman pertama sebagai cover
    return render(request, 'libraryApp/book_detail.html', {'book': book, 'cover_page': cover_page})



@login_required
def toggle_favorite(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.is_favorite = not book.is_favorite
    book.save()
    
    if book.is_favorite:
        messages.success(request, f'"{book.title}" ditambahkan ke Favorit!')
    else:
        messages.warning(request, f'"{book.title}" dihapus dari Favorit.')

    return redirect('catalog')

@login_required
def book_preview_view(request, book_id, page_number):
    book = get_object_or_404(Book, id=book_id)
    page = BookPage.objects.filter(book=book, page_number=page_number).first()
    next_page = None 
    if not page:
        return render(request, '404.html', status=404)  # Bisa pakai template 404 sendiri

    prev_page = page_number - 1 if page_number > 1 else None
    if BookPage.objects.filter(book=book, page_number=page_number + 1).exists():
        next_page = page_number + 1
    return render(request, 'libraryApp/book_preview.html', {
        'book': book,
        'page': page,
        'prev_page': prev_page,
        'next_page': next_page
    })
@login_required
def upload_book(request):
    if request.method == "POST" and request.FILES.get("pdf_file"):
        title = request.POST["title"]
        author = request.POST["author"]
        description = request.POST["description"]
        genre = request.POST["genre"]
        published_year = request.POST["published_year"]
        total_pages = request.POST["total_pages"]
        pdf_file = request.FILES["pdf_file"]

        # Simpan buku ke database
        book = Book.objects.create(
            title=title,
            author=author,
            description=description,
            genre=genre,
            published_year=published_year,
            total_pages=total_pages,
            pdf_file=pdf_file
        )

        # Konversi PDF ke gambar setelah upload selesai
        convert_pdf_to_images(book)

        return redirect("catalog")  # Redirect ke halaman daftar buku

    return render(request, "libraryApp/upload_book.html")
@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.description = request.POST.get("description")
        book.genre = request.POST.get("genre")
        book.published_year = request.POST.get("published_year")
        book.total_pages = request.POST.get("total_pages")

        # Hapus file PDF lama jika user upload PDF baru
        if "pdf_file" in request.FILES:
            if book.pdf_file:  # Jika ada file lama
                old_pdf_path = os.path.join(settings.MEDIA_ROOT, book.pdf_file.name)
                if os.path.exists(old_pdf_path):
                    os.remove(old_pdf_path)  # Hapus file lama

            book.pdf_file = request.FILES["pdf_file"]

            # Hapus semua gambar lama hasil konversi
            for page in book.pages.all():
                if page.image:
                    image_path = os.path.join(settings.MEDIA_ROOT, page.image.name)
                    if os.path.exists(image_path):
                        os.remove(image_path)  # Hapus file gambar
            book.pages.all().delete() 

        book.save()

        # Konversi PDF ke gambar jika ada file baru
        if "pdf_file" in request.FILES:
            book.convert_pdf_to_images()

        messages.success(request, "Buku berhasil diperbarui!")
        return redirect("catalog")

    return render(request, "libraryApp/edit_book.html", {"book": book})
@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == "POST":
        book.delete()  # Panggil metode delete() yang kita buat
        messages.success(request, "Buku berhasil dihapus.")
        return redirect("catalog")  # Redirect ke halaman katalog buku
    
    return redirect("book_detail", book_id=book.id)





@login_required
def profile_views(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'libraryApp/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        photo = request.FILES.get("photo")

        request.user.first_name = name
        request.user.email = email
        request.user.save()

        if photo:
            profile.photo = photo
            profile.save()
        
        messages.success(request, "Profil berhasil diperbarui!")
        return redirect("profile")

    return render(request, "libraryApp/edit_profile.html", {"profile": profile})



@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, "libraryApp/profile.html", {"profile": profile})



@login_required
def profile_view(request):
    if request.method == "POST":
        if "update_profile" in request.POST:
            request.user.username = request.POST.get("username")
            request.user.email = request.POST.get("email")
            if "photo" in request.FILES:
                request.user.profile.photo = request.FILES["photo"]
            request.user.save()
            messages.success(request, "Profil berhasil diperbarui!")

        elif "change_password" in request.POST:
            old_password = request.POST.get("old_password")
            new_password1 = request.POST.get("new_password1")
            new_password2 = request.POST.get("new_password2")

            if not check_password(old_password, request.user.password):
                messages.error(request, "Password lama salah!")
            elif new_password1 != new_password2:
                messages.error(request, "Password baru tidak cocok!")
            else:
                request.user.set_password(new_password1)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "Password berhasil diubah!")

        return redirect("profile")

    return render(request, "libraryApp/profile.html")


@login_required
def favorite_books_view(request):
    books = Book.objects.filter(is_favorite=True).prefetch_related("pages")

    for book in books:
        book.cover_page = book.pages.first()  # Ambil halaman pertama

    paginator = Paginator(books, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "libraryApp/favorites.html", {"page_obj": page_obj})
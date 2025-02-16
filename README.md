# 📚 e-Library

e-Library adalah sistem perpustakaan digital berbasis Django yang mendukung:
- Manajemen buku (unggah, edit, hapus)
- Sistem favorit
- Konversi PDF ke gambar otomatis
- Profil pengguna dengan fitur edit & ubah password


## 🚀 Cara Menjalankan Proyek

### 1️⃣ Clone Repository
```
git clone https://github.com/TarmanaM/e-library.git
cd e-library

```
### 2️⃣ Buat virtual environment(Optional)
```
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows
```
### 3️⃣ Instal Dependensi
```
pip install -r requirements.txt
```
### 4️⃣ Konfigurasi Database
```
python manage.py migrate
```
### 5️⃣ Buat Superuser (Opsional)
```
python manage.py createsuperuser
```
 
### 6️⃣ Jalankan Server
```
python manage.py runserver
```
Buka di browser: http://127.0.0.1:8000/

## 🔧 Teknologi yang Digunakan
Python 3.12
Django 5.1
Bootstrap 5
PyMuPDF (untuk konversi PDF ke gambar)
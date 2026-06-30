# Pengembangan Sistem Portofolio Berbasis Web

Aplikasi portofolio web ini adalah sebuah sistem yang menyajikan profil, keahlian, pengalaman, proyek, dan formulir kontak secara dinamis. Sistem ini dilengkapi dengan panel admin untuk melakukan operasi CRUD dan integrasi upload gambar serta notifikasi email.

## Fitur Utama

- Admin CRUD untuk mengelola profil, skill, pengalaman, dan proyek.
- Halaman publik yang menampilkan data portofolio secara dinamis.
- Integrasi Cloudinary untuk upload gambar proyek dan profil.
- Integrasi Resend untuk mengirim notifikasi email dari formulir kontak.
- Autentikasi admin sederhana menggunakan session Flask.

## Teknologi yang Digunakan

- Python
- Flask
- Flask-SQLAlchemy
- TiDB / MySQL (via PyMySQL)
- Cloudinary
- Resend
- HTML, CSS, JavaScript

## Struktur Proyek

- pp.py: Entry point aplikasi Flask.
- config.py: Memuat konfigurasi environment dan database.
- model.py: Definisi model ORM untuk tabel database.
- Backend/: Logika backend untuk admin dan halaman utama.
- Frontend/: Template dan aset frontend untuk admin dan publik.

## Langkah Instalasi

1. Clone repository:
   `ash
   git clone <repo_url>
   cd Portofolio_Tugas
   `

2. Buat virtual environment:
   `ash
   python -m venv venv
   `

3. Aktifkan virtual environment:
   - Windows PowerShell:
     `powershell
     .\venv\Scripts\Activate.ps1
     `
   - Command Prompt:
     `cmd
     .\venv\Scripts\activate.bat
     `
   - macOS/Linux:
     `ash
     source venv/bin/activate
     `

4. Install dependencies:
   `ash
   pip install -r requirements.txt
   `

5. Siapkan variabel lingkungan:
   - Salin file .env.example ke .env.
   - Isi nilai konfigurasi seperti database, Cloudinary, dan Resend.

6. Jalankan aplikasi:
   `ash
   python app.py
   `

7. Akses aplikasi di browser:
   - Public: http://127.0.0.1:5000/
   - Admin login: http://127.0.0.1:5000/login

## Kredensial Default Admin

- Username: dmin
- Password: dmin123

## Catatan

- Pastikan file .env tidak dibagikan ke publik.
- Jika menggunakan database lokal, sesuaikan SQLALCHEMY_DATABASE_URI di .env.
- Gunakan kredensial default hanya untuk pengujian. Ganti password sebelum deploy.

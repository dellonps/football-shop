
1. Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial)?

    Aku mengimplementasikan proyek Django dengan mengikuti checklist, tapi tidak hanya sekadar menyalin dari tutorial. Berikut langkah-langkahku sendiri:

    1. Inisialisasi Proyek

    - Membuat proyek Django baru dengan django-admin startproject football_shop.
    - Menyiapkan virtual environment (python -m venv env) dan menginstal dependensi dari requirements.txt.

    2. Pembuatan App

    - Membuat app utama dengan python manage.py startapp main.
    - Mendaftarkannya ke INSTALLED_APPS di settings.py.

    3. Routing URL

    - Menambahkan urls.py di dalam app main.
    - Mengonfigurasi football_shop/urls.py agar menyertakan route dari app main.

    4. Views dan Template

    - Membuat fungsi di views.py untuk menangani request
    - Membuat HTML template di dalam main/templates/main/.

    5. Model dan Database

    - Mendesain model di models.py.
    - Menjalankan migrasi dengan python manage.py makemigrations dan python manage.py migrate.
    - Mengecek perubahan database lewat Django admin panel.

    6. Static Files & Whitenoise

    - Mengonfigurasi static files untuk deployment dan mengaktifkan Whitenoise middleware agar bisa menyajikannya.

    7. Deployment ke PWS

    - Menambahkan requirements.txt.
    - Push proyek ke remote GitLab PWS (git push pws main:master).
    - Memperbaiki error dengan memastikan semua file proyek (termasuk requirements.txt) sudah ditrack Git.

2. Buatlah bagan yang berisi request client ke web aplikasi berbasis Django beserta responnya dan jelaskan pada bagan tersebut kaitan antara urls.py, views.py, models.py, dan berkas html !
   
    1. Alur request–response di Django:
    2. Client mengirim request lewat browser.
    3. urls.py mencari pola URL yang cocok.
    4. Request diteruskan ke views.py yang mengatur logika.
    5. Jika perlu data, views.py memanggil models.py untuk akses database.
    6. Data dari views diteruskan ke template HTML.
    7. Hasil render HTML dikirim kembali ke client sebagai response.

3. Jelaskan peran settings.py dalam proyek Django?
   settings.py merupakan berkas konfigurasi utama pada proyek Django yang berfungsi untuk menyimpan seluruh pengaturan penting yang dibutuhkan agar aplikasi dapat berjalan dengan baik. File ini pertama kali dibaca setiap kali server Django dijalankan, sehingga dapat dikatakan bahwa settings.py adalah pusat konfigurasi dari proyek Django.

   1. Beberapa peran penting dari settings.py antara lain:
   2. Mengatur aplikasi yang digunakan
   3. Mengatur koneksi database
   4. Mengatur keamanan dan akses host
   5. Mengatur lokasi template dan static files
   6. Mengatur konfigurasi tambahan


4.  Bagaimana cara kerja migrasi database di Django?
    1. Buat perubahan model di models.py ?

    2. Jalankan,python manage.py makemigrations


    3. Django membuat file migrasi yang mendeskripsikan perubahan database    Jalankan, python manage.py migrate


    4. Django mengeksekusi migrasi ke database → membuat tabel, menambahkan kolom, dsb.




5. Menurut Anda, dari semua framework yang ada, mengapa framework Django dijadikan permulaan pembelajaran pengembangan perangkat lunak?

    Saat pertama kali belajar Django, saya merasa framework ini cukup lengkap . Beberapa impresi pertama saya:

    1. Full-stack dan terstruktur, saya bisa melihat jelas alur antara models, views, dan templates. Rasanya seperti punya panduan bawaan untuk membangun aplikasi web yang rapi. 
    2. Mudah dipahami untuk pemula, dokumentasinya jelas dan banyak contoh. Walaupun awalnya banyak istilah baru, tapi saya bisa mengikuti tutorial dan langsung melihat hasilnya di browser.
    3. Struktur proyek standar, folder dan file di Django sudah terorganisir dengan baik. Ini membantu saya belajar best practices sejak awal, misalnya cara menaruh templates, static files, dan apps.
    4. Cepat melihat hasil, dalam waktu singkat saya bisa membuat halaman web yang berjalan, bahkan menampilkan data dari model Product di tugas Football Shop. Rasanya menyenangkan karena bisa langsung melihat “apa yang saya tulis = apa yang muncul di browser”.
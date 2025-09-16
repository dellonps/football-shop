
TUGAS 3

1. Mengapa kita memerlukan data delivery dalam pengimplementasian platform?

    Data delivery diperlukan agar informasi dapat berpindah dari satu pihak ke pihak lain dengan format yang konsisten dan dapat dipahami. Dalam konteks platform, data delivery memastikan komunikasi antara server, database, dan client berjalan lancar. Tanpa mekanisme ini, pengguna tidak akan bisa menerima data yang diminta (misalnya menampilkan daftar produk atau berita). Jadi, data delivery adalah jembatan utama agar sistem dapat berfungsi dengan baik.

2. Mana yang lebih baik antara XML dan JSON? Mengapa JSON lebih populer dibandingkan XML?
     
     Secara umum, JSON lebih baik digunakan dibandingkan XML untuk kebutuhan web modern. JSON lebih ringkas, lebih mudah dibaca oleh manusia, dan lebih mudah diproses oleh bahasa pemrograman karena strukturnya mirip dengan object/array di banyak bahasa (seperti JavaScript dan Python). Sementara XML lebih verbose (panjang karena banyak tag), sehingga kurang efisien.
     JSON lebih populer dibandingkan XML karena:

        1. Lebih ringan dan cepat diparsing.
        2. Sudah terintegrasi secara natural dengan JavaScript.
        3. Lebih mudah dipahami developer, terutama di era API dan web modern.

3. Fungsi dari method is_valid() pada form Django dan mengapa kita membutuhkannya?

    Method is_valid() digunakan untuk memvalidasi data input yang dikirimkan melalui form. Django akan memeriksa apakah data sudah sesuai dengan aturan yang didefinisikan (misalnya format email benar, field wajib diisi, dll).

    Kita membutuhkan method ini agar data yang masuk ke server aman dan bersih, sehingga mencegah error maupun potensi penyalahgunaan. Dengan begitu, hanya data valid yang diproses lebih lanjut, misalnya untuk disimpan ke database.

4. Mengapa kita membutuhkan csrf_token saat membuat form di Django?
    csrf_token diperlukan untuk melindungi aplikasi dari serangan Cross-Site Request Forgery (CSRF). Tanpa token ini, seorang penyerang bisa membuat form palsu di luar aplikasi kita, lalu mengarahkan pengguna agar secara tidak sadar mengirimkan request berbahaya ke server kita (misalnya mengganti password atau melakukan transaksi).

    Dengan adanya csrf_token, setiap form hanya akan dianggap sah jika membawa token unik yang cocok dengan server. Jika tidak, request ditolak. Hal ini mencegah manipulasi request dari pihak luar.

5. Bagaimana cara saya mengimplementasikan checklist di atas secara step-by-step?

    1. Ringkasan yang saya tambahkan:
        1. Empat endpoint data untuk mengembalikan produk dalam format XML dan JSON:

            ~ /api/products/json/ → semua produk (JSON)
            ~ /api/products/xml/ → semua produk (XML)
            ~ /api/products/json/<id>/ → satu produk berdasarkan id (JSON)
            ~ /api/products/xml/<id>/ → satu produk berdasarkan id (XML)

        2. Halaman HTML:

            ~ Halaman daftar produk yang menampilkan semua produk dengan tombol "Add" dan "tautan Detail" untuk tiap produk.
            ~ Halaman tambah produk dengan form untuk membuat produk baru.
            ~ Halaman detail produk yang menampilkan data lengkap dari satu produk.

        3. Formulir:

            ~ ProductForm (main/forms.py) dibuat dengan ModelForm agar validasi dan penyimpanan data lebih mudah.

        4. Routing:

            ~ Pola URL ditambahkan pada main/urls.py untuk halaman HTML dan endpoint API.
            ~ Proyek football_shop/urls.py menyertakan URL dari app main.

        5. Validasi & keamanan:

            ~ Form tambah produk menggunakan form.is_valid() untuk memvalidasi input sebelum menyimpan data.

            ~ Template menggunakan {% csrf_token %} untuk melindungi permintaan POST.

    2. File yang saya buat atau edit

        1. main/forms.py — ProductForm (ModelForm)
        2. main/views.py — ditambahkan:
            - api_products_json, api_products_xml, api_product_json, api_product_xml (menggunakan django.core.serializers.serialize() untuk output XML/JSON)
            - product_list, product_detail, product_add (views untuk HTML)
        3. main/urls.py — ditambahkan routing untuk API + halaman
        4. main/templates/main/product_list.html — menampilkan daftar produk + tombol Add + tautan Detail
        5. main/templates/main/product_form.html — form untuk tambah produk (menggunakan {% csrf_token %})
        6. main/templates/main/product_detail.html — menampilkan detail dari satu produk

    3. Catatan implementasi & keputusan kecil:

        Saya menggunakan Django serializers (serializers.serialize("json", queryset)) agar output JSON/XML sederhana dan konsisten. Cara ini cepat untuk proyek kecil dan memastikan nama field sama dengan field model. Untuk form HTML tambah produk, saya menggunakan ModelForm dari tutorial kedua sehingga validasi dan penyimpanan lebih mudah dilakukan.



6. Feedback untuk asdos tutorial 2
    
    Menurut saya, asisten dosen sudah cukup jelas dalam memberikan penjelasan.






![xml](image.png)
![json](image-1.png)
![json by id]((image-2.png))
![xml by id](image-3.png)




TUGAS 2

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
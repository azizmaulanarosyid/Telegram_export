# Telegram_export
Telegram Export adalah aplikasi Python yang memungkinkan pengguna untuk mengekspor pesan dari grup Telegram ke dalam format file Excel (.xlsx). Aplikasi ini memanfaatkan pustaka Telethon untuk berinteraksi dengan API Telegram dan pandas untuk memproses dan menyimpan data dalam bentuk spreadsheet.

# Fitur
Ekspor pesan berdasarkan tanggal dan waktu yang ditentukan.

Mendukung pemilihan grup Telegram yang ingin diekspor.

Menghasilkan file Excel dengan struktur kolom yang jelas dan teratur.

Antarmuka pengguna grafis sederhana menggunakan Tkinter.

# Persyaratan
Sebelum menjalankan aplikasi, pastikan Anda telah memenuhi persyaratan berikut:
Python 3.x

Pustaka yang diperlukan:
pandas,
telethon,
tkinter,
tkcalendar,
pytz

Anda dapat menginstal pustaka yang diperlukan dengan menjalankan perintah berikut:

pip install pandas telethon tkcalendar pytz


# Cara Menggunakan
# 1. Konfigurasi API Telegram:

Dapatkan api_id dan api_hash dari Telegram API.

Gantilah nilai api_id, api_hash, dan phone pada kode dengan informasi Anda.

# 2. Menjalankan Aplikasi:

Setelah mengkonfigurasi kode, jalankan aplikasi dengan perintah:

python telegram_export.py

Antarmuka pengguna akan muncul.

# 3. Mengisi Data:

Masukkan nama grup Telegram yang ingin diekspor.

Pilih tanggal dan jam yang diinginkan.

Klik tombol "Ekspor".

# 4. Hasil:

File Excel akan dihasilkan dan disimpan di direktori kerja Anda dengan nama yang unik.


# Struktur Kode
Fungsi Utama:

export_telegram_messages: Menangani logika utama untuk mengekspor pesan.

process_message_batch: Memproses batch pesan dari Telegram.

export_messages_to_excel: Menyimpan data pesan ke file Excel.

# Antarmuka Pengguna:

Dibangun menggunakan Tkinter, memungkinkan pengguna untuk menginput data dengan mudah.


# Contoh Penggunaan
Berikut adalah contoh penggunaan untuk mengekspor pesan dari grup Telegram:

# Konfigurasi API Telegram
api_id = '123456'
api_hash = 'your_api_hash'
phone = '+628123456789'

# Lisensi
Proyek ini dilisensikan di bawah MIT License.

# Kontribusi
Silakan ajukan pull request atau buka isu jika Anda ingin berkontribusi pada proyek ini.

# Kontak
Jika Anda memiliki pertanyaan atau masukan, silakan hubungi saya di [azizmaulanarosyid@gmail.com].


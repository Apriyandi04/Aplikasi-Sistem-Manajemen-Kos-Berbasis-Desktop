# rillKos - Sistem Manajemen Kos

rillKos adalah aplikasi desktop berbasis Python dan PyQt6 yang dirancang untuk memudahkan manajemen rumah kos. Aplikasi ini menyediakan solusi komprehensif untuk pemilik kos (Admin) dalam mengelola kamar, penghuni, pembayaran, dan keluhan, serta memberikan akses kepada penghuni (User) untuk melihat informasi dan berinteraksi dengan pengelola.

## 📋 Fitur Utama

### 👑 Admin
*   **Dashboard**: Ringkasan status kos secara real-time.
*   **Manajemen Kamar**: Tambah, edit, hapus, dan pantau status kamar (kosong/terisi) beserta fasilitas dan harga.
*   **Manajemen Penghuni**: Kelola data penghuni, tanggal masuk, dan penempatan kamar.
*   **Keuangan & Pembayaran**: Pantau status pembayaran bulanan, konfirmasi bukti bayar, dan riwayat transaksi.
*   **Keluhan**: Terima dan tanggapi keluhan dari penghuni.

### 👤 Penghuni (User)
*   **Dashboard Personal**: Informasi status kamar dan tagihan.
*   **Pembayaran**: Upload bukti pembayaran bulanan.
*   **Keluhan**: Ajukan keluhan terkait fasilitas atau layanan kos dan lihat tanggapan admin.
*   **Profil**: Lihat dan kelola data diri.

## 🛠️ Teknologi yang Digunakan

*   **Bahasa Pemrograman**: Python 3.x
*   **GUI Framework**: PyQt6 (Python Qt bindings)
*   **Database**: SQLite
*   **Styling**: QSS (Qt Style Sheets)

## 📂 Struktur Project

```
rillKos/
├── assets/             # Asset gambar dan file style (style.qss)
├── views/              # File tampilan (UI) untuk Login, Admin, User
│   ├── login.py
│   ├── admin_window.py
│   ├── user_window.py
│   └── ...
├── database.py         # Skrip inisialisasi dan manajemen database SQLite
├── main.py             # Titik masuk (Entry point) aplikasi
├── components.py       # Komponen UI reusable
├── kos_management.db   # File database (otomatis dibuat)
└── README.md           # Dokumentasi proyek
```

## 🚀 Instalasi dan Cara Penggunaan

### Prasyarat
Pastikan Python 3 sudah terinstal di komputer Anda. Disarankan menggunakan virtual environment.

### Langkah-langkah

1.  **Clone Repository**
    ```bash
    git clone https://github.com/username/rillKos.git
    cd rillKos
    ```

2.  **Install Dependencies**
    Install paket yang dibutuhkan (terutama PyQt6):
    ```bash
    pip install PyQt6
    ```

3.  **Jalankan Aplikasi**
    Eksekusi file `main.py` untuk memulai aplikasi:
    ```bash
    python main.py
    ```

### 🔑 Akun Default (Untuk Testing)

Saat pertama kali dijalankan, aplikasi akan membuat database dengan akun default berikut:

*   **Admin**
    *   Username: `admin`
    *   Password: `admin123`
*   **User**
    *   Username: `user`
    *   Password: `user123`

## 👥 Kontribusi

Kontribusi selalu diterima! Silakan buat *pull request* untuk perbaikan bug atau penambahan fitur baru.

---
Dibuat dengan ❤️ oleh Tim Pengembang rillKos.

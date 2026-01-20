import sqlite3

import os
import sys

# Determine the base path: executable location if frozen, else script location
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_FILE = os.path.join(BASE_DIR, "kos_management.db")

def query_db(query, params=(), fetch=False):
    # Fungsi pembantu untuk mengeksekusi perintah SQL ke SQLite.
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        data = cursor.fetchall() if fetch else None
        conn.commit()
        return data
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Tabel User
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (username TEXT PRIMARY KEY, password TEXT, role TEXT, email TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS session
                      (id INTEGER PRIMARY KEY CHECK (id = 1), user TEXT, pw TEXT)''')
    
    # Cek apakah user admin sudah ada, jika belum buat akun default
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users VALUES ('admin', 'admin123', 'admin', 'admin@kos.com')")
        cursor.execute("INSERT INTO users VALUES ('user', 'user123', 'user', 'user@gmail.com')")
    
    conn.commit()
    conn.close()

def init_business_db():
    query_db('''CREATE TABLE IF NOT EXISTS kamar
                (id INTEGER PRIMARY KEY AUTOINCREMENT, no_kamar TEXT,
                kapasitas TEXT, harga INTEGER, status TEXT, fasilitas TEXT)''')
    
    query_db('''CREATE TABLE IF NOT EXISTS penghuni
                (id INTEGER PRIMARY KEY AUTOINCREMENT, nama TEXT, nik TEXT,
                hp TEXT, kamar_no TEXT, username TEXT, tgl_masuk TEXT)''')
    
    query_db('''CREATE TABLE IF NOT EXISTS pembayaran
                (id INTEGER PRIMARY KEY AUTOINCREMENT, bulan TEXT, kamar_no TEXT,
                jumlah INTEGER, status TEXT, jatuh_tempo TEXT, bukti_bayar TEXT)''')
    
    query_db('''CREATE TABLE IF NOT EXISTS keluhan (id INTEGER PRIMARY KEY AUTOINCREMENT,
                kamar_no TEXT, isi TEXT, status TEXT, tanggapan TEXT)''')

def patch_pembayaran_db():
    # Cek kolom yang ada di tabel pembayaran
    columns_info = query_db("PRAGMA table_info(pembayaran)", fetch=True)
    existing_columns = [col[1] for col in columns_info]

    # Tambahkan jatuh_tempo jika belum ada
    if "jatuh_tempo" not in existing_columns:
        try:
            query_db("ALTER TABLE pembayaran ADD COLUMN jatuh_tempo TEXT")
        except:
            pass

    # Tambahkan bukti_bayar jika belum ada
    if "bukti_bayar" not in existing_columns:
        try:
            query_db("ALTER TABLE pembayaran ADD COLUMN bukti_bayar TEXT")
        except Exception as e:
            print(f"Gagal update kolom bukti: {e}")

def patch_db():
    columns_info = query_db("PRAGMA table_info(keluhan)", fetch=True)
    existing_columns = [col[1] for col in columns_info]

    if "tanggapan" not in existing_columns:
        try:
            query_db("ALTER TABLE keluhan ADD COLUMN tanggapan TEXT")
            print("Database updated: Kolom 'tanggapan' berhasil ditambahkan.")
        except Exception as e:
            print(f"Gagal menambah kolom: {e}")

import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QStackedWidget, QPushButton, QLabel, QTableWidget, QTableWidgetItem, 
    QHeaderView, QDialog, QLineEdit, QMessageBox, QFrame, QFormLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtWidgets import QFileDialog
from datetime import datetime

# Import database functions
from database import query_db

# Import StatCard
from .components import StatCard

class UserWindow(QMainWindow):
    def __init__(self, username="User", email=""):
        super().__init__()
        self.username = username
        self.email = email
        self.setWindowTitle(f"Portal Penghuni - {username}")
        self.resize(1000, 700)
        # Background handled by QSS (QMainWindow)

        central = QWidget(); self.setCentralWidget(central)
        layout = QHBoxLayout(central); layout.setContentsMargins(0, 0, 0, 0)
        
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(220)
        side_lay = QVBoxLayout(self.sidebar)
        
        # BAGIAN LOGO GAMBAR
        self.logo_label = QLabel()
        assets_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
        pixmap = QPixmap(os.path.join(assets_path, "dasboard_icon.jpg"))
        
        if pixmap.isNull():
             self.logo_label.setText("USER")
             self.logo_label.setStyleSheet("color:white; font-weight:bold; font-size:20px;")
        else:
            scaled_pixmap = pixmap.scaledToWidth(80, Qt.TransformationMode.SmoothTransformation)
            self.logo_label.setPixmap(scaled_pixmap)

        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setStyleSheet("padding: 20px 0px;") 
        
        side_lay.addWidget(self.logo_label)
        self.kos_name_label = QLabel("rill KOS")
        self.kos_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.kos_name_label.setStyleSheet("""
            color: white; 
            font-size: 14px; 
            font-weight: bold; 
            padding-bottom: 20px;
            letter-spacing: 1px;
        """)
        side_lay.addWidget(self.kos_name_label)

        lbl_kategori = QLabel("MAIN MENU")
        lbl_kategori.setStyleSheet("""
            color: #94A3B8; 
            font-size: 11px; 
            font-weight: bold; 
            padding-left: 20px; 
            margin-top: 20px; 
            margin-bottom: 5px;
            letter-spacing: 1px;
        """)
        side_lay.addWidget(lbl_kategori)

        self.btn_dash = QPushButton("  Dashboard")
        self.btn_profil = QPushButton("  Profil / Data")
        self.btn_tagihan = QPushButton("  Tagihan Saya")
        self.btn_keluhan = QPushButton("  Kirim Keluhan")
        
        for b in [self.btn_dash, self.btn_profil, self.btn_tagihan, self.btn_keluhan]:
            b.setProperty("class", "sidebar-btn")
            side_lay.addWidget(b)
            
        side_lay.addStretch()
        btn_out = QPushButton("Logout")
        btn_out.setStyleSheet("color: #EF4444; border: none; padding: 20px; font-weight: bold;")
        btn_out.clicked.connect(self.close)
        side_lay.addWidget(btn_out)
        
        self.pages = QStackedWidget()
        self.setup_pages()
        layout.addWidget(self.sidebar); layout.addWidget(self.pages)
        
        # Navigasi Index
        self.btn_dash.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        self.btn_profil.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        self.btn_tagihan.clicked.connect(lambda: self.pages.setCurrentIndex(2))
        self.btn_keluhan.clicked.connect(lambda: self.pages.setCurrentIndex(3))

    def setup_pages(self):
        # Dashboard
        self.page_dash = QWidget(); self.lay_dash = QVBoxLayout(self.page_dash)
        self.lay_dash.setContentsMargins(40,40,40,40)
        self.pages.addWidget(self.page_dash)
        
        # Profil
        self.page_profil = QWidget(); self.lay_profil = QVBoxLayout(self.page_profil)
        self.lay_profil.setContentsMargins(40,40,40,40)
        self.pages.addWidget(self.page_profil)
        
        # Tagihan
        self.page_tagihan = QWidget(); l_tag = QVBoxLayout(self.page_tagihan); l_tag.setContentsMargins(40,40,40,40)
        l_tag.addWidget(QLabel("Riwayat Tagihan", styleSheet="font-size: 22px; color: white; font-weight: bold;"))
        self.table_user = QTableWidget(0, 3)
        self.table_user.setHorizontalHeaderLabels(["BULAN", "JUMLAH", "STATUS"])
        self.table_user.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # QTableWidget style handled by QSS
        l_tag.addWidget(self.table_user)
        self.pages.addWidget(self.page_tagihan)
        
        # Keluhan
        self.page_keluhan = QWidget(); l_kel = QVBoxLayout(self.page_keluhan); l_kel.setContentsMargins(40,40,40,40)
        l_kel.addWidget(QLabel("Kirim Keluhan", styleSheet="font-size: 22px; color: white; font-weight: bold;"))
        self.input_keluhan = QLineEdit(); self.input_keluhan.setPlaceholderText("Tulis keluhan...")
        self.input_keluhan.setStyleSheet("padding: 15px; margin-top: 10px;")
        
        btn_kirim = QPushButton("Kirim Keluhan")
        btn_kirim.setProperty("class", "primary-btn")
        btn_kirim.clicked.connect(self.save_keluhan)
        l_kel.addWidget(self.input_keluhan); l_kel.addWidget(btn_kirim); l_kel.addStretch()
        self.pages.addWidget(self.page_keluhan)
        
        self.refresh_user_dashboard()
        self.refresh_profil_page()
        self.load_data()

    def refresh_user_dashboard(self):
        # Bersihkan layout lama
        while self.lay_dash.count():
            child = self.lay_dash.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

        # Header Ucapan Selamat Datang
        header = QLabel(f"Halo")
        header.setStyleSheet("font-size: 28px; color: white; font-weight: 800; margin-bottom: 5px;")
        sub_header = QLabel("Selamat datang kembali di rill KOS. Berikut ringkasan akun Anda.")
        sub_header.setStyleSheet("color: #94A3B8; font-size: 14px; margin-bottom: 25px;")
        
        self.lay_dash.addWidget(header)
        self.lay_dash.addWidget(sub_header)

        # Logika Mengambil Data untuk Statistik
        res_user = query_db("SELECT kamar_no FROM penghuni WHERE username = ?", (self.username,), fetch=True)
        no_kamar = res_user[0][0] if res_user else "-"
        
        # Hitung total tagihan yang statusnya belum lunas
        total_tunggakan = 0
        if no_kamar != "-":
            tagihan_data = query_db("SELECT jumlah FROM pembayaran WHERE kamar_no = ? AND status != 'Lunas'", (no_kamar,), fetch=True)
            total_tunggakan = sum(t[0] for t in tagihan_data) if tagihan_data else 0

        # Barisan Kartu Statistik (Stat Cards)
        card_layout = QHBoxLayout()
        card_layout.setSpacing(20)
        
        card_layout.addWidget(StatCard("NOMOR KAMAR", no_kamar, "#3B82F6"))
        card_layout.addWidget(StatCard("STATUS HUNIAN", "AKTIF", "#22C55E"))
        
        # Format Rupiah untuk tunggakan
        txt_tunggakan = f"Rp {total_tunggakan:,}".replace(",", ".")
        card_layout.addWidget(StatCard("BELUM DIBAYAR", txt_tunggakan, "#EF4444"))
        
        self.lay_dash.addLayout(card_layout)
        
        self.lay_dash.addSpacing(30)

        # 5. Area Notifikasi / Pesan dari Admin
        if no_kamar != "-":
            # Ambil keluhan yang sudah ada tanggapan tapi belum di-close oleh user
            notif_data = query_db("SELECT id, isi, tanggapan FROM keluhan WHERE kamar_no = ? AND status = 'Selesai' AND tanggapan != ''", (no_kamar,), fetch=True)
            
            if notif_data:
                notif_title = QLabel("📢 PESAN TERBARU")
                notif_title.setStyleSheet("color: #94A3B8; font-weight: bold; font-size: 12px; letter-spacing: 1px;")
                self.lay_dash.addWidget(notif_title)
                
                for id_kel, isi, resp in notif_data:
                    card = QFrame()
                    card.setStyleSheet("""
                        QFrame {
                            background-color: #1E293B; 
                            border-left: 5px solid #22C55E; 
                            border-radius: 10px; 
                            padding: 15px;
                        }
                    """)
                    l = QVBoxLayout(card)
                    
                    h = QHBoxLayout()
                    h.addWidget(QLabel("Tanggapan Keluhan Selesai", styleSheet="color: #22C55E; font-weight: bold;"))
                    h.addStretch()
                    
                    btn_x = QPushButton("Tandai Dibaca")
                    btn_x.setCursor(Qt.CursorShape.PointingHandCursor)
                    btn_x.setStyleSheet("background: #334155; color: white; padding: 5px 10px; border-radius: 5px; font-size: 10px;")
                    btn_x.clicked.connect(lambda _, ik=id_kel: self.mark_as_read(ik))
                    h.addWidget(btn_x)
                    
                    l.addLayout(h)
                    l.addWidget(QLabel(f"Keluhan Anda: \"{isi}\"", styleSheet="color: #94A3B8; font-style: italic;"))
                    l.addWidget(QLabel(f"Admin: {resp}", styleSheet="color: white; font-size: 14px; font-weight: 500;"))
                    self.lay_dash.addWidget(card)

        self.lay_dash.addStretch()

    def mark_as_read(self, id_keluhan):
        query_db("UPDATE keluhan SET status = 'Closed' WHERE id = ?", (id_keluhan,))
        self.refresh_user_dashboard() 

    def refresh_profil_page(self):
        # Bersihkan layout profil sebelum render ulang
        self.clear_layout(self.lay_profil)

        # Ambil data dari database
        data = query_db("SELECT nama, nik, hp, kamar_no, tgl_masuk FROM penghuni WHERE username = ?", (self.username,), fetch=True)
        
        sudah_ada_data = False
        if data and any(data[0]): 
            sudah_ada_data = True

        profile_card = QFrame()
        profile_card.setObjectName("ProfileCard")
        # Inline style is specific here, maybe hard to generalize
        profile_card.setStyleSheet("background-color: #1E1E1E; border-radius: 12px;")
        profile_card.setFixedWidth(800)
        
        card_layout = QVBoxLayout(profile_card)
        card_layout.setContentsMargins(40, 40, 40, 40)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(40)

        # PANEL KIRI
        left_panel = QVBoxLayout()
        self.img_label = QLabel()
        self.img_label.setFixedSize(200, 200)
        self.img_label.setStyleSheet("background-color: #A0A0A0; border-radius: 8px;")
        
        photo_path = f"profile_{self.username}.png"
        if os.path.exists(photo_path):
            pix = QPixmap(photo_path).scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
            self.img_label.setPixmap(pix)
        
        left_panel.addWidget(self.img_label)

        btn_ganti_foto = QPushButton("Ganti Foto")
        btn_ganti_foto.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_ganti_foto.setStyleSheet("background: #444; color: white; border: 1px solid white; padding: 8px; border-radius: 4px; margin-top: 10px;")
        btn_ganti_foto.clicked.connect(self.upload_photo)
        left_panel.addWidget(btn_ganti_foto)
        
        left_panel.addStretch()

        # PANEL KANAN
        right_panel = QFormLayout()
        right_panel.setSpacing(15)

        style_input = "background-color: transparent; border: 1px solid white; border-radius: 6px; color: white; padding: 10px; min-width: 300px;"
        style_locked = "background-color: #334155; border: 1px solid #475569; border-radius: 6px; color: #94A3B8; padding: 10px; min-width: 300px;"

        self.in_nama = QLineEdit(); self.in_nik = QLineEdit()
        self.in_hp = QLineEdit(); self.in_kamar = QLineEdit(); self.in_tgl = QLineEdit()
        
        fields = [
            ("Name", self.in_nama), ("NIK", self.in_nik), 
            ("Nomor HP", self.in_hp), ("Kamar No", self.in_kamar), 
            ("Tgl Masuk", self.in_tgl)
        ]

        if data:
            d = data[0]
            self.in_nama.setText(str(d[0])); self.in_nik.setText(str(d[1]))
            self.in_hp.setText(str(d[2])); self.in_kamar.setText(str(d[3]))
            self.in_tgl.setText(str(d[4]))

        for label_text, edit_field in fields:
            if sudah_ada_data:
                edit_field.setReadOnly(True)
                edit_field.setStyleSheet(style_locked)
            else:
                edit_field.setStyleSheet(style_input)
            right_panel.addRow(QLabel(label_text, styleSheet="color: white; font-weight: bold;"), edit_field)

        content_layout.addLayout(left_panel)
        content_layout.addLayout(right_panel)
        card_layout.addLayout(content_layout)

        if not sudah_ada_data:
            self.btn_update = QPushButton("Simpan Data Profil")
            self.btn_update.setStyleSheet("background-color: #00A3CC; color: white; padding: 12px; border-radius: 6px; font-weight: bold;")
            self.btn_update.clicked.connect(self.save_profil)
            card_layout.addWidget(self.btn_update, alignment=Qt.AlignmentFlag.AlignCenter)
        else:
            lbl_info = QLabel("✔ Terima Kasih Telah Mengisi Data Anda.")
            lbl_info.setStyleSheet("color: #22C55E; font-weight: bold; margin-top: 10px;")
            card_layout.addWidget(lbl_info, alignment=Qt.AlignmentFlag.AlignCenter)

        self.lay_profil.addWidget(profile_card, alignment=Qt.AlignmentFlag.AlignCenter)
        self.lay_profil.addStretch()

    def upload_photo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Pilih Foto Profil", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            save_path = f"profile_{self.username}.png"
            pixmap = QPixmap(file_path)
            pixmap.save(save_path)
            self.refresh_profil_page()
            QMessageBox.information(self, "Berhasil", "Foto profil berhasil dipilih!")

    def save_profil(self):
        nama = self.in_nama.text()
        nik = self.in_nik.text()
        hp = self.in_hp.text()
        kamar = self.in_kamar.text()
        tgl = self.in_tgl.text()

        if not all([nama, nik, hp, kamar, tgl]):
            QMessageBox.warning(self, "Peringatan", "Semua kolom data harus diisi!")
            return

        existing = query_db("SELECT id FROM penghuni WHERE username = ?", (self.username,), fetch=True)
        
        if existing:
            query_db("""
                UPDATE penghuni 
                SET nama=?, nik=?, hp=?, kamar_no=?, tgl_masuk=? 
                WHERE username=?
            """, (nama, nik, hp, kamar, tgl, self.username))
            msg = "Profil berhasil diperbarui!"
        else:
            query_db("""
                INSERT INTO penghuni (nama, nik, hp, kamar_no, username, tgl_masuk) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nama, nik, hp, kamar, self.username, tgl))
            msg = "Data berhasil disimpan!"
        
        QMessageBox.information(self, "Berhasil", msg)
        self.refresh_profil_page()
        self.refresh_user_dashboard()
        self.load_data()

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    def load_data(self):
        res = query_db("SELECT kamar_no FROM penghuni WHERE username = ?", (self.username,), fetch=True)
        if res:
            data = query_db("SELECT bulan, jumlah, jatuh_tempo, status, bukti_bayar FROM pembayaran WHERE kamar_no = ?", (res[0][0],), fetch=True)
            
            self.table_user.setColumnCount(5) 
            self.table_user.setHorizontalHeaderLabels(["BULAN", "JUMLAH", "JATUH TEMPO", "STATUS", "BUKTI"])
            
            self.table_user.setRowCount(0)
            for r_idx, r_data in enumerate(data):
                self.table_user.insertRow(r_idx)
                
                is_overdue = False
                val_tempo = r_data[2]  
                val_status = r_data[3]
                val_bukti = r_data[4] 
                
                if val_tempo and val_status != "Lunas":
                    try:
                        tgl = datetime.strptime(val_tempo, "%Y-%m-%d")
                        if tgl < datetime.now():
                            is_overdue = True
                    except: pass

                for c_idx in range(4):
                    val = r_data[c_idx]
                    display_text = str(val) if val else "-"
                    
                    if c_idx == 1:  
                        try:
                            display_text = f"Rp {int(val):,}".replace(",", ".")
                        except: pass
                    
                    item = QTableWidgetItem(display_text)
                    
                    if is_overdue:
                        item.setBackground(QColor("#B91C1C")) 
                        item.setForeground(Qt.GlobalColor.white) 
                        
                    self.table_user.setItem(r_idx, c_idx, item)

                if val_bukti and os.path.exists(val_bukti):
                    btn_view = QPushButton("Lihat Bukti")
                    btn_view.setStyleSheet("background: #10B981; color: white; padding: 5px; font-weight: bold;")
                    btn_view.clicked.connect(lambda _, path=val_bukti: self.popup_gambar(path))
                    self.table_user.setCellWidget(r_idx, 4, btn_view)
                else:
                    item_empty = QTableWidgetItem("-")
                    if is_overdue:
                        item_empty.setBackground(QColor("#B91C1C"))
                    self.table_user.setItem(r_idx, 4, item_empty)

    def popup_gambar(self, file_path):
        diag = QDialog(self)
        diag.setWindowTitle("Bukti Pembayaran Cash")
        diag.setStyleSheet("background-color: #0F172A;")
        lay = QVBoxLayout(diag)
        
        lbl_img = QLabel()
        pixmap = QPixmap(file_path)
        lbl_img.setPixmap(pixmap.scaled(300, 500, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        
        lay.addWidget(lbl_img)
        btn_close = QPushButton("Tutup")
        btn_close.clicked.connect(diag.close)
        btn_close.setProperty("class", "primary-btn")
        lay.addWidget(btn_close)
        
        diag.exec()
        
    def save_keluhan(self):
        txt = self.input_keluhan.text()
        if txt:
            res = query_db("SELECT kamar_no FROM penghuni WHERE username = ?", (self.username,), fetch=True)
            kmr = res[0][0] if res else "Unknown"
            query_db("INSERT INTO keluhan (kamar_no, isi, status, tanggapan) VALUES (?, ?, ?, ?)", 
                     (kmr, txt, "Pending", "")) 
            self.input_keluhan.clear()
            QMessageBox.information(self, "Berhasil", "Keluhan telah terkirim.")

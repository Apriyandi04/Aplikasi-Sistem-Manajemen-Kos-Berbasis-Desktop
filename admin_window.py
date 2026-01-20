import os
import pandas as pd
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QStackedWidget, QPushButton, QLabel, QTableWidget, QTableWidgetItem, 
    QHeaderView, QDialog, QFormLayout, QLineEdit, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtWidgets import QFileDialog
from datetime import datetime

# Import functions from root database
from database import query_db

# Import StatCard from components
from .components import StatCard

# --- ADMIN WINDOW ---
class AdminWindow(QMainWindow):
    def __init__(self, email="Admin"):
        super().__init__()
        self.setWindowTitle("Admin Dashboard - Kos Management")
        self.resize(1000, 700)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0,0,0,0)
        
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(220)
        side_lay = QVBoxLayout(self.sidebar)
        
        # Logo
        self.logo_label = QLabel()
        # Adjusted path to assets
        assets_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
        pixmap = QPixmap(os.path.join(assets_path, "dasboard_icon.jpg"))
        
        if pixmap.isNull():
             # Fallback if image not found
             self.logo_label.setText("ADMIN")
             self.logo_label.setStyleSheet("color:white; font-weight:bold; font-size:20px;")
        else:
            scaled_pixmap = pixmap.scaledToWidth(80, Qt.TransformationMode.SmoothTransformation)
            self.logo_label.setPixmap(scaled_pixmap)
            
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setStyleSheet("padding: 20px 0px;")
        side_lay.addWidget(self.logo_label)
        
        self.kos_name_label = QLabel("rill KOS")
        self.kos_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.kos_name_label.setStyleSheet("color: #94A3B8; font-size: 12px; font-weight: bold; padding-bottom: 20px;")
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

        self.menus = [("Dashboard", 0), ("Data Kamar", 1), ("Data Penghuni", 2), ("Pembayaran", 3), ("Laporan Keluhan", 4)]
        for name, idx in self.menus:
            btn = QPushButton(f"  {name}")
            btn.setProperty("class", "sidebar-btn")
            btn.clicked.connect(lambda _, i=idx: self.pages.setCurrentIndex(i))
            side_lay.addWidget(btn)
        
        side_lay.addStretch()
        btn_logout = QPushButton("Logout")
        btn_logout.setStyleSheet("color: #EF4444; font-weight: bold; padding: 20px; border: none;")
        btn_logout.clicked.connect(self.close)
        side_lay.addWidget(btn_logout)
        
        self.pages = QStackedWidget()
        self.refresh_ui()
        layout.addWidget(self.sidebar)
        layout.addWidget(self.pages)

    def refresh_ui(self):
        while self.pages.count() > 0:
            self.pages.removeWidget(self.pages.widget(0))
        self.pages.addWidget(self.create_admin_dashboard())
        self.pages.addWidget(self.create_page("Kamar", ["id", "no_kamar", "kapasitas", "harga", "status", "fasilitas"], "kamar"))
        self.pages.addWidget(self.create_page("Penghuni", ["id", "tgl_masuk", "nama", "nik", "kamar_no", "username", "hp"], "penghuni"))
        self.pages.addWidget(self.create_page("Pembayaran", ["id", "bulan", "kamar_no", "jumlah", "status", "jatuh_tempo"], "pembayaran"))
        self.pages.addWidget(self.create_page("Keluhan", ["id", "kamar_no", "isi", "status", "tanggapan"], "keluhan"))

    def create_admin_dashboard(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(40,40,40,40)
        lay.setSpacing(25)
        
        # Header
        lay.addWidget(QLabel("Ringkasan Kos", styleSheet="font-size: 24px; color: white; font-weight: bold;"))
        
        # --- LOGIKA DATA ---
        tk = 15
        tk_terisi = query_db("SELECT COUNT(*) FROM kamar WHERE status = 'Terisi'", fetch=True)[0][0] or 0
        tk_kosong = query_db("SELECT COUNT(*) FROM kamar WHERE status = 'Tersedia' OR status = ''", fetch=True)[0][0] or 0
        tp = query_db("SELECT COUNT(*) FROM penghuni", fetch=True)[0][0] or 0
        tkul = query_db("SELECT COUNT(*) FROM keluhan WHERE status = 'Pending'", fetch=True)[0][0] or 0
        
        # Hitung Persentase untuk Progress Bar
        persentase = int((tk_terisi / tk * 100)) if tk > 0 else 0

        # KARTU STATISTIK
        grid = QHBoxLayout()
        # Using colors from main would be better if imported, but hex works.
        grid.addWidget(StatCard("TOTAL KAMAR", tk, "#3B82F6"))
        grid.addWidget(StatCard("TERISI", tk_terisi, "#22C55E"))
        grid.addWidget(StatCard("KOSONG", tk_kosong, "#F59E0B"))
        grid.addWidget(StatCard("PENGHUNI", tp, "#6366F1"))
        grid.addWidget(StatCard("KELUHAN", tkul, "#EF4444"))
        lay.addLayout(grid)

        lay.addSpacing(10)

        # SEKSI AKSI CEPAT
        lay.addWidget(QLabel("Aksi Cepat", styleSheet="font-size: 18px; color: white; font-weight: bold;"))
        aksi_box = QVBoxLayout()
        btns_aksi = [
            ("🏠  Kelola Kamar", 1),
            ("👥  Kelola Penghuni", 2),
            ("💳  Input Pembayaran", 3)
        ]
        
        for text, idx in btns_aksi:
            btn = QPushButton(text)
            btn.setProperty("class", "action-btn")
            btn.clicked.connect(lambda _, i=idx: self.pages.setCurrentIndex(i))
            aksi_box.addWidget(btn)
        lay.addLayout(aksi_box)

        lay.addSpacing(10)

        # --- 3. SEKSI TINGKAT HUNIAN ---
        lay.addWidget(QLabel("Tingkat Hunian", styleSheet="font-size: 18px; color: white; font-weight: bold;"))
        
        hunian_container = QVBoxLayout()
        # Baris Teks Persentase
        txt_lay = QHBoxLayout()
        txt_lay.addWidget(QLabel("Persentase Terisi", styleSheet="color: #94A3B8;"))
        txt_lay.addStretch()
        txt_lay.addWidget(QLabel(f"{persentase}%", styleSheet="color: white; font-weight: bold;"))
        hunian_container.addLayout(txt_lay)
        
        # Progress Bar Manual (Visual)
        progress_bg = QFrame()
        progress_bg.setFixedHeight(12)
        progress_bg.setStyleSheet("""
            background-color: #1E293B;
            border-radius: 6px;
        """)
        
        # Indikator Progress
        progress_fill = QFrame(progress_bg)
        progress_fill.setFixedHeight(12)
        fill_width = int((persentase / 100) * 700) if persentase > 0 else 0
        progress_fill.setFixedWidth(max(fill_width, 12)) 
        progress_fill.setStyleSheet("background-color: #2563EB; border-radius: 6px;")
        
        hunian_container.addWidget(progress_bg)
        
        # Keterangan Kamar
        lbl_detail = QLabel(f"{tk_terisi} dari {tk} kamar terisi")
        lbl_detail.setStyleSheet("color: #94A3B8; font-size: 12px; margin-top: 5px;")
        hunian_container.addWidget(lbl_detail)
        
        lay.addLayout(hunian_container)
        lay.addStretch()
        return page

    def create_page(self, title, cols, table_name):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(30,30,30,30)
        
        h_lay = QHBoxLayout()
        h_lay.addWidget(QLabel(title, styleSheet="font-size: 22px; color: white; font-weight: bold;"))
        
        # Tombol Export
        btn_export = QPushButton("📊 Excel")
        btn_export.setProperty("class", "success-btn")
        btn_export.clicked.connect(lambda: self.export_to_excel(table_name))
        
        # Tombol Tambah
        btn_add = QPushButton("+ Tambah")
        btn_add.setProperty("class", "primary-btn")
        btn_add.clicked.connect(lambda: self.show_dialog(title, cols, table_name))
        
        h_lay.addStretch()
        h_lay.addWidget(btn_export)
        h_lay.addWidget(btn_add)
        lay.addLayout(h_lay)
        
        data = query_db(f"SELECT {', '.join(cols)} FROM {table_name}", fetch=True)
        if data is None: data = []
        table = QTableWidget(len(data), len(cols) + 1)
        table.setHorizontalHeaderLabels([c.upper() for c in cols] + ["AKSI"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        for r_idx, r_val in enumerate(data):
            row_id = r_val[0]
            is_overdue = False
            if table_name == "pembayaran":
                try:
                    status_bayar = r_val[4]
                    tgl_tempo_str = r_val[5]
                    
                    if tgl_tempo_str and status_bayar != "Lunas":
                        tgl_tempo = datetime.strptime(tgl_tempo_str, "%Y-%m-%d")
                        if tgl_tempo < datetime.now():
                            is_overdue = True
                except:
                    pass
            for c_idx, val in enumerate(r_val):
                display_text = str(val) if val is not None else "-"
                
                if cols[c_idx] in ["harga", "jumlah"]:
                    try:
                        display_text = f"Rp {int(val):,}".replace(",", ".")
                    except: pass
                
                item = QTableWidgetItem(display_text)
                
                if is_overdue:
                    item.setBackground(QColor("#B91C1C")) # Merah gelap
                
                table.setItem(r_idx, c_idx, item)
            
            btn_container = QWidget()
            btn_lay = QHBoxLayout(btn_container)
            btn_lay.setContentsMargins(2, 2, 2, 2)
            btn_edit = QPushButton("Edit")
            btn_edit.setProperty("class", "success-btn")
            btn_edit.setStyleSheet("font-size: 10px; padding: 4px;") 
            
            btn_del = QPushButton("Hapus")
            btn_del.setProperty("class", "danger-btn")
            btn_del.setStyleSheet("font-size: 10px; padding: 4px;")
            
            btn_edit.clicked.connect(lambda _, rid=row_id, rd=r_val: self.show_dialog(title, cols, table_name, rid, rd))
            btn_del.clicked.connect(lambda _, rid=row_id: self.delete_data(table_name, rid))
            
            btn_lay.addWidget(btn_edit)
            btn_lay.addWidget(btn_del)
            table.setCellWidget(r_idx, len(cols), btn_container)
        
        lay.addWidget(table)
        return page

    def export_to_excel(self, table_name):
        column_map = {
            "kamar": ["no_kamar", "kapasitas", "harga", "status", "fasilitas"],
            "penghuni": ["nama", "nik", "kamar_no", "hp", "tgl_masuk"],
            "pembayaran": ["bulan", "kamar_no", "jumlah", "status"],
            "keluhan": ["kamar_no", "isi", "status", "tanggapan"]
        }
        
        cols_to_select = column_map.get(table_name, ["*"])
        query = f"SELECT {', '.join(cols_to_select)} FROM {table_name}"
        data = query_db(query, fetch=True)
        if not data:
            QMessageBox.warning(self, "Peringatan", "Tidak ada data.")
            return
        file_path, _ = QFileDialog.getSaveFileName(self, "Simpan", f"Backup_{table_name}.xlsx", "Excel Files (*.xlsx)")

        if file_path:
            try:
                df = pd.DataFrame(data, columns=[c.upper() for c in cols_to_select])
                df.to_excel(file_path, index=False)
                QMessageBox.information(self, "Berhasil", "Data berhasil disimpan!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Gagal: {e}")

    def show_dialog(self, title, cols, table_name, row_id=None, row_data=None):
        diag = QDialog(self)
        diag.setWindowTitle(title)
        diag.setFixedWidth(400)
        # Background handled by global QDialog style if it affects child dialogs, 
        # but we might need explicit class if QDialog style is too generic.
        # It's #1a2238 vs #0F172A. QSS handles QDialog.
        
        flay = QFormLayout(diag)
        inputs = {}
        
        active_cols = [c for c in cols if c != 'id']
        
        if table_name == "keluhan" and "tanggapan" not in active_cols:
            active_cols.append("tanggapan")

        if table_name == "pembayaran" and "bukti_bayar" not in active_cols:
            active_cols.append("bukti_bayar")

        for i, c in enumerate(active_cols):
            edit = QLineEdit()
            # QLineEdit style handled by QSS
            
            if c == "jatuh_tempo":
                edit.setPlaceholderText("YYYY-MM-DD (Contoh: 2024-06-10)")
            
            if c == "bukti_bayar":
                edit.setReadOnly(True) 
                btn_upload = QPushButton("📸 Pilih Bukti Cash")
                btn_upload.setProperty("class", "primary-btn")
                
                def pick_bukti(target_edit=edit):
                    f_path, _ = QFileDialog.getOpenFileName(self, "Pilih Foto Bukti", "", "Images (*.png *.jpg *.jpeg)")
                    if f_path:
                        fname = f"bukti_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
                        pix = QPixmap(f_path)
                        # Save to root/assets? Or root? 
                        # Original code saved to CWD.
                        pix.save(fname) 
                        target_edit.setText(fname)
                
                btn_upload.clicked.connect(lambda: pick_bukti())
                
                flay.addRow(QLabel("File Bukti:", styleSheet="color: white;"), edit)
                flay.addRow("", btn_upload)
                inputs[c] = edit
                continue 
            if row_id and row_data:
                try:
                    if c in cols:
                        val_idx = cols.index(c)
                        edit.setText(str(row_data[val_idx]))
                    elif c == "tanggapan" and table_name == "keluhan":
                        edit.setText(str(row_data[-1]))
                except: pass
                    
            inputs[c] = edit
            flay.addRow(QLabel(c.replace("_", " ").capitalize(), styleSheet="color: white;"), edit)
            
        btn = QPushButton("Simpan")
        btn.setProperty("class", "success-btn")
        btn.clicked.connect(diag.accept)
        flay.addWidget(btn)
        
        if diag.exec():
            vals = [inputs[c].text() for c in active_cols]
            
            if row_id:
                set_q = ", ".join([f"{c} = ?" for c in active_cols])
                query_db(f"UPDATE {table_name} SET {set_q} WHERE id = ?", (*vals, row_id))
            else:
                query_db(f"INSERT INTO {table_name} ({', '.join(active_cols)}) VALUES ({', '.join(['?']*len(vals))})", vals)
            
            self.refresh_ui()

    def delete_data(self, table_name, row_id):
        confirm = QMessageBox.question(self, "Konfirmasi", "Hapus data ini?", 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            query_db(f"DELETE FROM {table_name} WHERE id = ?", (row_id,))
            self.refresh_ui()
            QMessageBox.information(self, "Berhasil", "Data telah dihapus.")
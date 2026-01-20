import sys
import os
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox, QCheckBox, QDialog
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

# Adjust import to root database
# Since main.py runs from root, 'database' is in path.
# However, for IDE support we usually do relative imports if it's a package.
# Assuming run from root via 'python main.py'
import database
from database import DB_FILE, init_db
from .register import RegisterDialog

# We no longer import AdminWindow/UserWindow just for type checking locally
# or if we do, we do it safely.
# Actually, login.py doesn't instantiate them, so we can remove imports or keep them for reference if needed.

init_db()

# --- WINDOW LOGIN UTAMA ---
class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setObjectName("LoginWindow")
        self.setWindowTitle("Sistem Manajemen Kos")
        self.resize(450, 600)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(15)

        # Logo
        self.logo = QLabel()
        # Adjusted path to assets/
        img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "login_icon.jpg")
        if os.path.exists(img_path):
            pixmap = QPixmap(img_path).scaled(200, 150, Qt.AspectRatioMode.KeepAspectRatio,
                                                Qt.TransformationMode.SmoothTransformation)
            self.logo.setPixmap(pixmap)
        else:
            self.logo.setText("🏠")
            self.logo.setStyleSheet("color: white; font-size: 60px;")
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("KOSAN")
        title.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.setFixedWidth(320)
        # Style is now handling QLineEdit

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setFixedWidth(320)

        # Style Checkbox Ingat Saya
        self.cb_remember = QCheckBox("Ingat Saya")
        self.cb_remember.setFixedWidth(320)
        # Style handles QCheckBox

        btn_login = QPushButton("Sign In")
        btn_login.setFixedWidth(320)
        btn_login.setProperty("class", "primary-btn")
        btn_login.clicked.connect(self.handle_login)

        btn_register = QPushButton("Belum punya akun? Daftar")
        btn_register.setProperty("class", "link-btn")
        btn_register.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_register.clicked.connect(self.open_register)

        # Cek Session Saat Start
        self.load_remembered_data()

        layout.addStretch()
        layout.addWidget(self.logo)
        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(self.username, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.password, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.cb_remember, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(btn_login, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(btn_register, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

    def load_remembered_data(self):
        """Mengambil data sesi dari SQLite."""
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT user, pw FROM session WHERE id=1")
            row = cursor.fetchone()
            conn.close()
            if row:
                self.username.setText(row[0])
                self.password.setText(row[1])
                self.cb_remember.setChecked(True)
        except:
            pass

    def open_register(self):
        dlg = RegisterDialog(self)
        dlg.exec()

    def handle_login(self):
        u = self.username.text()
        p = self.password.text()
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT password, role, email FROM users WHERE username=?", (u,))
        user_data = cursor.fetchone()
        
        if user_data and user_data[0] == p:
            if self.cb_remember.isChecked():
                cursor.execute("REPLACE INTO session (id, user, pw) VALUES (1, ?, ?)", (u, p))
            else:
                cursor.execute("DELETE FROM session WHERE id=1")
            
            conn.commit()
            conn.close()

            # SIMPAN DATA KE VARIABLE OBJECT (Agar bisa dibaca main.py)
            self.role = user_data[1]
            self.email = user_data[2]
            self.user_name = u
            
            self.accept() 
        else:
            if conn: conn.close()
            QMessageBox.critical(self, "Error", "Username atau Password salah!")

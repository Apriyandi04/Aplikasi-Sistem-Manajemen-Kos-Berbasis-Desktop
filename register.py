import sqlite3
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox
from database import DB_FILE

class RegisterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("RegisterWindow")
        self.setWindowTitle("Register Akun Baru")
        self.setFixedWidth(350)
        
        layout = QVBoxLayout(self)
        self.form = QFormLayout()
        
        self.reg_user = QLineEdit()
        self.reg_pw = QLineEdit()
        self.reg_pw.setEchoMode(QLineEdit.EchoMode.Password)
        self.reg_email = QLineEdit()
        
        self.form.addRow("Username:", self.reg_user)
        self.form.addRow("Password:", self.reg_pw)
        self.form.addRow("Email:", self.reg_email)
        
        self.btn_done = QPushButton("Daftar Sekarang")
        self.btn_done.setProperty("class", "success-btn")
        self.btn_done.clicked.connect(self.handle_register)
        
        layout.addLayout(self.form)
        layout.addWidget(self.btn_done)

    def handle_register(self):
        u, p, e = self.reg_user.text(), self.reg_pw.text(), self.reg_email.text()
        if u and p and e:
            try:
                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users VALUES (?, ?, 'user', ?)", (u, p, e))
                conn.commit()
                conn.close()
                QMessageBox.information(self, "Sukses", "Akun berhasil dibuat!")
                self.accept()
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Error", "Username sudah terdaftar!")
        else:
            QMessageBox.warning(self, "Error", "Semua kolom harus diisi!")

import sys
import os
from PyQt6.QtWidgets import QApplication, QDialog

# Import database initialization from new module
from database import init_business_db, patch_pembayaran_db, patch_db

# Load Stylesheet Function
def load_stylesheet(app):
    qqss_path = os.path.join(os.path.dirname(__file__), "assets", "style.qss")
    if os.path.exists(qqss_path):
        with open(qqss_path, "r") as f:
            app.setStyleSheet(f.read())
    else:
        print(f"Warning: Stylesheet not found at {qqss_path}")

# Inisialisasi Database
init_business_db()
patch_pembayaran_db()
patch_db()

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Load external stylesheet
    load_stylesheet(app)
    
    # Import windows from views package
    try:
        from views.login import LoginWindow
        from views.admin_window import AdminWindow
        from views.user_window import UserWindow
        
        login = LoginWindow()
        if login.exec() == QDialog.DialogCode.Accepted:
            # LoginWindow sets role, email, user_name
            if hasattr(login, 'role') and login.role == "admin":
                main_win = AdminWindow(login.email)
            else:
                main_win = UserWindow(login.user_name, getattr(login, 'email', ''))
            
            main_win.show()
            sys.exit(app.exec())
    except ImportError as e:
        print(f"Error: Module tidak ditemukan. ({e})")
        # Fallback debug print
        import traceback
        traceback.print_exc()
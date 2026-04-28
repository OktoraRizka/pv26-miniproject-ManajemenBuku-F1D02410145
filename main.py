import sys
import os
from PySide6.QtWidgets import QApplication
from database.db_buku import DatabaseManager
from logic.logic import LoginWindow

def load_stylesheet(file_path):
    """membaca file QSS"""
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                return f.read()
        except Exception as e:
            print(f"Gagal membaca stylesheet: {e}")
    return ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    style_path = os.path.join(base_dir, "style", "style.qss")
    app.setStyleSheet(load_stylesheet(style_path))

    db = DatabaseManager()
    
    login = LoginWindow(db)
    login.show()
    
    sys.exit(app.exec())
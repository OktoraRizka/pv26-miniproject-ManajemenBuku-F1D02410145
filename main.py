import sys
from database.db_buku import DatabaseManager
from logic.logic import MainWindowLogic
from PySide6.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    
    # 1. Inisialisasi Database
    db = DatabaseManager()
    
    # 2. Inisialisasi Logic dan masukkan DB ke dalamnya
    window = MainWindowLogic(db)
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
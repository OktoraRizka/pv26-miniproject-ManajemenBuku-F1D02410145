import sys
from database.db_buku import DatabaseManager
from PySide6.QtWidgets import QApplication
from logic.logic import LoginWindow

def main():
    app = QApplication(sys.argv)
    db = DatabaseManager()    

    login = LoginWindow(db)
    login.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
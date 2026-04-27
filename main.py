import sys
from database.db_buku import DatabaseManager
from logic.logic import LoginWindow
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, 
                             QHBoxLayout, QPushButton, QLabel, QTableWidget, 
                             QHeaderView, QStatusBar, QStackedWidget, QApplication)
from PySide6.QtCore import Qt

class Ui_MainWindow:
    def setup_ui(self, MainWindow):
        MainWindow.setWindowTitle("Sistem Manajemen Perpustakaan")
        MainWindow.setGeometry(100, 100, 1000, 700)
        
        self.central = QWidget()
        MainWindow.setCentralWidget(self.central)
        
        # Layout utama adalah Horizontal (Sidebar di kiri, Konten di kanan)
        self.main_layout = QHBoxLayout(self.central)
        
        # =========================================================
        # SIDEBAR (Menu Utama)
        # =========================================================
        self.sidebar_container = QWidget()
        self.sidebar_container.setFixedWidth(200)
        self.sidebar_layout = QVBoxLayout(self.sidebar_container)
        
        self.label_menu = QLabel("MENU UTAMA")
        self.label_menu.setAlignment(Qt.AlignCenter)
        self.label_menu.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 10px;")
        
        self.btn_menu_buku = QPushButton("📚 Manajemen Buku")
        self.btn_menu_buku.setFixedHeight(40)
        self.btn_menu_anggota = QPushButton("👥 Data Peminjam")
        self.btn_menu_anggota.setFixedHeight(40)
        
        self.sidebar_layout.addWidget(self.label_menu)
        self.sidebar_layout.addWidget(self.btn_menu_buku)
        self.sidebar_layout.addWidget(self.btn_menu_anggota)
        self.sidebar_layout.addStretch() # Mendorong tombol ke atas
        
        self.main_layout.addWidget(self.sidebar_container)

        # =========================================================
        # STACKED WIDGET (Konten yang Berubah-ubah)
        # =========================================================
        self.stacked_widget = QStackedWidget() # <--- PENTING: Membuat objek stacked widget
        self.main_layout.addWidget(self.stacked_widget)

        # ---------------------------------------------------------
        # HALAMAN 1: MANAJEMEN BUKU
        # ---------------------------------------------------------
        self.page_buku = QWidget()
        self.layout_buku = QVBoxLayout(self.page_buku)
        
        # Form Input Buku
        self.form_layout = QFormLayout()
        self.judul_input = QLineEdit()
        self.judul_input.setPlaceholderText("Masukkan judul buku")
        self.form_layout.addRow("Judul Buku:", self.judul_input)
        
        self.penulis_input = QLineEdit()
        self.form_layout.addRow("Penulis:", self.penulis_input)
        
        self.tahun_input = QLineEdit()
        self.form_layout.addRow("Tahun Terbit:", self.tahun_input)
        
        self.genre_input = QLineEdit()
        self.form_layout.addRow("Genre:", self.genre_input)
        self.layout_buku.addLayout(self.form_layout)
        
        # Tombol Aksi Buku
        self.btn_layout = QHBoxLayout()
        self.btn_simpan = QPushButton("Simpan")
        self.btn_hapus = QPushButton("Hapus")
        self.btn_batal = QPushButton("Batal")
        self.btn_layout.addWidget(self.btn_simpan)
        self.btn_layout.addWidget(self.btn_hapus)
        self.btn_layout.addWidget(self.btn_batal)
        self.layout_buku.addLayout(self.btn_layout)
        
        # Search & Table Buku
        self.search_layout = QHBoxLayout()
        self.search_layout.addWidget(QLabel("Cari Buku:"))
        self.search_input = QLineEdit()
        self.search_layout.addWidget(self.search_input)
        self.layout_buku.addLayout(self.search_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Judul", "Tahun", "Genre", "Penulis"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout_buku.addWidget(self.table)
        
        self.stacked_widget.addWidget(self.page_buku) # Masukkan ke index 0

        # ---------------------------------------------------------
        # HALAMAN 2: DATA PEMINJAM
        # ---------------------------------------------------------
        self.page_peminjam = QWidget()
        self.layout_peminjam = QVBoxLayout(self.page_peminjam) 
        
        self.label_peminjam = QLabel("DAFTAR PEMINJAMAN AKTIF")
        self.label_peminjam.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout_peminjam.addWidget(self.label_peminjam)
        
        self.search_layout_p = QHBoxLayout()
        self.search_layout_p.addWidget(QLabel("Cari Peminjam:"))
        self.cari_peminjam = QLineEdit()
        self.cari_peminjam.setPlaceholderText("Masukkan ID atau Nama...")
        self.search_layout_p.addWidget(self.cari_peminjam)
        self.layout_peminjam.addLayout(self.search_layout_p)
        
        self.table_peminjam = QTableWidget()
        self.table_peminjam.setColumnCount(4)
        self.table_peminjam.setHorizontalHeaderLabels(["ID Pinjam", "Judul Buku", "ID Peminjam", "Status"])
        self.table_peminjam.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout_peminjam.addWidget(self.table_peminjam)
        
        self.stacked_widget.addWidget(self.page_peminjam) # Masukkan ke index 1
        
        # Status Bar
        self.statusbar = QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

def main():
    app = QApplication(sys.argv)
    db = DatabaseManager()    

    login = LoginWindow(db)
    login.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
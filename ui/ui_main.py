from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, 
                             QHBoxLayout, QPushButton, QLabel, QTableWidget, 
                             QHeaderView, QStatusBar, QStackedWidget)

class Ui_MainWindow:
    def setup_ui(self, MainWindow):
        MainWindow.setWindowTitle("Sistem Manajemen Buku")
        MainWindow.setGeometry(100, 100, 1000, 700)
        
        self.central = QWidget()
        MainWindow.setCentralWidget(self.central)
        
        # 1. LAYOUT UTAMA (Horizontal: Sidebar di kiri, Konten di kanan)
        self.main_layout = QHBoxLayout(self.central)

        # =========================================================
        # SIDEBAR (Menu Navigasi)
        # =========================================================
        self.sidebar_widget = QWidget()
        self.sidebar_widget.setFixedWidth(180) # Membatasi lebar menu
        self.sidebar_layout = QVBoxLayout(self.sidebar_widget)
        
        self.btn_menu_buku = QPushButton("📚 Manajemen Buku")
        self.btn_menu_buku.setFixedHeight(40)
        self.btn_menu_anggota = QPushButton("👥 Data Peminjam")
        self.btn_menu_anggota.setFixedHeight(40)
        
        self.sidebar_layout.addWidget(self.btn_menu_buku)
        self.sidebar_layout.addWidget(self.btn_menu_anggota)
        self.sidebar_layout.addStretch() # Mendorong tombol ke atas
        
        self.main_layout.addWidget(self.sidebar_widget)

        # =========================================================
        # KONTEN UTAMA (Stacked Widget)
        # =========================================================
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        # ---------------------------------------------------------
        # HALAMAN 1: MANAJEMEN BUKU (Index 0)
        # ---------------------------------------------------------
        self.page_buku = QWidget()
        self.layout_buku = QVBoxLayout(self.page_buku)

        # Form Input Buku
        self.form_layout = QFormLayout()
        self.judul_input = QLineEdit()
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
        self.btn_batal = QPushButton("Batal / Reset")
        self.btn_layout.addWidget(self.btn_simpan)
        self.btn_layout.addWidget(self.btn_hapus)
        self.btn_layout.addWidget(self.btn_batal)
        self.layout_buku.addLayout(self.btn_layout)

        # Search & Tabel Buku
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

        self.stacked_widget.addWidget(self.page_buku)

        # ---------------------------------------------------------
        # HALAMAN 2: DATA PEMINJAM (Index 1)
        # ---------------------------------------------------------
        self.page_peminjam = QWidget()
        self.layout_peminjam = QVBoxLayout(self.page_peminjam)

        self.layout_peminjam.addWidget(QLabel("Cari Peminjam:"))
        self.input_cari_peminjam = QLineEdit() 
        self.input_cari_peminjam.setPlaceholderText("Cari NIM atau Nama...")
        self.layout_peminjam.addWidget(self.input_cari_peminjam)

        # Tambahkan tabel peminjam agar halaman ini tidak kosong
        self.table_peminjam = QTableWidget()
        self.table_peminjam.setColumnCount(4)
        self.table_peminjam.setHorizontalHeaderLabels(["ID Pinjam", "ID Buku", "NIM", "Status"])
        self.table_peminjam.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout_peminjam.addWidget(self.table_peminjam)

        self.stacked_widget.addWidget(self.page_peminjam)

        # Status Bar
        self.statusbar = QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
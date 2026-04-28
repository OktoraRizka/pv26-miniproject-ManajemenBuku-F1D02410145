from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, 
                             QHBoxLayout, QPushButton, QLabel, QTableWidget, 
                             QHeaderView, QStatusBar, QStackedWidget, QGroupBox, 
                             QComboBox, QDateEdit, QMainWindow, QToolBar)
from PySide6.QtGui import QAction, QActionGroup
from PySide6.QtCore import Qt

class Ui_MainWindow:
    def setup_ui(self, MainWindow):
        MainWindow.setWindowTitle("Sistem Manajemen Perpustakaan")
        MainWindow.setGeometry(100, 100, 1100, 750)
        
        # =========================================================
        # 1. MENU BAR 
        # =========================================================
        self.menu_group = QActionGroup(MainWindow)
        self.menubar = MainWindow.menuBar()
        
        # Menu Navigasi
        self.menu_file = self.menubar.addMenu("File")
        self.menu_navigasi = self.menubar.addMenu("Navigasi")
        
        # Actions untuk Menu dan Toolbar
        self.action_manajemen_buku = QAction("📚 Manajemen Buku", MainWindow)
        self.action_data_anggota = QAction("👥 Data Anggota", MainWindow)
        self.action_data_peminjam = QAction("📋 Laporan Peminjaman", MainWindow)
        self.action_about = QAction("Tentang Aplikasi", MainWindow)
        self.action_exit = QAction("🚪 Keluar", MainWindow)
        
        
        self.menu_navigasi.addAction(self.action_manajemen_buku)
        self.menu_navigasi.addAction(self.action_data_anggota)
        self.menu_navigasi.addAction(self.action_data_peminjam)
        self.menu_file.addAction(self.action_about)
        self.menu_file.addAction(self.action_exit)

        self.action_manajemen_buku.setCheckable(True)
        self.action_data_anggota.setCheckable(True)
        self.action_data_peminjam.setCheckable(True)
        
        self.menu_group.addAction(self.action_manajemen_buku)
        self.menu_group.addAction(self.action_data_anggota)
        self.menu_group.addAction(self.action_data_peminjam)
        
        self.action_manajemen_buku.setChecked(True)
        
        # =========================================================
        # 2. TOOLBAR 
        # =========================================================
        self.toolbar = QToolBar("Main Toolbar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolbar)
        self.toolbar.addAction(self.action_manajemen_buku)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_data_anggota)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_data_peminjam)

        # =========================================================
        # 3. KONTEN UTAMA
        # =========================================================
        self.central = QWidget()
        MainWindow.setCentralWidget(self.central)
        self.main_layout = QVBoxLayout(self.central) 

        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        # ---------------------------------------------------------
        # HALAMAN 1: MANAJEMEN BUKU 
        # ---------------------------------------------------------
        self.page_buku = QWidget()
        self.layout_buku = QVBoxLayout(self.page_buku)

        self.group_input_buku = QGroupBox("Detail Informasi Buku")
        self.form_layout = QFormLayout(self.group_input_buku)
        
        self.judul_input = QLineEdit()
        self.penulis_input = QLineEdit()
        self.tahun_input = QLineEdit()
        self.genre_input = QLineEdit()
        self.stok_input = QLineEdit()
        
        self.form_layout.addRow("Judul Buku:", self.judul_input)
        self.form_layout.addRow("Penulis:", self.penulis_input)
        self.form_layout.addRow("Tahun Terbit:", self.tahun_input)
        self.form_layout.addRow("Genre:", self.genre_input)
        self.form_layout.addRow("Stok:", self.stok_input)
        self.layout_buku.addWidget(self.group_input_buku)

        self.btn_layout = QHBoxLayout()
        self.btn_simpan = QPushButton("💾 Simpan / Update")
        self.btn_hapus = QPushButton("🗑️ Hapus")
        self.btn_batal = QPushButton("🔄 Reset")
        self.btn_layout.addWidget(self.btn_simpan)
        self.btn_layout.addWidget(self.btn_hapus)
        self.btn_layout.addWidget(self.btn_batal)
        self.layout_buku.addLayout(self.btn_layout)

        self.search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Cari judul, penulis, atau genre...")
        self.search_layout.addWidget(QLabel("Cari:"))
        self.search_layout.addWidget(self.search_input)
        self.layout_buku.addLayout(self.search_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Judul", "Tahun", "Genre", "Penulis", "Stok"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout_buku.addWidget(self.table)

        self.stacked_widget.addWidget(self.page_buku)

        # ---------------------------------------------------------
        # HALAMAN 2: DATA PEMINJAM / LAPORAN
        # ---------------------------------------------------------
        self.page_peminjam = QWidget()
        self.layout_peminjam = QVBoxLayout(self.page_peminjam)

        self.layout_peminjam.addWidget(QLabel("🔍 Filter Laporan Peminjaman:"))
        self.input_cari_peminjam = QLineEdit() 
        self.input_cari_peminjam.setPlaceholderText("Ketik Nama atau ID Peminjam...")
        self.layout_peminjam.addWidget(self.input_cari_peminjam)

        self.table_peminjam = QTableWidget()
        # Di dalam setup_ui pada ui_main.py
        self.table_peminjam.setColumnCount(6)
        self.table_peminjam.setHorizontalHeaderLabels([
            "ID Pinjam", "Judul Buku", "Nama Peminjam", "Status", "Tgl Pinjam", "Tgl Kembali"
        ])
        self.table_peminjam.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_peminjam.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout_peminjam.addWidget(self.table_peminjam)

        self.stacked_widget.addWidget(self.page_peminjam)

        # ---------------------------------------------------------
        # HALAMAN 3: DATA ANGGOTA & PINJAM 
        # ---------------------------------------------------------
        self.page_3 = QWidget()
        self.verticalLayout_page3 = QVBoxLayout(self.page_3)

        # Form Peminjaman Baru (Atas)
        self.group_pinjam = QGroupBox("📝 Form Proses Peminjaman Baru")
        self.form_pinjam_layout = QFormLayout(self.group_pinjam)

        self.id_buku_pinjam = QLineEdit()
        self.id_buku_pinjam.setPlaceholderText("Masukkan ID Buku")
        self.id_user_pinjam = QLineEdit()
        self.id_user_pinjam.setReadOnly(True)
        self.id_user_pinjam.setPlaceholderText("Pilih Anggota dari tabel di bawah")
        self.status_pinjam_combo = QComboBox()
        self.status_pinjam_combo.addItems(["Dipinjam", "Kembali", "Hilang"])

        self.form_pinjam_layout.addRow("ID Buku:", self.id_buku_pinjam)
        self.form_pinjam_layout.addRow("ID Peminjam:", self.id_user_pinjam)
        self.form_pinjam_layout.addRow("Status:", self.status_pinjam_combo)

        self.btn_layout_pinjam = QHBoxLayout()
        self.btn_simpan_pinjam = QPushButton("✅ Proses Pinjam")
        self.btn_batal_pinjam = QPushButton("❌ Batal")
        self.btn_layout_pinjam.addWidget(self.btn_simpan_pinjam)
        self.btn_layout_pinjam.addWidget(self.btn_batal_pinjam)
        self.form_pinjam_layout.addRow(self.btn_layout_pinjam)

        self.verticalLayout_page3.addWidget(self.group_pinjam)

        # Tabel Daftar User
        self.verticalLayout_page3.addWidget(QLabel("👥 Daftar Seluruh Anggota:"))
        self.table_daftar_user = QTableWidget()
        self.table_daftar_user.setColumnCount(3)
        self.table_daftar_user.setHorizontalHeaderLabels(["ID User", "Username", "Nama Lengkap"])
        self.table_daftar_user.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_daftar_user.setEditTriggers(QTableWidget.NoEditTriggers)
        self.verticalLayout_page3.addWidget(self.table_daftar_user)

        self.stacked_widget.addWidget(self.page_3)

        # Status Bar
        self.statusbar = QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
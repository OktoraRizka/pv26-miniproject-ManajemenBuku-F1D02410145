from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, 
                             QHBoxLayout, QPushButton, QLabel, QTableWidget, 
                             QHeaderView, QStatusBar, QStackedWidget, QGroupBox, QFormLayout, QComboBox, QDateEdit, QHBoxLayout)

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
        self.btn_menu_daftar_user = QPushButton("👥 Data Anggota")
        self.btn_menu_daftar_user.setFixedHeight(40)
        
        self.sidebar_layout.addWidget(self.btn_menu_buku)
        self.sidebar_layout.addWidget(self.btn_menu_daftar_user)
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
        self.stok_input = QLineEdit()
        self.form_layout.addRow("Stok:", self.stok_input)
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
        self.table.setColumnCount(6) # Ubah dari 5 menjadi 6
        self.table.setHorizontalHeaderLabels(["ID", "Judul", "Tahun", "Genre", "Penulis", "Stok"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout_buku.addWidget(self.table)

        self.stacked_widget.addWidget(self.page_buku)
        
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
       
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
        
        self.table_peminjam.setEditTriggers(QTableWidget.NoEditTriggers)

        # --- (DAFTAR USER) ---
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")

        # Layout untuk halaman ketiga agar tabel memenuhi layar
        self.verticalLayout_page3 = QVBoxLayout(self.page_3)
        self.verticalLayout_page3.setObjectName(u"verticalLayout_page3")

        # Membuat Tabel Daftar User
        self.table_daftar_user = QTableWidget(self.page_3)
        self.table_daftar_user.setObjectName(u"table_daftar_user")

        # Mengatur kolom tabel
        self.table_daftar_user.setColumnCount(3)
        self.table_daftar_user.setHorizontalHeaderLabels(["ID User", "Username", "Nama Lengkap"])
        # Membuat header tabel menyesuaikan lebar jendela
        self.table_daftar_user.horizontalHeader().setStretchLastSection(True)

        # Masukkan tabel ke layout halaman
        self.verticalLayout_page3.addWidget(self.table_daftar_user)

        # MASUKKAN HALAMAN KE STACKED WIDGET
        self.stacked_widget.addWidget(self.page_3)

        # Status Bar
        self.statusbar = QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
                
                # --- BAGIAN ATAS TABLE_DAFTAR_USER ---
        self.group_pinjam = QGroupBox("Form Manajemen Peminjaman")
        self.form_pinjam_layout = QFormLayout(self.group_pinjam)

        # Input ID Buku (Bisa diganti QComboBox nanti jika ingin lebih canggih)
        self.id_buku_pinjam = QLineEdit()
        self.id_buku_pinjam.setPlaceholderText("Masukkan ID Buku")
        self.form_pinjam_layout.addRow("ID Buku:", self.id_buku_pinjam)

        # Input ID Peminjam (Otomatis terisi saat tabel diklik)
        self.id_user_pinjam = QLineEdit()
        self.id_user_pinjam.setReadOnly(True) # Biar tidak salah ketik, harus pilih dari tabel
        self.id_user_pinjam.setPlaceholderText("Klik user pada tabel di bawah")
        self.form_pinjam_layout.addRow("ID Peminjam:", self.id_user_pinjam)

        # Status Peminjaman
        self.status_pinjam_combo = QComboBox()
        self.status_pinjam_combo.addItems(["Dipinjam", "Kembali", "Hilang"])
        self.form_pinjam_layout.addRow("Status:", self.status_pinjam_combo)

        # Tombol Aksi
        self.layout_tombol_pinjam = QHBoxLayout()
        self.btn_simpan_pinjam = QPushButton("Proses Pinjam")
        self.btn_batal_pinjam = QPushButton("Batal")
        self.layout_tombol_pinjam.addWidget(self.btn_simpan_pinjam)
        self.layout_tombol_pinjam.addWidget(self.btn_batal_pinjam)
        self.form_pinjam_layout.addRow(self.layout_tombol_pinjam)

        # Masukkan GroupBox ini ke layout utama page_3 SEBELUM table_daftar_user
        self.verticalLayout_page3.insertWidget(0, self.group_pinjam)
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, 
                             QHBoxLayout, QPushButton, QLabel, QTableWidget, 
                             QHeaderView, QStatusBar)

class Ui_MainWindow:
    def setup_ui(self, MainWindow):
        MainWindow.setWindowTitle("Sistem Manajemen Buku")
        MainWindow.setGeometry(100, 100, 800, 600)
        
        self.central = QWidget()
        MainWindow.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)
        
        # ===== FORM INPUT =====
        self.form_layout = QFormLayout()
        self.judul_input = QLineEdit()
        self.judul_input.setPlaceholderText("Masukkan judul buku")
        self.form_layout.addRow("Judul Buku:", self.judul_input)
        
        self.penulis_input = QLineEdit()
        self.penulis_input.setPlaceholderText("Nama penulis")
        self.form_layout.addRow("Penulis:", self.penulis_input)
        
        self.tahun_input = QLineEdit()
        self.tahun_input.setPlaceholderText("Contoh: 2024")
        self.form_layout.addRow("Tahun Terbit:", self.tahun_input)
        
        self.genre_input = QLineEdit()
        self.genre_input.setPlaceholderText("Contoh: Fiksi, Sains, Sejarah")
        self.form_layout.addRow("Genre:", self.genre_input)
        self.layout.addLayout(self.form_layout)
        
        # ===== TOMBOL AKSI =====
        self.btn_layout = QHBoxLayout()
        self.btn_simpan = QPushButton("Simpan")
        self.btn_hapus = QPushButton("Hapus")
        self.btn_batal = QPushButton("Batal / Reset")
        
        self.btn_layout.addWidget(self.btn_simpan)
        self.btn_layout.addWidget(self.btn_hapus)
        self.btn_layout.addWidget(self.btn_batal)
        self.layout.addLayout(self.btn_layout)
        
        # ===== SEARCH =====
        self.search_layout = QHBoxLayout()
        self.search_layout.addWidget(QLabel("Cari Buku:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ketik judul, penulis, atau genre...")
        self.search_layout.addWidget(self.search_input)
        self.layout.addLayout(self.search_layout)
        
        # ===== TABEL DATA =====
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Judul", "Tahun", "Genre", "Penulis"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        
        self.layout.addWidget(self.table)
        
        self.statusbar = QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
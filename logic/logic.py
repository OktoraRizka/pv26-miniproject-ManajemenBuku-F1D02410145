import sys
from PySide6.QtWidgets import (QMainWindow, QMessageBox, QTableWidgetItem, 
                             QApplication, QHeaderView)
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QIntValidator
from ui.ui_main import Ui_MainWindow
from ui.ui_login import Ui_LoginWindow

class LoginManager(QObject):
    # Parameter diubah menjadi 'object' agar bisa mengirim satu baris DB utuh
    login_success = Signal(object)  
    login_failed = Signal(str)

    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager

    def attempt_login(self, username, password):
        if not username or not password:
            self.login_failed.emit("Username dan Password wajib diisi!")
            return

        user = self.db.check_login(username, password)

        if user:
            # Kirim seluruh objek 'user' (Row) ke Signal
            self.login_success.emit(user)
        else:
            self.login_failed.emit("Username atau Password salah!")

class LoginWindow(QMainWindow, Ui_LoginWindow):
    def __init__(self, db_manager):
        super().__init__()
        self.setup_ui(self)
        self.db = db_manager
        self.login_auth = LoginManager(self.db)
        
        self.btn_login.clicked.connect(self.on_login_click) 
        self.login_auth.login_success.connect(self.handle_success)
        self.login_auth.login_failed.connect(self.handle_error)
        
    
    def on_login_click(self):
        username = self.user_input.text().strip()
        password = self.pass_input.text().strip()
        self.login_auth.attempt_login(username, password)

    def handle_success(self, user_data):
        try:
            uid = user_data['id_user']
            u_role = user_data['role']
            u_nama = user_data['nama_lengkap']
            
            self.main_app = MainWindowLogic(self.db, u_role, uid)
            self.main_app.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error Logic", f"Gagal memproses data user: {e}")

    def handle_error(self, message):
        QMessageBox.warning(self, "Gagal", message)

class MainWindowLogic(QMainWindow, Ui_MainWindow):
    def __init__(self, db_manager, role, user_id):
        super().__init__()
        self.setup_ui(self)
        self.db = db_manager
        self.role = role 
        self.current_user_id = user_id
        self.selected_id = None
        # Validator Input (Hanya Angka)
        self.stok_input.setValidator(QIntValidator(0, 999))
        self.tahun_input.setValidator(QIntValidator(1000, 2099))
        
        # 1. Koneksi Navigasi Menu Bar (Ganti dari .clicked ke .triggered)
        self.action_manajemen_buku.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.action_data_peminjam.triggered.connect(self.buka_menu_peminjam)
        self.action_data_anggota.triggered.connect(self.buka_menu_daftar_user)
        self.action_exit.triggered.connect(self.close) 

        # 2. Koneksi Tombol CRUD & Form Peminjaman
        self.btn_simpan.clicked.connect(self.simpan_data)
        self.btn_hapus.clicked.connect(self.hapus_data)
        self.btn_batal.clicked.connect(self.batal_edit)
        self.btn_simpan_pinjam.clicked.connect(self.simpan_peminjaman_admin)
        self.btn_batal_pinjam.clicked.connect(self.reset_form_pinjam)
        
        # 3. Fitur Tabel & Pencarian
        self.table.clicked.connect(self.isi_form_dari_tabel)
        self.table_daftar_user.clicked.connect(self.pilih_user_untuk_pinjam)
        self.search_input.textChanged.connect(self.cari_data)
        self.input_cari_peminjam.textChanged.connect(self.cari_peminjam)
        
        self.action_about.triggered.connect(self.tampilkan_tentang_aplikasi)
        
        # 4. Inisialisasi Tampilan
        self.atur_hak_akses()
        self.load_data()
        
            
    def atur_hak_akses(self):
        """Mengatur visibilitas menu dan tombol berdasarkan role"""
        if self.role == "Peminjam":
            # Sembunyikan menu Data Anggota (Action, bukan Button)
            self.action_data_anggota.setVisible(False)
            
            # Kunci input manajemen buku
            self.btn_simpan.hide()
            self.btn_hapus.hide()
            self.btn_batal.hide()
            self.judul_input.setDisabled(True)
            self.tahun_input.setDisabled(True)
            self.genre_input.setDisabled(True)
            self.penulis_input.setDisabled(True)
            self.stok_input.setDisabled(True)
            self.setWindowTitle("Katalog Perpustakaan - Mode Peminjam")
        else:
            self.action_data_anggota.setVisible(True)
            self.setWindowTitle(f"Sistem Manajemen Perpustakaan - {self.role}")

    def load_data(self, data_buku=None):
        if data_buku is None:
            data_buku = self.db.ambil_semua_buku()
        
        self.table.setRowCount(0)
        for row_data in data_buku:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(row_data['id_buku'])))
            self.table.setItem(row, 1, QTableWidgetItem(row_data['judul_buku']))
            self.table.setItem(row, 2, QTableWidgetItem(str(row_data['tahun_terbit'])))
            self.table.setItem(row, 3, QTableWidgetItem(row_data['genre_buku']))
            self.table.setItem(row, 4, QTableWidgetItem(row_data['penulis']))
            self.table.setItem(row, 5, QTableWidgetItem(str(row_data['stok'])))
        self.statusbar.showMessage(f"Total Koleksi: {len(data_buku)} Buku")

    def simpan_data(self):
        judul = self.judul_input.text().strip()
        penulis = self.penulis_input.text().strip()
        tahun = self.tahun_input.text().strip()
        genre = self.genre_input.text().strip()
        stok = self.stok_input.text().strip()

        if not judul or not penulis:
            QMessageBox.warning(self, "Peringatan", "Judul dan Penulis wajib diisi!")
            return

        try:
            if self.selected_id is None:
                self.db.tambah_buku(judul, tahun, genre, penulis, stok)
                self.statusbar.showMessage("Buku berhasil ditambahkan", 3000)
            else:
                self.db.update_buku(self.selected_id, judul, tahun, genre, penulis, stok)
                self.statusbar.showMessage("Data buku diperbarui", 3000)
            
            self.batal_edit()
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal simpan: {e}")

    def isi_form_dari_tabel(self):
        row = self.table.currentRow()
        if row >= 0:
            self.selected_id = int(self.table.item(row, 0).text())
            self.judul_input.setText(self.table.item(row, 1).text())
            self.tahun_input.setText(self.table.item(row, 2).text())
            self.genre_input.setText(self.table.item(row, 3).text())
            self.penulis_input.setText(self.table.item(row, 4).text())
            self.stok_input.setText(self.table.item(row, 5).text())
            self.btn_simpan.setText("Update Data")

    def buka_menu_peminjam(self):
        self.stacked_widget.setCurrentIndex(1)
        self.load_data_peminjam()
    
    def load_data_peminjam(self):
        data = self.db.ambil_semua_peminjaman() if self.role == "Super Admin" else \
               self.db.ambil_peminjaman_by_user(self.current_user_id)
        
        self.table_peminjam.setRowCount(0)
        for row_data in data:
            row = self.table_peminjam.rowCount()
            self.table_peminjam.insertRow(row)
            self.table_peminjam.setItem(row, 0, QTableWidgetItem(str(row_data['id_pinjam'])))
            self.table_peminjam.setItem(row, 1, QTableWidgetItem(row_data['judul_buku']))
            self.table_peminjam.setItem(row, 2, QTableWidgetItem(str(row_data['nama_lengkap'])))
            self.table_peminjam.setItem(row, 3, QTableWidgetItem(row_data['status']))

    def buka_menu_daftar_user(self):
        self.stacked_widget.setCurrentIndex(2)
        self.load_daftar_user()
        
    def load_daftar_user(self):
        data = self.db.ambil_semua_peminjam_user()
        self.table_daftar_user.setRowCount(0)
        for row_data in data:
            row = self.table_daftar_user.rowCount()
            self.table_daftar_user.insertRow(row)
            self.table_daftar_user.setItem(row, 0, QTableWidgetItem(str(row_data['id_user'])))
            self.table_daftar_user.setItem(row, 1, QTableWidgetItem(row_data['username']))
            self.table_daftar_user.setItem(row, 2, QTableWidgetItem(row_data['nama_lengkap']))
            
    def tampilkan_tentang_aplikasi(self):
        """Menampilkan kotak dialog informasi aplikasi dan pengembang"""
        info_teks = (
            "<h3>Sistem Manajemen Perpustakaan V1.0</h3>"
            "<p>Aplikasi Manajemen buku, "
            "data anggota, dan transaksi peminjaman secara efisien.</p>"
            "<hr>"
            "<b>Dikembangkan oleh:</b><br>"
            "Nama: Oktora Rizka Arifin<br>"
            "NIM: F1D02410145<br>"
            "Prodi: Teknik Informatika, Universitas Mataram"
        )
        
        QMessageBox.about(self, "Tentang Aplikasi", info_teks)

    def pilih_user_untuk_pinjam(self):
        row = self.table_daftar_user.currentRow()
        if row >= 0:
            id_user = self.table_daftar_user.item(row, 0).text()
            self.id_user_pinjam.setText(id_user)

    def simpan_peminjaman_admin(self):
        id_buku = self.id_buku_pinjam.text().strip()
        id_user = self.id_user_pinjam.text().strip()
        status = self.status_pinjam_combo.currentText()

        if not id_buku or not id_user:
            QMessageBox.warning(self, "Peringatan", "Pilih User dan masukkan ID Buku!")
            return

        try:
            self.db.proses_peminjaman_baru(id_buku, id_user, status)
            QMessageBox.information(self, "Sukses", "Peminjaman berhasil dicatat!")
            self.reset_form_pinjam()
            self.load_data() 
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal: {e}")

    def reset_form_pinjam(self):
        self.id_buku_pinjam.clear()
        self.id_user_pinjam.clear()
        self.status_pinjam_combo.setCurrentIndex(0)

    def cari_data(self):
        keyword = self.search_input.text()
        self.load_data(self.db.cari_buku(keyword))

    def cari_peminjam(self):
        keyword = self.input_cari_peminjam.text()
        data = self.db.cari_peminjaman(keyword)
        self.table_peminjam.setRowCount(0)
        for row_data in data:
            row = self.table_peminjam.rowCount()
            self.table_peminjam.insertRow(row)
            self.table_peminjam.setItem(row, 0, QTableWidgetItem(str(row_data['id_pinjam'])))
            self.table_peminjam.setItem(row, 1, QTableWidgetItem(row_data['judul_buku']))
            self.table_peminjam.setItem(row, 2, QTableWidgetItem(str(row_data['nama_lengkap'])))
            self.table_peminjam.setItem(row, 3, QTableWidgetItem(row_data['status']))

    def batal_edit(self):
        self.selected_id = None
        self.judul_input.clear()
        self.penulis_input.clear()
        self.tahun_input.clear()
        self.genre_input.clear()
        self.stok_input.clear()
        self.btn_simpan.setText("Simpan")
        self.table.clearSelection()

    def hapus_data(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Peringatan", "Pilih buku dahulu!")
            return
        if QMessageBox.question(self, "Konfirmasi", "Hapus buku ini?", 
                               QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.db.hapus_buku(self.selected_id)
            self.batal_edit()
            self.load_data()
                 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowLogic()
    window.show()
    sys.exit(app.exec())
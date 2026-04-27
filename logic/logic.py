import sys
from PySide6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QApplication
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QIntValidator
from ui.ui_main import Ui_MainWindow
from ui.ui_login import Ui_LoginWindow # Asumsi Anda buat file UI login

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
        # Sekarang user_data adalah sqlite3.Row, akses pakai Nama Kolom!
        try:
            uid = user_data['id_user']      # Pastikan nama kolom di DB id_user
            u_role = user_data['role']
            u_nama = user_data['nama_lengkap']
            
            print(f"DEBUG - Login Sukses: {u_nama} (ID: {uid})")
            
            # Kirim data ke MainWindow
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
        self.stok_input.setValidator(QIntValidator(0, 999)) # Hanya angka 0-999
        self.tahun_input.setValidator(QIntValidator(1000, 2099))
        
        # Klik tabel user untuk isi ID Peminjam di form
        self.table_daftar_user.clicked.connect(self.pilih_user_untuk_pinjam)

        # Klik tombol simpan pinjaman
        self.btn_simpan_pinjam.clicked.connect(self.simpan_peminjaman_admin)
        self.btn_batal_pinjam.clicked.connect(self.reset_form_pinjam)
        
        # 1. Atur Tampilan Berdasarkan Role
        self.atur_hak_akses()
        
        # 2. Koneksi Navigasi Sidebar
        self.btn_menu_buku.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_menu_anggota.clicked.connect(self.buka_menu_peminjam)
        
        # 3. Koneksi Tombol CRUD
        self.btn_simpan.clicked.connect(self.simpan_data)
        self.btn_hapus.clicked.connect(self.hapus_data)
        self.btn_batal.clicked.connect(self.batal_edit)
        
        # 4. Fitur Pencarian & Klik Tabel
        self.search_input.textChanged.connect(self.cari_data)
        self.table.clicked.connect(self.isi_form_dari_tabel)
        # Pastikan nama widget search di halaman peminjam benar (search_peminjam atau input_cari_peminjam)
        self.input_cari_peminjam.textChanged.connect(self.cari_peminjam)
        
        self.btn_menu_daftar_user.clicked.connect(self.buka_menu_daftar_user)   
        
        # 5. Load Data Awal
        self.load_data()
    
    def buka_menu_peminjam(self):
        self.stacked_widget.setCurrentIndex(1)
        self.load_data_peminjam()
    
    def load_data_peminjam(self):
        if self.role == "Super Admin":
            data = self.db.ambil_semua_peminjaman()
        else:
            data = self.db.ambil_peminjaman_by_user(self.current_user_id)
        
        self.table_peminjam.setRowCount(0)
        for row_data in data:
            row = self.table_peminjam.rowCount()
            self.table_peminjam.insertRow(row)
            # Gunakan key dict karena sudah pakai row_factory = sqlite3.Row
            self.table_peminjam.setItem(row, 0, QTableWidgetItem(str(row_data['id_pinjam'])))
            self.table_peminjam.setItem(row, 1, QTableWidgetItem(row_data['judul_buku']))
            self.table_peminjam.setItem(row, 2, QTableWidgetItem(str(row_data['nama_lengkap'])))
            self.table_peminjam.setItem(row, 3, QTableWidgetItem(row_data['status']))
    
    def pinjam_buku(self):
        # 1. Pastikan ada buku yang dipilih di tabel
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih buku yang ingin dipinjam!")
            return
        
        id_buku = self.table.item(row, 0).text()
        
        # 2. Cek stok buku ke database
        buku = self.db.ambil_buku_by_id(id_buku) # Anda perlu buat fungsi ini di db_buku.py
        
        if buku['stok'] > 0:
            # 3. Jalankan transaksi (Simpan ke tabel peminjaman & Kurangi stok)
            nim = "12345" # Contoh, nantinya bisa diambil dari input atau data login
            if self.db.catat_peminjaman(id_buku, nim):
                QMessageBox.information(self, "Sukses", "Buku berhasil dipinjam!")
                self.load_data() # Refresh tabel agar stok terbaru muncul
            else:
                QMessageBox.critical(self, "Error", "Gagal memproses peminjaman.")
        else:
            QMessageBox.warning(self, "Stok Habis", "Maaf, stok buku ini sedang kosong!")
    
    def cari_peminjam(self):
        keyword = self.input_cari_peminjam.text()
        data = self.db.cari_peminjaman(keyword)
        # Update tabel peminjam dengan hasil cari
        self.table_peminjam.setRowCount(0)
        for row_data in data:
            row = self.table_peminjam.rowCount()
            self.table_peminjam.insertRow(row)
            self.table_peminjam.setItem(row, 0, QTableWidgetItem(str(row_data['id_pinjam'])))
            self.table_peminjam.setItem(row, 1, QTableWidgetItem(row_data['judul_buku']))
            self.table_peminjam.setItem(row, 2, QTableWidgetItem(str(row_data['nama_lengkap'])))
            self.table_peminjam.setItem(row, 3, QTableWidgetItem(row_data['status']))

    def atur_hak_akses(self):
        if self.role == "Peminjam":
            self.btn_simpan.hide()
            self.btn_hapus.hide()
            self.btn_batal.hide()
            self.judul_input.setDisabled(True)
            self.tahun_input.setDisabled(True)
            self.genre_input.setDisabled(True)
            self.penulis_input.setDisabled(True)
            self.stok_input.setDisabled(True)
            self.btn_menu_daftar_user.hide()
            self.setWindowTitle("Katalog Perpustakaan - Mode Peminjam")
        elif self.role == "Super Admin":
            self.btn_menu_daftar_user.show()
        else:
            self.setWindowTitle("Sistem Manajemen Perpustakaan - Super Admin")
            
                        
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
            self.table.setItem(row, 5, QTableWidgetItem(row_data['stok']))

    def simpan_data(self):
        judul = self.judul_input.text()
        penulis = self.penulis_input.text()
        tahun = self.tahun_input.text()
        genre = self.genre_input.text()
        genre = self.stok_input.text()

        if not judul or not penulis:
            QMessageBox.warning(self, "Peringatan", "Judul dan Penulis wajib diisi!")
            return

        try:
            if self.selected_id is None:
                self.db.tambah_buku(judul, tahun, genre, penulis)
                self.statusbar.showMessage("Buku berhasil ditambahkan", 3000)
            else:
                self.db.update_buku(self.selected_id, judul, tahun, genre, penulis)
                self.statusbar.showMessage("Data buku diperbarui", 3000)
            
            self.batal_edit()
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal simpan: {e}")

    def hapus_data(self):
        if self.selected_id is None:
            QMessageBox.warning(self, "Peringatan", "Pilih buku dahulu!")
            return
        
        confirm = QMessageBox.question(self, "Konfirmasi", "Hapus buku ini?", 
                                     QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.db.hapus_buku(self.selected_id)
            self.batal_edit()
            self.load_data()

    def isi_form_dari_tabel(self):
        row = self.table.currentRow()
        if row >= 0:
            self.selected_id = int(self.table.item(row, 0).text())
            self.judul_input.setText(self.table.item(row, 1).text())
            self.tahun_input.setText(self.table.item(row, 2).text())
            self.genre_input.setText(self.table.item(row, 3).text())
            self.penulis_input.setText(self.table.item(row, 4).text())
            self.stok_input.setText(self.table.item(row, 5).text())
            
            # Ambil stok dari kolom ke-5 (indeks 5)
            stok_val = self.table.item(row, 5).text() if self.table.item(row, 5) else "0"
            self.stok_input.setText(stok_val)
            
            self.btn_simpan.setText("Update Data")

    def cari_data(self):
        keyword = self.search_input.text()
        hasil = self.db.cari_buku(keyword)
        self.load_data(hasil)

    def batal_edit(self):
        self.selected_id = None
        self.judul_input.clear()
        self.tahun_input.clear()
        self.genre_input.clear()
        self.penulis_input.clear()
        self.stok_input.clear()
        self.btn_simpan.setText("Simpan")
        self.table.clearSelection()
        
    # ============================
    # OPERASI CRUD MANAJEMEN BUKU
    # ============================
    
    def load_data(self, data=None):
        """Ambil semua data dari DB dan tampilkan ke tabel"""
        if data is None:
            data = self.db.ambil_semua_buku()
        
        self.tampilkan_ke_tabel(data)
        self.statusbar.showMessage(f"Total Koleksi: {len(data)} Buku")
    
    def tampilkan_ke_tabel(self, data):
        """Mengisi tabel dengan data buku"""
        self.table.setRowCount(0)  # Kosongkan tabel dulu
        
        for row_data in data:
            row = self.table.rowCount()
            self.table.insertRow(row)
            # Menyesuaikan dengan index kolom: 0:ID, 1:Judul, 2:Tahun, 3:Genre, 4:Penulis
            self.table.setItem(row, 0, QTableWidgetItem(str(row_data['id_buku'])))
            self.table.setItem(row, 1, QTableWidgetItem(row_data['judul_buku']))
            self.table.setItem(row, 2, QTableWidgetItem(str(row_data['tahun_terbit'])))
            self.table.setItem(row, 3, QTableWidgetItem(row_data['genre_buku']))
            self.table.setItem(row, 4, QTableWidgetItem(row_data['penulis']))
            self.table.setItem(row, 5, QTableWidgetItem(str(row_data['stok'])))
    
    def simpan_data(self):
        judul = self.judul_input.text().strip()
        penulis = self.penulis_input.text().strip()
        tahun = self.tahun_input.text().strip()
        genre = self.genre_input.text().strip()
        stok = self.stok_input.text().strip() # Ambil input stok

        if not judul or not penulis:
            QMessageBox.warning(self, "Peringatan", "Judul dan Penulis harus diisi!")
            return

        try:
            if self.selected_id:
                # Kirim variabel stok ke fungsi update_buku
                self.db.update_buku(self.selected_id, judul, tahun, genre, penulis, stok)
                self.statusbar.showMessage("Data buku berhasil diperbarui", 3000)
            else:
                # Jika tambah buku baru, pastikan fungsi tambah_buku juga mendukung stok
                self.db.tambah_buku(judul, tahun, genre, penulis, stok)
                self.statusbar.showMessage("Buku baru berhasil ditambahkan", 3000)
            
            self.batal_edit()
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal simpan: {e}")
    
    def hapus_data(self):
        """Hapus buku yang dipilih di tabel"""
        if not self.selected_id:
            QMessageBox.warning(self, "Peringatan", "Pilih buku di tabel yang akan dihapus!")
            return
        
        reply = QMessageBox.question(
            self, "Konfirmasi Hapus",
            "Yakin ingin menghapus buku ini dari koleksi?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.db.hapus_buku(self.selected_id)
            self.batal_edit()
            self.load_data()
            self.statusbar.showMessage("Buku berhasil dihapus", 3000)
    
    def cari_data(self):
        """Cari buku berdasarkan keyword (Judul/Penulis)"""
        keyword = self.search_input.text().strip()
        if keyword:
            data = self.db.cari_buku(keyword)
        else:
            data = self.db.ambil_semua_buku()
        self.tampilkan_ke_tabel(data)
    
    def isi_form_dari_tabel(self):
        """Saat baris di tabel diklik, isi form dengan data buku tersebut"""
        row = self.table.currentRow()
        if row >= 0:
            self.selected_id = int(self.table.item(row, 0).text())
            self.judul_input.setText(self.table.item(row, 1).text())
            self.tahun_input.setText(self.table.item(row, 2).text())
            self.genre_input.setText(self.table.item(row, 3).text())
            self.penulis_input.setText(self.table.item(row, 4).text())
            self.stok_input.setText(self.table.item(row, 5).text())
            
            self.btn_simpan.setText("Update Data")
            self.statusbar.showMessage(f"Mengedit Buku ID: {self.selected_id}")
    
    def batal_edit(self):
        """Reset form ke mode tambah baru"""
        self.selected_id = None
        self.judul_input.clear()
        self.penulis_input.clear()
        self.tahun_input.clear()
        self.genre_input.clear()
        self.stok_input.clear()
        
        self.btn_simpan.setText("Simpan")
        self.table.clearSelection()
        self.statusbar.showMessage("Siap")
        
        
    def buka_menu_daftar_user(self):
    # Pindah ke halaman index 2 (Halaman baru Anda)
        self.stacked_widget.setCurrentIndex(2)
        self.load_daftar_user()
        
    def load_daftar_user(self):
        # Ambil data dari database
        data = self.db.ambil_semua_peminjam_user()
        
        self.table_daftar_user.setRowCount(0)
        self.table_daftar_user.setColumnCount(3)
        self.table_daftar_user.setHorizontalHeaderLabels(["ID", "Username", "Nama Lengkap"])

        for row_data in data:
            row = self.table_daftar_user.rowCount()
            self.table_daftar_user.insertRow(row)
            self.table_daftar_user.setItem(row, 0, QTableWidgetItem(str(row_data['id_user'])))
            self.table_daftar_user.setItem(row, 1, QTableWidgetItem(row_data['username']))
            self.table_daftar_user.setItem(row, 2, QTableWidgetItem(row_data['nama_lengkap']))
            
    def pilih_user_untuk_pinjam(self):
        """Mengambil ID User dari tabel daftar_user ke form input"""
        row = self.table_daftar_user.currentRow()
        if row >= 0:
            id_user = self.table_daftar_user.item(row, 0).text()
            self.id_user_pinjam.setText(id_user)
            self.statusbar.showMessage(f"Menyiapkan peminjaman untuk User ID: {id_user}")

    def simpan_peminjaman_admin(self):
        id_buku = self.id_buku_pinjam.text().strip()
        id_user = self.id_user_pinjam.text().strip()
        status = self.status_pinjam_combo.currentText()

        if not id_buku or not id_user:
            QMessageBox.warning(self, "Peringatan", "Pilih User dan masukkan ID Buku!")
            return

        try:
            self.db.proses_peminjaman_baru(id_buku, id_user, status)
            QMessageBox.information(self, "Sukses", "Data peminjaman berhasil dicatat!")
            self.reset_form_pinjam()
            self.load_data() # Refresh stok di tabel buku
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal: {e}")

    def reset_form_pinjam(self):
        self.id_buku_pinjam.clear()
        self.id_user_pinjam.clear()
        self.status_pinjam_combo.setCurrentIndex(0)
            
    

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowLogic()
    window.show()
    sys.exit(app.exec())
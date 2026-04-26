import sys
from PySide6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QApplication
from PySide6.QtCore import QObject, Signal
from ui.ui_main import Ui_MainWindow
from ui.ui_login import Ui_LoginWindow # Asumsi Anda buat file UI login

class LoginManager(QObject):
    login_success = Signal(str) # Mengirim nama lengkap admin
    login_failed = Signal(str)

    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager

    def attempt_login(self, username, password):
        # Validasi input kosong
        if not username or not password:
            self.login_failed.emit("Username dan Password wajib diisi!")
            return

        # Cek ke Database
        user = self.db.check_login(username, password)

        if user:
            # Jika ditemukan, kirim sinyal sukses dengan nama lengkapnya
            self.login_success.emit(user['nama_lengkap'])
        else:
            # Jika tidak ada, kirim sinyal gagal
            self.login_failed.emit("Username atau Password salah!")
            
class LoginWindow(QMainWindow, Ui_LoginWindow):
    def __init__(self, db_manager):
        super().__init__()
        self.setup_ui(self)
        self.db = db_manager
        self.login_auth = LoginManager(self.db)
        
        # Baris yang menyebabkan error (pastikan nama fungsinya sama)
        self.btn_login.clicked.connect(self.on_login_click) 
        
        self.login_auth.login_success.connect(self.handle_success)
        self.login_auth.login_failed.connect(self.handle_error)
    
    def on_login_click(self):
        username = self.user_input.text().strip()
        password = self.pass_input.text().strip()
        
        # Memanggil fungsi attempt_login dari LoginManager
        self.login_auth.attempt_login(username, password)

    def handle_success(self, nama):
        QMessageBox.information(self, "Sukses", f"Selamat datang, {nama}")
        self.main_app = MainWindowLogic(self.db)
        self.main_app.show()
        self.close()

    def handle_error(self, message):
        QMessageBox.warning(self, "Gagal", message)


class MainWindowLogic(QMainWindow, Ui_MainWindow):
    def __init__(self, db_manager):
        super().__init__()
        self.setup_ui(self)
        self.db = db_manager # Menerima database dari main.py
        self.selected_id = None
        
        # Signal & Slots
        self.btn_simpan.clicked.connect(self.simpan_data)
        self.btn_hapus.clicked.connect(self.hapus_data)
        self.btn_batal.clicked.connect(self.batal_edit)
        self.search_input.textChanged.connect(self.cari_data)
        self.table.clicked.connect(self.isi_form_dari_tabel)
        
        self.load_data()

    # ... (lanjutkan dengan fungsi load_data, simpan_data, dll seperti kode sebelumnya)

    def load_data(self, data_buku=None):
        if data_buku is None:
            data_buku = self.db.ambil_semua_buku()
        self.table.setRowCount(0)
        for row_idx, row_data in enumerate(data_buku):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(row_data['id_buku'])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(row_data['judul_buku']))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(row_data['tahun_terbit'])))
            self.table.setItem(row_idx, 3, QTableWidgetItem(row_data['genre_buku']))
            self.table.setItem(row_idx, 4, QTableWidgetItem(row_data['penulis']))

    def simpan_data(self):
        judul = self.judul_input.text()
        penulis = self.penulis_input.text()
        tahun = self.tahun_input.text()
        genre = self.genre_input.text()

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
        self.selected_id = int(self.table.item(row, 0).text())
        self.judul_input.setText(self.table.item(row, 1).text())
        self.tahun_input.setText(self.table.item(row, 2).text())
        self.genre_input.setText(self.table.item(row, 3).text())
        self.penulis_input.setText(self.table.item(row, 4).text())
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
    
    def simpan_data(self):
        """Simpan buku baru atau update data buku yang sudah dipilih"""
        judul = self.judul_input.text().strip()
        penulis = self.penulis_input.text().strip()
        tahun = self.tahun_input.text().strip()
        genre = self.genre_input.text().strip()
        
        # Validasi minimal
        if not judul or not penulis:
            QMessageBox.warning(self, "Peringatan", "Judul dan Penulis harus diisi!")
            return
        
        try:
            if self.selected_id:
                # MODE UPDATE
                self.db.update_buku(self.selected_id, judul, tahun, genre, penulis)
                self.statusbar.showMessage("Data buku berhasil diperbarui", 3000)
            else:
                # MODE TAMBAH
                self.db.tambah_buku(judul, tahun, genre, penulis)
                self.statusbar.showMessage("Buku baru berhasil ditambahkan", 3000)
            
            self.batal_edit()   # Reset form
            self.load_data()    # Refresh tabel
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan saat menyimpan:\n{e}")
    
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
            
            self.btn_simpan.setText("Update Data")
            self.statusbar.showMessage(f"Mengedit Buku ID: {self.selected_id}")
    
    def batal_edit(self):
        """Reset form ke mode tambah baru"""
        self.selected_id = None
        self.judul_input.clear()
        self.penulis_input.clear()
        self.tahun_input.clear()
        self.genre_input.clear()
        
        self.btn_simpan.setText("Simpan")
        self.table.clearSelection()
        self.statusbar.showMessage("Siap")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowLogic()
    window.show()
    sys.exit(app.exec())
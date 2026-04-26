import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name='database_buku.db'):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, db_name)
        self.create_table()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create_table(self):
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS buku (
                    id_buku INTEGER PRIMARY KEY AUTOINCREMENT,
                    judul_buku TEXT NOT NULL,
                    tahun_terbit INTEGER,
                    genre_buku TEXT,
                    penulis TEXT NOT NULL,
                    stok INTEGER DEFAULT 0
                )
            ''')
            
            conn.execute('''
            CREATE TABLE IF NOT EXISTS peminjaman (
                id_pinjam INTEGER PRIMARY KEY AUTOINCREMENT,
                id_buku INTEGER,
                nim_peminjam TEXT NOT NULL,
                tgl_pinjam TEXT NOT NULL,
                tgl_kembali_seharusnya TEXT NOT NULL,
                tgl_kembali_aktual TEXT,
                status TEXT DEFAULT 'Dipinjam',
                FOREIGN KEY (id_buku) REFERENCES buku (id_buku)
            )
            ''')
            
            cek = conn.execute("SELECT COUNT(*) FROM peminjaman").fetchone()[0]
        
            if cek == 0:
                # Masukkan data dummy
                conn.execute('''
                    INSERT INTO peminjaman (id_buku, nim_peminjam, tgl_pinjam, tgl_kembali_seharusnya, status)
                    VALUES (?, ?, ?, ?, ?)
                ''', (1, 'F1D02410145', '2026-04-26', '2026-05-03', 'Dipinjam'))
                print("Data peminjaman awal berhasil ditambahkan!")
            
            conn.execute('''
            CREATE TABLE IF NOT EXISTS admin (
                id_admin INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                nama_lengkap TEXT,
                role TEXT DEFAULT 'Petugas'
            )
            ''')
            
            conn.execute('''
            INSERT OR IGNORE INTO admin (username, password, nama_lengkap, role)
            VALUES (?, ?, ?, ?)
             ''', ('peminjam1', '12345', 'Oktora Rizka', 'Peminjam'))
        
            # Opsional: Membuat admin default jika tabel masih kosong
            # Agar Anda bisa login untuk pertama kali
            admin_ada = conn.execute('SELECT COUNT(*) FROM admin').fetchone()[0]
            if admin_ada == 0:
                conn.execute('''
                    INSERT INTO admin (username, password, nama_lengkap, role)
                    VALUES (?, ?, ?, ?)
                ''', ('admin', 'admin123', 'Administrator Utama', 'Super Admin'))
            
            
                
    def check_login(self, username, password):
        with self.get_connection() as conn:
            # Mencari user yang username DAN passwordnya cocok
            query = "SELECT * FROM admin WHERE username = ? AND password = ?"
            return conn.execute(query, (username, password)).fetchone()
            
    
    def tambah_buku(self, judul, tahun, genre, penulis):
        with self.get_connection() as conn:
            conn.execute('''
                INSERT INTO buku (judul_buku, tahun_terbit, genre_buku, penulis) 
                VALUES (?, ?, ?, ?)
            ''', (judul, tahun, genre, penulis))
    
    def ambil_semua_buku(self):
        with self.get_connection() as conn:
            # Mengurutkan berdasarkan judul buku agar tampilan di GUI lebih rapi
            return conn.execute('SELECT * FROM buku ORDER BY judul_buku').fetchall()
    
    def cari_buku(self, keyword):
        with self.get_connection() as conn:
            # Mencari berdasarkan judul atau penulis
            query = '''
                SELECT * FROM buku 
                WHERE judul_buku LIKE ? OR penulis LIKE ? OR genre_buku LIKE ?
            '''
            wildcard = f'%{keyword}%'
            return conn.execute(query, (wildcard, wildcard, wildcard)).fetchall()
    
    def update_buku(self, id_buku, judul, tahun, genre, penulis):
        with self.get_connection() as conn:
            conn.execute('''
                UPDATE buku 
                SET judul_buku=?, tahun_terbit=?, genre_buku=?, penulis=? 
                WHERE id_buku=?
            ''', (judul, tahun, genre, penulis, id_buku))
    
    def hapus_buku(self, id_buku):
        with self.get_connection() as conn:
            conn.execute('DELETE FROM buku WHERE id_buku = ?', (id_buku,))
    
    def ambil_semua_peminjaman(self):
        with self.get_connection() as conn:
            # Kita gunakan JOIN agar bisa menampilkan Judul Buku, bukan cuma ID-nya
            query = '''
                SELECT p.id_pinjam, b.judul_buku, p.nim_peminjam, p.status 
                FROM peminjaman p
                JOIN buku b ON p.id_buku = b.id_buku
            '''
            return conn.execute(query).fetchall()

    def cari_peminjaman(self, keyword):
        with self.get_connection() as conn:
            query = "SELECT * FROM peminjaman WHERE nim_peminjam LIKE ?"
            return conn.execute(query, (f'%{keyword}%',)).fetchall()

# Contoh Penggunaan:
if __name__ == "__main__":
    db = DatabaseManager()
    # db.tambah_buku("Laskar Pelangi", 2005, "Fiksi", "Andrea Hirata")
    print("Database siap digunakan!")
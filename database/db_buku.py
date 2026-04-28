import sqlite3
import os
import datetime

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
                CREATE TABLE IF NOT EXISTS user (
                    id_user INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    nama_lengkap TEXT,
                    role TEXT DEFAULT 'Petugas'
                )
            ''')
            
            conn.execute('''
            CREATE TABLE IF NOT EXISTS peminjaman (
                id_pinjam INTEGER PRIMARY KEY AUTOINCREMENT,
                id_buku INTEGER,
                id_peminjam INTEGER NOT NULL, 
                tgl_pinjam TEXT NOT NULL,
                tgl_kembali_seharusnya TEXT NOT NULL,
                tgl_kembali_aktual TEXT,
                status TEXT DEFAULT 'Dipinjam',
                FOREIGN KEY (id_buku) REFERENCES buku (id_buku),
                FOREIGN KEY (id_peminjam) REFERENCES user (id_user)
            )
            ''')
        

    def check_login(self, username, password):
        with self.get_connection() as conn:
            query = "SELECT * FROM user WHERE username = ? AND password = ?"
            print(conn.execute(query, (username, password)).fetchone())
            return conn.execute(query, (username, password)).fetchone()
        
            
    def tambah_buku(self, judul, tahun, genre, penulis, stok):
        with self.get_connection() as conn:
            conn.execute('''
                INSERT INTO buku (judul_buku, tahun_terbit, genre_buku, penulis, stok) 
                VALUES (?, ?, ?, ?, ?)
            ''', (judul, tahun, genre, penulis, stok))
    
    def ambil_semua_buku(self):
        with self.get_connection() as conn:
            return conn.execute('SELECT * FROM buku ORDER BY judul_buku').fetchall()
    
    def cari_buku(self, keyword):
        with self.get_connection() as conn:
            query = '''
                SELECT * FROM buku 
                WHERE judul_buku LIKE ? OR penulis LIKE ? OR genre_buku LIKE ?
            '''
            wildcard = f'%{keyword}%'
            return conn.execute(query, (wildcard, wildcard, wildcard)).fetchall()
    
    def update_buku(self, id_buku, judul, tahun, genre, penulis, stok):
        with self.get_connection() as conn:
            conn.execute('''
                UPDATE buku 
                SET judul_buku=?, tahun_terbit=?, genre_buku=?, penulis=?, stok=? 
                WHERE id_buku=?
            ''', (judul, tahun, genre, penulis, stok, id_buku))
    
    def hapus_buku(self, id_buku):
        with self.get_connection() as conn:
            conn.execute('DELETE FROM buku WHERE id_buku = ?', (id_buku,))
    
    def ambil_semua_peminjaman(self):
        with self.get_connection() as conn:
            query = """
                SELECT p.id_pinjam, b.judul_buku, u.nama_lengkap, p.status, 
                    p.tgl_pinjam, p.tgl_kembali_seharusnya 
                FROM peminjaman p
                JOIN buku b ON p.id_buku = b.id_buku
                JOIN user u ON p.id_peminjam = u.id_user
            """
            return conn.execute(query).fetchall()
    
    def ambil_peminjaman_by_user(self, user_id):
        with self.get_connection() as conn:
            query = """
                SELECT p.id_pinjam, b.judul_buku, u.nama_lengkap, p.status, 
                    p.tgl_pinjam, p.tgl_kembali_seharusnya 
                FROM peminjaman p
                JOIN buku b ON p.id_buku = b.id_buku
                JOIN user u ON p.id_peminjam = u.id_user
                WHERE p.id_peminjam = ?
            """
            return conn.execute(query, (user_id,)).fetchall()

    def cari_peminjaman(self, keyword):
        with self.get_connection() as conn:
            query = '''
                SELECT p.id_pinjam, b.judul_buku, u.nama_lengkap, p.status 
                FROM peminjaman p
                JOIN buku b ON p.id_buku = b.id_buku
                JOIN user u ON p.id_peminjam = u.id_user
                WHERE u.nama_lengkap LIKE ? OR b.judul_buku LIKE ?
            '''
            wildcard = f'%{keyword}%'
            return conn.execute(query, (wildcard, wildcard)).fetchall()
        
    def ambil_semua_peminjam_user(self):
        with self.get_connection() as conn:
            # Hanya mengambil user dengan role Peminjam
            query = "SELECT id_user, username, nama_lengkap, role FROM user WHERE role = 'Peminjam'"
            return conn.execute(query).fetchall()
        
    def proses_peminjaman_baru(self, id_buku, id_user, status):
        with self.get_connection() as conn:
            tgl_sekarang = datetime.date.today().strftime("%Y-%m-%d")
            tgl_kembali = (datetime.date.today() + datetime.timedelta(days=7)).strftime("%Y-%m-%d")
            
            query = '''
                INSERT INTO peminjaman (id_buku, id_peminjam, tgl_pinjam, tgl_kembali_seharusnya, status)
                VALUES (?, ?, ?, ?, ?)
            '''
            conn.execute(query, (id_buku, id_user, tgl_sekarang, tgl_kembali, status))
            
            # Opsi: Kurangi stok buku secara otomatis
            conn.execute("UPDATE buku SET stok = stok - 1 WHERE id_buku = ? AND stok > 0", (id_buku,))

if __name__ == "__main__":
    db = DatabaseManager()
    print("Database siap digunakan!")
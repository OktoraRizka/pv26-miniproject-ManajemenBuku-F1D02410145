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
                    penulis TEXT NOT NULL
                )
            ''')
    
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

# Contoh Penggunaan:
if __name__ == "__main__":
    db = DatabaseManager()
    # db.tambah_buku("Laskar Pelangi", 2005, "Fiksi", "Andrea Hirata")
    print("Database siap digunakan!")
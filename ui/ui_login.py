from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, 
                             QPushButton, QLabel, QHBoxLayout, QFrame)
from PySide6.QtCore import Qt

class Ui_LoginWindow:
    def setup_ui(self, LoginWindow):
        LoginWindow.setWindowTitle("Login - Sistem Manajemen Buku")
        LoginWindow.setFixedSize(350, 250)  

        self.central_widget = QWidget()
        LoginWindow.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(30, 30, 30, 30)

        # Header / Judul
        self.label_title = QLabel("LOGIN ADMIN")
        self.label_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.label_title.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.label_title)

        # Garis pemisah
        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.main_layout.addWidget(self.line)

        # Form Layout untuk Input
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(15)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Masukkan username")
        self.form_layout.addRow("Username:", self.user_input)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Masukkan password")
        self.pass_input.setEchoMode(QLineEdit.Password) # Menyembunyikan password
        self.form_layout.addRow("Password:", self.pass_input)

        self.main_layout.addLayout(self.form_layout)

        # Tombol Login
        self.btn_login = QPushButton("Login Sekarang")
        self.btn_login.setFixedHeight(40)
        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.main_layout.addWidget(self.btn_login)

        # Status Label untuk pesan error singkat
        self.label_status = QLabel("")
        self.label_status.setStyleSheet("color: red;")
        self.label_status.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.label_status)
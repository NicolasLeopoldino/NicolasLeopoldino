import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QFile, QTextStream, Qt, QPoint, QPropertyAnimation, QEasingCurve
from ldap3 import Server, Connection, ALL
import subprocess

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.setFixedSize(399, 518)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.moving = False
        self.start = QPoint(0, 0)

        self.init_ui()
        self.set_background_image('loginimage.jpg')
        self.apply_stylesheet('style.qss')

    def init_ui(self):
        # Create UI elements
        self.username_label = self.create_label('USUARIO:')
        self.password_label = self.create_label('CONTRASEÑA:')
        self.username_input = self.create_line_edit()
        self.password_input = self.create_line_edit(True)
        self.minimize_button = self.create_button('-', "color: #003d99; font-size: 16px;")  # Dark blue color
        self.close_button = self.create_button('X', "color: #003d99; font-size: 16px;")  # Dark blue color
        self.login_button = QPushButton('Login', self)
        self.login_button.setStyleSheet("background-color: #003d99; color: white; border: none; border-radius: 5px; padding: 10px 20px;")  # Dark blue color
        self.setup_button_animation()

        # Layouts
        header_layout = QHBoxLayout()
        header_layout.addStretch()
        header_layout.addWidget(self.minimize_button)
        header_layout.addWidget(self.close_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(header_layout)
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_layout.addWidget(self.username_label)
        main_layout.addWidget(self.username_input)
        main_layout.addWidget(self.password_label)
        main_layout.addWidget(self.password_input)
        main_layout.addWidget(self.login_button)
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(main_layout)

        # Connect signals
        self.minimize_button.clicked.connect(self.showMinimized)
        self.close_button.clicked.connect(self.close)
        self.login_button.clicked.connect(self.handle_login)

    def create_label(self, text):
        label = QLabel(text, self)
        label.setStyleSheet("color: black; font-weight: bold; text-transform: uppercase;")
        return label

    def create_line_edit(self, password=False):
        le = QLineEdit(self)
        if password:
            le.setEchoMode(QLineEdit.Password)
        le.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px; background-color: rgba(255, 255, 255, 0.8); color: #003d99;")
        return le

    def create_button(self, text, style):
        button = QPushButton(text, self)
        button.setStyleSheet(f"background: none; border: none; {style}")
        return button

    def set_background_image(self, image_path):
        background_label = QLabel(self)
        background_label.setPixmap(QPixmap(image_path))
        background_label.setGeometry(self.rect())
        background_label.lower()

    def apply_stylesheet(self, path):
        file = QFile(path)
        if file.open(QFile.ReadOnly | QFile.Text):
            self.setStyleSheet(QTextStream(file).readAll())

    def setup_button_animation(self):
        self.login_button_animation = QPropertyAnimation(self.login_button, b"styleSheet")
        self.login_button_animation.setDuration(300)
        self.login_button_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.default_style = "background-color: #003d99; color: white; border: none; border-radius: 5px; padding: 10px 20px;"  # Dark blue color
        self.hover_style = "background-color: #002a6d; color: white; border: none; border-radius: 5px; padding: 10px 20px;"  # Slightly darker blue
        self.login_button.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.login_button:
            if event.type() == event.Enter:
                self.animate_button(self.default_style, self.hover_style)
            elif event.type() == event.Leave:
                self.animate_button(self.hover_style, self.default_style)
        return super().eventFilter(obj, event)

    def animate_button(self, start_style, end_style):
        self.login_button_animation.setStartValue(start_style)
        self.login_button_animation.setEndValue(end_style)
        self.login_button_animation.start()

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if self.connect_to_ldap(username, password):
            self.close()  # Cierra la ventana actual
            self.open_fichaje(username)  # Pasa el nombre de usuario a fichaje.py
        else:
            QMessageBox.critical(self, 'Error', 'Error al conectarse. Verifique sus credenciales o consulte con el administrador')

    def connect_to_ldap(self, username, password):
        ldap_server = 'ldap://192.168.XXX.X:389'  # IP del servidor LDAP
        try:
            server = Server(ldap_server, get_info=ALL)
            conn = Connection(server, user=username, password=password, authentication='SIMPLE')
            if not conn.bind():
                return False
            if conn.bound:
                conn.unbind()
            return True
        except Exception as e:
            print(f'Ocurrió un error: {e}')
            return False

    def open_fichaje(self, username):
        try:
            subprocess.Popen(['python', 'fichaje.py', username])
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error al abrir sistema de fichaje: {e}')

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moving = True
            self.start = event.pos()

    def mouseMoveEvent(self, event):
        if self.moving:
            self.move(self.pos() + event.pos() - self.start)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moving = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

import sys
import pyodbc
from datetime import datetime
import socket
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect, Qt
import requests

class MainWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()

        # Configuración de la ventana
        self.setWindowTitle("Ventana con Imagen de Fondo")
        self.setFixedSize(546, 327)  # Establecer tamaño fijo para la ventana

        # Configurar la ventana sin barra de título
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Crear un widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Crear la etiqueta para la imagen de fondo
        self.background_label = QLabel(self)
        self.pixmap = QPixmap('fondofichaje.png')  # Cargar la imagen
        self.background_label.setPixmap(self.pixmap)
        self.background_label.setScaledContents(True)  # Ajusta la imagen al tamaño del label
        self.background_label.setGeometry(0, 0, 546, 327)  # Ajustar el tamaño de la etiqueta
        self.background_label.setStyleSheet("background: transparent;")  # Hacer el fondo de la etiqueta transparente

        # Crear el QLabel para el texto
        self.text_label = QLabel(username, self)  # Mostrar el nombre de usuario aquí
        self.text_label.setGeometry(QRect(90, 170, 300, 20))  # Ajustar posición y tamaño del texto

        # Crear un layout vertical para los botones
        self.buttons_layout = QVBoxLayout()
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes para ajustar el tamaño del widget
        self.buttons_layout.setSpacing(10)  # Espacio entre los botones

        # Crear botones
        self.boton_entrada = QPushButton('FICHAR ENTRADA')
        self.boton_salida = QPushButton('FICHAR SALIDA')

        # Conectar los botones a las funciones correspondientes
        self.boton_entrada.clicked.connect(self.confirmar_fichaje_entrada)
        self.boton_salida.clicked.connect(self.confirmar_fichaje_salida)

        # Añadir botones al layout de botones
        self.buttons_layout.addWidget(self.boton_entrada)
        self.buttons_layout.addWidget(self.boton_salida)

        # Configurar el layout de botones para que aparezcan en la parte derecha central
        self.buttons_widget = QWidget(self)
        self.buttons_widget.setLayout(self.buttons_layout)
        self.buttons_widget.setGeometry(QRect(320, 90, 200, 100))  # Ajustar posición y tamaño de los botones

        # Añadir la etiqueta, el texto y los botones al widget central
        self.background_label.setParent(self.central_widget)
        self.text_label.setParent(self.central_widget)
        self.buttons_widget.setParent(self.central_widget)

        # Añadir los botones de cerrar y minimizar
        self.add_title_buttons()

        # Asegúrate de que el tamaño del widget central es el mismo que el de la ventana
        self.central_widget.setFixedSize(546, 327)

        # Aplicar el estilo desde el archivo QSS
        self.load_style_sheet()

    def load_style_sheet(self):
        with open('style2.qss', 'r') as file:
            self.setStyleSheet(file.read())

    def add_title_buttons(self):
        # Crear botón de minimizar
        self.minimize_button = QPushButton('-')
        self.minimize_button.setObjectName('minimizeButton')
        self.minimize_button.clicked.connect(self.showMinimized)  # Conectar el botón a la acción de minimizar

        # Crear botón de cerrar
        self.close_button = QPushButton('X')
        self.close_button.setObjectName('closeButton')
        self.close_button.clicked.connect(self.close)  # Conectar el botón a la acción de cerrar

        # Crear un widget para los botones del título
        self.title_buttons_widget = QWidget(self)
        title_buttons_layout = QHBoxLayout(self.title_buttons_widget)
        title_buttons_layout.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes para ajustar el tamaño del widget
        title_buttons_layout.setSpacing(5)  # Espacio entre los botones

        # Añadir botones al layout
        title_buttons_layout.addWidget(self.minimize_button)
        title_buttons_layout.addWidget(self.close_button)

        # Configurar el widget de botones de título
        self.title_buttons_widget.setLayout(title_buttons_layout)
        self.title_buttons_widget.setGeometry(QRect(480, 0, 66, 30))  # Posicionar el widget en la esquina superior derecha

    def obtener_datos(self, tipo_fichaje):
        # Obtener el nombre de usuario desde el texto del QLabel
        usuario = self.text_label.text()

        # Obtener la fecha actual en formato DD-MM-YYYY
        fecha_actual = datetime.now().strftime('%d-%m-%Y')

        # Obtener la hora actual desde una API web
        try:
            response = requests.get('http://worldtimeapi.org/api/timezone/America/Argentina/Buenos_Aires')
            data = response.json()
            hora_actual = datetime.fromisoformat(data['datetime']).strftime('%H:%M')
        except Exception as e:
            print("Error al obtener la hora de la API:", e)
            hora_actual = datetime.now().strftime('%H:%M')  # Fallback en caso de error

        # Obtener la IP local
        ip_local = socket.gethostbyname(socket.gethostname())

        return usuario, fecha_actual, hora_actual, tipo_fichaje, ip_local

    def verificar_fichaje_existe(self, usuario, fecha, tipo_fichaje):
        try:
            # Configuración de la cadena de conexión
            conn_str = (
                'DRIVER={ODBC Driver 18 for SQL Server};'
                'SERVER=XXXX;' # Reemplaza con el nombre del servidor SQL
                'DATABASE=master;'  # Reemplaza con el nombre de tu base de datos
                'UID=usuario;'  # Nombre de usuario
                'PWD=contraseña;'  # Contraseña del usuario
                'TrustServerCertificate=yes;'
            )
            
            # Conectar a la base de datos
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()

            # Consultar si ya existe un fichaje para el usuario en la misma fecha
            sql = """
            SELECT COUNT(*) FROM fichajes
            WHERE usuario = ? AND dia = ? AND tipo_de_fichaje = ?
            """
            cursor.execute(sql, (usuario, fecha, tipo_fichaje))
            resultado = cursor.fetchone()[0]

            # Cerrar el cursor y la conexión
            cursor.close()
            conn.close()

            return resultado > 0

        except pyodbc.Error as e:
            print("Error de ODBC:", e)
            return False
        except Exception as e:
            print("Error inesperado:", e)
            return False

    def insertar_datos(self, usuario, fecha, hora, tipo_fichaje, ip):
        try:
            # Configuración de la cadena de conexión
            conn_str = (
                'DRIVER={ODBC Driver 18 for SQL Server};'
                'SERVER=XXXX;' # Reemplaza con el nombre del servidor SQL
                'DATABASE=master;'  # Reemplaza con el nombre de tu base de datos
                'UID=usuario;'  # Nombre de usuario
                'PWD=contraseña;'  # Contraseña del usuario
                'TrustServerCertificate=yes;'
            )
            
            # Conectar a la base de datos
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()

            # Iniciar la transacción
            conn.autocommit = False

            # Insertar datos en la tabla
            sql = """
            INSERT INTO fichajes (usuario, dia, horario, tipo_de_fichaje, ip)
            VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(sql, (usuario, fecha, hora, tipo_fichaje, ip))
            conn.commit()

            # Cerrar el cursor y la conexión
            cursor.close()
            conn.close()

            return True, hora  # Devolver True y la hora en caso de éxito

        except pyodbc.Error as e:
            print("Error de ODBC:", e)
            conn.rollback()  # Revertir en caso de error
            return False, None
        except Exception as e:
            print("Error inesperado:", e)
            conn.rollback()  # Revertir en caso de error
            return False, None

    def mostrar_mensaje(self, mensaje):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(mensaje)
        msg_box.setWindowTitle("Paktar Cobranzas - Sistema de fichaje ejecutivo")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def confirmar_fichaje_entrada(self):
        # Mostrar el cuadro de diálogo de confirmación
        reply = QMessageBox.question(self, 'Paktar Cobranzas - Sistema de fichaje ejecutivo', 
                                     "¿Estás seguro de que quieres fichar entrada? Recuerda que solo puedes hacerlo una vez por día.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.fichar_entrada()

    def confirmar_fichaje_salida(self):
        # Mostrar el cuadro de diálogo de confirmación
        reply = QMessageBox.question(self, 'Paktar Cobranzas - Sistema de fichaje ejecutivo', 
                                     "¿Estás seguro de que quieres fichar salida? Recuerda que solo puedes hacerlo una vez por día",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.fichar_salida()

    def fichar_entrada(self):
        # Obtener los datos y el tipo de fichaje
        datos = self.obtener_datos('entrada')
        usuario, fecha, hora, tipo_fichaje, ip = datos

        if self.verificar_fichaje_existe(usuario, fecha, tipo_fichaje):
            self.mostrar_mensaje("Ya tenías registrado un fichaje de entrada en el día de hoy.")
        else:
            exito, hora_fichaje = self.insertar_datos(usuario, fecha, hora, tipo_fichaje, ip)
            if exito:
                mensaje = f"Fichaje de entrada realizado correctamente a las {hora_fichaje}."
                self.mostrar_mensaje(mensaje)

    def fichar_salida(self):
        # Obtener los datos y el tipo de fichaje
        datos = self.obtener_datos('salida')
        usuario, fecha, hora, tipo_fichaje, ip = datos

        # Verificar si el usuario ya ha fichado entrada el mismo día
        if not self.verificar_fichaje_existe(usuario, fecha, 'entrada'):
            self.mostrar_mensaje("Primero debes fichar entrada antes de fichar salida.")
        elif self.verificar_fichaje_existe(usuario, fecha, tipo_fichaje):
            self.mostrar_mensaje("Ya tenías registrado un fichaje de salida en el día de hoy.")
        else:
            exito, hora_fichaje = self.insertar_datos(usuario, fecha, hora, tipo_fichaje, ip)
            if exito:
                mensaje = f"Fichaje de salida realizado correctamente a las {hora_fichaje}."
                self.mostrar_mensaje(mensaje)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        username = 'Desconocido'

    app = QApplication(sys.argv)
    window = MainWindow(username)
    window.show()
    sys.exit(app.exec_())

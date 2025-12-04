"""
Ventana de Login - Top Flow
Conecta Login_topflow.ui con la base de datos
"""
import sys
from PyQt5.QtWidgets import QDialog, QMessageBox, QApplication
from PyQt5 import uic
from modelo.usuariodao import UsuarioDAO


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        # Cargar el archivo .ui
        uic.loadUi('ui_topflow/Login_topflow.ui', self)
        
        # Inicializar DAO
        self.usuario_dao = UsuarioDAO()
        
        # Conectar botones
        self.boton_login.clicked.connect(self.iniciar_sesion)
        self.boton_registro.clicked.connect(self.registrar_usuario)
        
        # Variables para almacenar el usuario actual
        self.usuario_actual = None
    
    def iniciar_sesion(self):
        """Validar credenciales e iniciar sesión"""
        usuario = self.login_user.text().strip()
        contraseña = self.login_password.text().strip()
        
        # Validar campos vacíos
        if not usuario or not contraseña:
            QMessageBox.warning(self, "Campos vacíos", "Por favor ingrese usuario y contraseña")
            return
        
        # Validar con la base de datos
        try:
            if self.usuario_dao.validarLogin(usuario, contraseña):
                self.usuario_actual = usuario
                QMessageBox.information(self, "Éxito", f"¡Bienvenido {usuario}!")
                self.accept()  # Cierra el diálogo con resultado exitoso
            else:
                QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")
                self.login_password.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error de conexión", f"No se pudo conectar a la base de datos:\n{str(e)}")
    
    def registrar_usuario(self):
        """Registrar nuevo usuario"""
        usuario = self.login_user.text().strip()
        contraseña = self.login_password.text().strip()
        
        # Validar campos vacíos
        if not usuario or not contraseña:
            QMessageBox.warning(self, "Campos vacíos", "Por favor ingrese usuario y contraseña")
            return
        
        # Validar longitud de contraseña
        if len(contraseña) < 4:
            QMessageBox.warning(self, "Contraseña débil", "La contraseña debe tener al menos 4 caracteres")
            return
        
        # Registrar en la base de datos
        try:
            if self.usuario_dao.registrarUsuario(usuario, contraseña):
                QMessageBox.information(self, "Éxito", f"Usuario {usuario} registrado correctamente")
                self.login_user.clear()
                self.login_password.clear()
            else:
                QMessageBox.warning(self, "Error", "El usuario ya existe o hubo un error al registrar")
        except Exception as e:
            QMessageBox.critical(self, "Error de conexión", f"No se pudo conectar a la base de datos:\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = LoginWindow()
    if ventana.exec_() == QDialog.Accepted:
        print(f"Usuario logueado: {ventana.usuario_actual}")
    sys.exit()

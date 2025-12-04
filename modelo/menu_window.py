"""
Ventana de Menú Principal - Top Flow
Conecta Menu_topflow.ui con las diferentes secciones
"""
import sys
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5 import uic


class MenuWindow(QDialog):
    def __init__(self, usuario=None):
        super().__init__()
        # Cargar el archivo .ui
        uic.loadUi('ui_topflow/Menu_topflow.ui', self)
        
        self.usuario = usuario
        
        # Actualizar el mensaje de bienvenida
        if usuario:
            self.label.setText(f"Bienvenido {usuario}, ¿A qué sección deseas ingresar?")
        
        # Conectar botones
        self.menu_productos.clicked.connect(self.abrir_productos)
        self.menu_empleados.clicked.connect(self.abrir_carrito)
        self.menu_logout.clicked.connect(self.cerrar_sesion)
        
        # Variable para saber qué ventana abrir
        self.ventana_seleccionada = None
    
    def abrir_productos(self):
        """Abrir ventana de productos"""
        self.ventana_seleccionada = "productos"
        self.accept()
    
    def abrir_carrito(self):
        """Abrir ventana de carrito/pedidos"""
        self.ventana_seleccionada = "carrito"
        self.accept()
    
    def cerrar_sesion(self):
        """Cerrar sesión y volver al login"""
        self.ventana_seleccionada = "logout"
        self.reject()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MenuWindow("Usuario Demo")
    ventana.exec_()
    sys.exit()

"""
Aplicación Principal - Top Flow
Sistema de gestión de tienda de ropa
Integra todas las ventanas: Login, Menú, Productos, Carrito
"""
import sys
from PyQt5.QtWidgets import QApplication, QDialog
from login_window import LoginWindow
from menu_window import MenuWindow
from productos_window import ProductosWindow
from carrito_window import CarritoWindow
from consultar_productos_window import ConsultarProductosWindow


class TopFlowApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.usuario_actual = None
        
        # Iniciar desde el login
        self.mostrar_login()
    
    def mostrar_login(self):
        """Mostrar ventana de login"""
        self.login_window = LoginWindow()
        
        if self.login_window.exec_() == QDialog.Accepted:
            # Login exitoso
            self.usuario_actual = self.login_window.usuario_actual
            self.mostrar_menu()
        else:
            # Usuario canceló o cerró el login
            sys.exit()
    
    def mostrar_menu(self):
        """Mostrar menú principal"""
        self.menu_window = MenuWindow(self.usuario_actual)
        
        if self.menu_window.exec_() == QDialog.Accepted:
            # Usuario seleccionó una opción
            if self.menu_window.ventana_seleccionada == "productos":
                self.mostrar_productos()
            elif self.menu_window.ventana_seleccionada == "carrito":
                self.mostrar_carrito()
        else:
            # Usuario cerró sesión
            self.mostrar_login()
    
    def mostrar_productos(self):
        """Mostrar ventana de productos"""
        self.productos_window = ProductosWindow()
        self.productos_window.show()
        
        # Cuando se cierre la ventana de productos, volver al menú
        self.productos_window.destroyed.connect(self.mostrar_menu)
    
    def mostrar_carrito(self):
        """Mostrar ventana de carrito"""
        self.carrito_window = CarritoWindow()
        self.carrito_window.show()
        
        # Cuando se cierre la ventana de carrito, volver al menú
        self.carrito_window.destroyed.connect(self.mostrar_menu)
    
    def run(self):
        """Ejecutar la aplicación"""
        sys.exit(self.app.exec_())


def main():
    """Función principal"""
    print("=" * 60)
    print("TOP FLOW - Sistema de Gestión de Tienda de Ropa")
    print("=" * 60)
    print("Iniciando aplicación...")
    
    app = TopFlowApp()
    app.run()


if __name__ == "__main__":
    main()

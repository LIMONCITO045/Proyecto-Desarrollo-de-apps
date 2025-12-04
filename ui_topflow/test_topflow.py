"""
Script de prueba - Top Flow
Permite probar cada ventana individualmente
"""
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox

# Menú de pruebas
def menu_pruebas():
    print("\n" + "=" * 60)
    print("TOP FLOW - MENÚ DE PRUEBAS")
    print("=" * 60)
    print("1. Probar ventana de Login")
    print("2. Probar ventana de Menú")
    print("3. Probar ventana de Productos")
    print("4. Probar ventana de Carrito")
    print("5. Probar ventana de Consultar Productos (CRUD)")
    print("6. Ejecutar aplicación completa")
    print("0. Salir")
    print("=" * 60)
    
    opcion = input("\nSeleccione una opción: ")
    return opcion


def probar_login():
    """Probar ventana de login"""
    from login_window import LoginWindow
    
    app = QApplication(sys.argv)
    ventana = LoginWindow()
    ventana.exec_()
    sys.exit()


def probar_menu():
    """Probar ventana de menú"""
    from menu_window import MenuWindow
    
    app = QApplication(sys.argv)
    ventana = MenuWindow("Usuario de Prueba")
    ventana.exec_()
    sys.exit()


def probar_productos():
    """Probar ventana de productos"""
    from productos_window import ProductosWindow
    
    app = QApplication(sys.argv)
    ventana = ProductosWindow()
    ventana.show()
    sys.exit(app.exec_())


def probar_carrito():
    """Probar ventana de carrito"""
    from carrito_window import CarritoWindow
    
    app = QApplication(sys.argv)
    ventana = CarritoWindow()
    ventana.show()
    sys.exit(app.exec_())


def probar_consultar_productos():
    """Probar ventana de consultar productos"""
    from consultar_productos_window import ConsultarProductosWindow
    
    app = QApplication(sys.argv)
    ventana = ConsultarProductosWindow()
    ventana.show()
    sys.exit(app.exec_())


def ejecutar_app_completa():
    """Ejecutar aplicación completa"""
    from main_topflow import main
    main()


def main():
    """Función principal"""
    while True:
        opcion = menu_pruebas()
        
        if opcion == "1":
            probar_login()
        elif opcion == "2":
            probar_menu()
        elif opcion == "3":
            probar_productos()
        elif opcion == "4":
            probar_carrito()
        elif opcion == "5":
            probar_consultar_productos()
        elif opcion == "6":
            ejecutar_app_completa()
        elif opcion == "0":
            print("\n¡Hasta luego!")
            break
        else:
            print("\n❌ Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    main()

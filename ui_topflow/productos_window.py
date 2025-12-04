"""
Ventana de Productos - Top Flow
Conecta Productos_topflow.ui con la base de datos
"""
import sys
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QApplication, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5 import uic
from modelo.productodao import ProductoDAO


class ProductosWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Cargar el archivo .ui
        uic.loadUi('ui_topflow/Productos_topflow.ui', self)
        
        # Inicializar DAO
        self.producto_dao = ProductoDAO()
        
        # Configurar la tabla
        self.configurar_tabla()
        
        # Conectar botones
        self.pushButton.clicked.connect(self.salir)  # Botón Salir
        self.pushButton_2.clicked.connect(self.abrir_carrito)  # Botón Carrito
        
        # Cargar productos al iniciar
        self.cargar_productos()
    
    def configurar_tabla(self):
        """Configurar la tabla de productos"""
        # Configurar headers
        headers = ["ID", "Tipo", "Precio", "Talla", "Catálogo", "Cantidad"]
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(headers)
        
        # Ajustar el tamaño de las columnas
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Tipo
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Precio
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Talla
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Catálogo
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Cantidad
        
        # Hacer la tabla de solo lectura
        self.tableWidget.setEditTriggers(self.tableWidget.NoEditTriggers)
        
        # Habilitar selección de filas completas
        self.tableWidget.setSelectionBehavior(self.tableWidget.SelectRows)
        self.tableWidget.setSelectionMode(self.tableWidget.SingleSelection)
    
    def cargar_productos(self):
        """Cargar productos desde la base de datos"""
        try:
            filas = self.producto_dao.listarProductos()
            
            # Limpiar la tabla
            self.tableWidget.setRowCount(0)
            
            # Llenar la tabla
            for fila in filas:
                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)
                
                # id_producto, tipo, precio, talla, id_catalogo, cantidad
                for col, valor in enumerate(fila):
                    item = QTableWidgetItem(str(valor))
                    item.setTextAlignment(Qt.AlignCenter)
                    
                    # Si la cantidad es 0, resaltar en rojo
                    if col == 5 and valor == 0:
                        item.setBackground(Qt.red)
                    # Si el precio está en la columna 2, formatear como moneda
                    elif col == 2:
                        item.setText(f"${valor} USD")
                    
                    self.tableWidget.setItem(row_position, col, item)
            
            print(f"✓ {len(filas)} productos cargados")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los productos:\n{str(e)}")
            print(f"Error al cargar productos: {e}")
    
    def abrir_carrito(self):
        """Abrir ventana de carrito"""
        # Importar aquí para evitar import circular
        from carrito_window import CarritoWindow
        
        self.carrito_window = CarritoWindow()
        self.carrito_window.show()
    
    def salir(self):
        """Cerrar la ventana"""
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = ProductosWindow()
    ventana.show()
    sys.exit(app.exec_())

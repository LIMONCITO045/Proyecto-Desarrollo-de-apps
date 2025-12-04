"""
Ventana de Carrito/Pedidos - Top Flow
Conecta Carrito_topflow.ui con la base de datos
"""
import sys
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QApplication, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pedidodao import PedidoDAO


class CarritoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Cargar el archivo .ui
        uic.loadUi('ui_topflow/Carrito_topflow.ui', self)
        
        # Inicializar DAO
        self.pedido_dao = PedidoDAO()
        
        # Configurar la tabla
        self.configurar_tabla()
        
        # Conectar botones
        self.pushButton.clicked.connect(self.salir)  # Botón Salir
        self.pushButton_2.clicked.connect(self.actualizar_pedidos)  # Botón Actualizar
        
        # Cargar pedidos al iniciar
        self.cargar_pedidos()
    
    def configurar_tabla(self):
        """Configurar la tabla de pedidos"""
        # La tabla ya tiene headers definidos en el .ui
        # ID_Pedido, Fecha, Cantidad_de_productos, Precio total
        
        # Ajustar el tamaño de las columnas
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID_Pedido
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Fecha (no existe en la BD, se puede calcular)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Cantidad
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Precio total
        
        # Hacer la tabla de solo lectura
        self.tableWidget.setEditTriggers(self.tableWidget.NoEditTriggers)
        
        # Habilitar selección de filas completas
        self.tableWidget.setSelectionBehavior(self.tableWidget.SelectRows)
        self.tableWidget.setSelectionMode(self.tableWidget.SingleSelection)
    
    def cargar_pedidos(self):
        """Cargar pedidos desde la base de datos"""
        try:
            filas = self.pedido_dao.listarPedidos()
            
            # Limpiar la tabla
            self.tableWidget.setRowCount(0)
            
            # Llenar la tabla
            for fila in filas:
                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)
                
                # fila: id_pedidos, destino, id_informacion_pedido, total, id_producto, id_cliente, id_produccion, id_catalogo
                # Vamos a mostrar: ID, Destino (como "fecha"), "1" como cantidad, Total
                
                # ID Pedido
                item_id = QTableWidgetItem(str(fila[0]))
                item_id.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(row_position, 0, item_id)
                
                # Destino (en lugar de fecha)
                item_destino = QTableWidgetItem(str(fila[1]))
                item_destino.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(row_position, 1, item_destino)
                
                # Cantidad de productos (por ahora 1, se puede mejorar con JOIN)
                item_cantidad = QTableWidgetItem("1")
                item_cantidad.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(row_position, 2, item_cantidad)
                
                # Precio total
                item_total = QTableWidgetItem(f"${fila[3]} USD")
                item_total.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(row_position, 3, item_total)
            
            # Actualizar el contador LCD
            self.lcdNumber.display(len(filas))
            
            print(f"✓ {len(filas)} pedidos cargados")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los pedidos:\n{str(e)}")
            print(f"Error al cargar pedidos: {e}")
    
    def actualizar_pedidos(self):
        """Actualizar la lista de pedidos"""
        self.cargar_pedidos()
        QMessageBox.information(self, "Actualizado", "Lista de pedidos actualizada")
    
    def salir(self):
        """Cerrar la ventana"""
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = CarritoWindow()
    ventana.show()
    sys.exit(app.exec_())

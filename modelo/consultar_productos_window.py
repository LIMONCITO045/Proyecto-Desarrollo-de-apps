"""
Ventana de Consulta de Productos - Top Flow
Conecta Consultar_productos.ui con la base de datos
Incluye funcionalidad completa CRUD
"""
import sys
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QApplication, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5 import uic
from productodao import ProductoDAO


class ConsultarProductosWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Cargar el archivo .ui
        uic.loadUi('ui_topflow/Consultar_productos.ui', self)
        
        # Inicializar DAO
        self.producto_dao = ProductoDAO()
        
        # Configurar la tabla
        self.configurar_tabla()
        
        # Conectar botones del menú lateral
        self.boton_salir.clicked.connect(self.salir)
        self.boton_agregar.clicked.connect(self.mostrar_agregar)
        self.boton_actualizar.clicked.connect(self.mostrar_actualizar)
        self.boton_eliminar.clicked.connect(self.mostrar_eliminar)
        self.boton_buscar.clicked.connect(self.mostrar_buscar)
        self.boton_consultar.clicked.connect(self.mostrar_consultar)
        
        # Conectar botones de acción
        self.accion_guardar.clicked.connect(self.guardar_producto)
        self.accion_actualizar.clicked.connect(self.actualizar_producto)
        self.accion_eliminar.clicked.connect(self.eliminar_producto)
        self.accion_limpiar.clicked.connect(self.limpiar_busqueda)
        self.boton_refresh.clicked.connect(self.cargar_productos)
        
        # Mostrar la página de consulta por defecto
        self.stackedWidget.setCurrentIndex(4)  # Página consultar
        
        # Cargar productos
        self.cargar_productos()
    
    def configurar_tabla(self):
        """Configurar la tabla de productos"""
        # Ajustar el tamaño de las columnas
        header = self.tabla_consulta.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # SKU (ID)
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Descripción (Tipo)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Existencia (Cantidad)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Precio
        
        # Hacer la tabla de solo lectura
        self.tabla_consulta.setEditTriggers(self.tabla_consulta.NoEditTriggers)
        
        # Habilitar selección de filas completas
        self.tabla_consulta.setSelectionBehavior(self.tabla_consulta.SelectRows)
        self.tabla_consulta.setSelectionMode(self.tabla_consulta.SingleSelection)
        
        # Conectar señal de selección
        self.tabla_consulta.itemSelectionChanged.connect(self.producto_seleccionado)
    
    def cargar_productos(self):
        """Cargar productos desde la base de datos"""
        try:
            filas = self.producto_dao.listarProductos()
            
            # Limpiar la tabla
            self.tabla_consulta.setRowCount(0)
            
            # Llenar la tabla
            for fila in filas:
                row_position = self.tabla_consulta.rowCount()
                self.tabla_consulta.insertRow(row_position)
                
                # fila: id_producto, tipo, precio, talla, id_catalogo, cantidad
                # Mostrar: SKU (ID), Descripción (Tipo + Talla), Existencia (Cantidad), Precio
                
                # SKU (ID)
                item_id = QTableWidgetItem(str(fila[0]))
                item_id.setTextAlignment(Qt.AlignCenter)
                self.tabla_consulta.setItem(row_position, 0, item_id)
                
                # Descripción (Tipo + Talla)
                descripcion = f"{fila[1]} - Talla {fila[3]}"
                item_desc = QTableWidgetItem(descripcion)
                item_desc.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.tabla_consulta.setItem(row_position, 1, item_desc)
                
                # Existencia (Cantidad)
                item_cantidad = QTableWidgetItem(str(fila[5]))
                item_cantidad.setTextAlignment(Qt.AlignCenter)
                if fila[5] == 0:
                    item_cantidad.setBackground(Qt.red)
                elif fila[5] < 10:
                    item_cantidad.setBackground(Qt.yellow)
                self.tabla_consulta.setItem(row_position, 2, item_cantidad)
                
                # Precio
                item_precio = QTableWidgetItem(f"${fila[2]}")
                item_precio.setTextAlignment(Qt.AlignCenter)
                self.tabla_consulta.setItem(row_position, 3, item_precio)
            
            print(f"✓ {len(filas)} productos cargados")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los productos:\n{str(e)}")
    
    def producto_seleccionado(self):
        """Cargar datos del producto seleccionado en los formularios"""
        selected_items = self.tabla_consulta.selectedItems()
        if not selected_items:
            return
        
        # Obtener el ID del producto (primera columna)
        row = selected_items[0].row()
        id_producto = int(self.tabla_consulta.item(row, 0).text())
        
        try:
            # Obtener datos completos del producto
            producto = self.producto_dao.obtenerProductoPorID(id_producto)
            
            if producto:
                # id_producto, tipo, precio, talla, id_catalogo
                # Llenar formulario de actualizar
                self.sku_actualizar.setText(str(producto[0]))
                self.descripcion_actualizar.setText(producto[1])
                self.precio_actualizar.setText(str(producto[2]))
                self.existencia_actualizar.setText(producto[3])  # Talla
                
                # Llenar formulario de eliminar
                self.sku_eliminar.setText(str(producto[0]))
                self.descripcion_eliminar.setText(producto[1])
                self.precio_eliminar.setText(str(producto[2]))
                self.existencia_eliminar.setText(producto[3])  # Talla
                
                # Llenar formulario de buscar
                self.sku_buscar.setText(str(producto[0]))
                self.descripcion_buscar.setText(producto[1])
                self.precio_buscar.setText(str(producto[2]))
                self.existencia_buscar.setText(producto[3])  # Talla
                
        except Exception as e:
            print(f"Error al cargar producto: {e}")
    
    # Métodos para cambiar de página en el StackedWidget
    def mostrar_agregar(self):
        self.stackedWidget.setCurrentIndex(0)
        self.limpiar_formulario_agregar()
    
    def mostrar_actualizar(self):
        self.stackedWidget.setCurrentIndex(1)
    
    def mostrar_eliminar(self):
        self.stackedWidget.setCurrentIndex(2)
    
    def mostrar_buscar(self):
        self.stackedWidget.setCurrentIndex(3)
    
    def mostrar_consultar(self):
        self.stackedWidget.setCurrentIndex(4)
        self.cargar_productos()
    
    # Métodos CRUD
    def guardar_producto(self):
        """Guardar nuevo producto"""
        try:
            # Obtener datos del formulario
            tipo = self.descripcion_agregar.text().strip()
            precio = self.precio_agregar.text().strip()
            talla = self.sku_agregar.text().strip()  # Usando SKU como talla
            existencia = self.existencia_agregar.text().strip()
            
            # Validar campos
            if not all([tipo, precio, talla, existencia]):
                QMessageBox.warning(self, "Campos vacíos", "Por favor complete todos los campos")
                return
            
            # Convertir a tipos correctos
            precio = int(precio)
            existencia = int(existencia)
            id_catalogo = 1  # Por defecto
            
            # Insertar en la base de datos
            id_nuevo = self.producto_dao.insertarProducto(tipo, precio, talla, id_catalogo)
            
            QMessageBox.information(self, "Éxito", f"Producto agregado con ID: {id_nuevo}")
            self.limpiar_formulario_agregar()
            self.cargar_productos()
            
        except ValueError:
            QMessageBox.warning(self, "Error de formato", "El precio y la existencia deben ser números")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el producto:\n{str(e)}")
    
    def actualizar_producto(self):
        """Actualizar producto existente"""
        try:
            # Obtener datos del formulario
            id_producto = int(self.sku_actualizar.text().strip())
            tipo = self.descripcion_actualizar.text().strip()
            precio = int(self.precio_actualizar.text().strip())
            talla = self.existencia_actualizar.text().strip()
            id_catalogo = 1  # Por defecto
            
            # Validar campos
            if not all([tipo, talla]):
                QMessageBox.warning(self, "Campos vacíos", "Por favor complete todos los campos")
                return
            
            # Actualizar en la base de datos
            self.producto_dao.actualizarProducto(id_producto, tipo, precio, talla, id_catalogo)
            
            QMessageBox.information(self, "Éxito", "Producto actualizado correctamente")
            self.cargar_productos()
            
        except ValueError:
            QMessageBox.warning(self, "Error de formato", "Verifique que los datos sean correctos")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar el producto:\n{str(e)}")
    
    def eliminar_producto(self):
        """Eliminar producto"""
        try:
            id_producto = int(self.sku_eliminar.text().strip())
            
            # Confirmar eliminación
            respuesta = QMessageBox.question(
                self, 
                "Confirmar eliminación", 
                f"¿Está seguro de eliminar el producto {id_producto}?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if respuesta == QMessageBox.Yes:
                self.producto_dao.eliminarProducto(id_producto)
                QMessageBox.information(self, "Éxito", "Producto eliminado correctamente")
                self.cargar_productos()
                self.limpiar_formulario_eliminar()
                
        except ValueError:
            QMessageBox.warning(self, "Error", "ID de producto inválido")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo eliminar el producto:\n{str(e)}")
    
    def limpiar_busqueda(self):
        """Limpiar campos de búsqueda"""
        self.sku_buscar.clear()
        self.descripcion_buscar.clear()
        self.precio_buscar.clear()
        self.existencia_buscar.clear()
    
    def limpiar_formulario_agregar(self):
        """Limpiar formulario de agregar"""
        self.sku_agregar.clear()
        self.descripcion_agregar.clear()
        self.precio_agregar.clear()
        self.existencia_agregar.clear()
    
    def limpiar_formulario_eliminar(self):
        """Limpiar formulario de eliminar"""
        self.sku_eliminar.clear()
        self.descripcion_eliminar.clear()
        self.precio_eliminar.clear()
        self.existencia_eliminar.clear()
    
    def salir(self):
        """Cerrar la ventana"""
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = ConsultarProductosWindow()
    ventana.show()
    sys.exit(app.exec_())

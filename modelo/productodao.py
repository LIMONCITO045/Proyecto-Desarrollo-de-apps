from modelo.productos import Producto
from modelo.conexionbd import ConexionBD

class ProductoDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.producto = Producto()
        
    def listarProductos(self):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        query = 'SELECT id_producto, tipo, precio, talla, id_catalogo FROM [dbo].[productos]'
        cursor.execute(query)
        filas = cursor.fetchall()
        for fila in filas:
            print(f"ID: {fila[0]}, Tipo: {fila[1]}, Precio: {fila[2]}, Talla: {fila[3]}, Catálogo: {fila[4]}")
        self.bd.cerrarConexionBD()
    
    def insertarProducto(self, tipo, precio, talla, id_catalogo):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_InsertarProducto] ?, ?, ?, ?'
        cursor.execute(sp, (tipo, precio, talla, id_catalogo))
        self.bd.conexion.commit()
        resultado = cursor.fetchone()
        print(f"Producto insertado con ID: {resultado[0]}")
        self.bd.cerrarConexionBD()
        return resultado[0]
    
    def actualizarPrecioProducto(self, id_producto, nuevo_precio):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_ActualizarPrecioProducto] ?, ?'
        cursor.execute(sp, (id_producto, nuevo_precio))
        self.bd.conexion.commit()
        resultado = cursor.fetchone()
        print(resultado[0])
        self.bd.cerrarConexionBD()
    
    def obtenerProductosPorCatalogo(self, id_catalogo):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        query = 'SELECT * FROM [dbo].[fn_ProductosPorCatalogo](?)'
        cursor.execute(query, (id_catalogo,))
        filas = cursor.fetchall()
        for fila in filas:
            print(f"ID: {fila[0]}, Tipo: {fila[1]}, Precio: {fila[2]}, Talla: {fila[3]}")
        self.bd.cerrarConexionBD()
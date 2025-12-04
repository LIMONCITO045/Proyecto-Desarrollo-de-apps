from models import Producto
from conexionbd import ConexionBD

class ProductoDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.producto = Producto()
    
    def listarProductos(self):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_ListarProductos]'
        cursor.execute(sp)
        filas = cursor.fetchall()
        self.bd.cerrarConexionBD()
        return filas
    
    def obtenerProductoPorID(self, id_producto):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_ObtenerProductoPorID] ?'
        cursor.execute(sp, (id_producto,))
        fila = cursor.fetchone()
        self.bd.cerrarConexionBD()
        return fila
    
    def insertarProducto(self, tipo, precio, talla, id_catalogo):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_InsertarProducto] ?, ?, ?, ?'
        cursor.execute(sp, (tipo, precio, talla, id_catalogo))
        self.bd.conexion.commit()
        resultado = cursor.fetchone()
        self.bd.cerrarConexionBD()
        return resultado[0]
    
    def actualizarProducto(self, id_producto, tipo, precio, talla, id_catalogo):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_ActualizarProducto] ?, ?, ?, ?, ?'
        cursor.execute(sp, (id_producto, tipo, precio, talla, id_catalogo))
        self.bd.conexion.commit()
        self.bd.cerrarConexionBD()
    
    def actualizarPrecioProducto(self, id_producto, nuevo_precio):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_ActualizarPrecioProducto] ?, ?'
        cursor.execute(sp, (id_producto, nuevo_precio))
        self.bd.conexion.commit()
        self.bd.cerrarConexionBD()
    
    def eliminarProducto(self, id_producto):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_EliminarProducto] ?'
        cursor.execute(sp, (id_producto,))
        self.bd.conexion.commit()
        self.bd.cerrarConexionBD()
    
    def obtenerProductosPorCatalogo(self, id_catalogo):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        query = 'SELECT * FROM [dbo].[fn_ProductosPorCatalogo](?)'
        cursor.execute(query, (id_catalogo,))
        filas = cursor.fetchall()
        self.bd.cerrarConexionBD()
        return filas
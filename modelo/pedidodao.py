from models import Pedido
from conexionbd import ConexionBD

class PedidoDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.pedido = Pedido()
    
    def listarPedidos(self):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_ListarPedidos]'
        cursor.execute(sp)
        filas = cursor.fetchall()
        for fila in filas:
            print(f"ID: {fila[0]}, Destino: {fila[1]}, Total: {fila[3]}, Cliente: {fila[5]}")
        self.bd.cerrarConexionBD()
        return filas
    
    def obtenerPedidoPorID(self, id_pedidos):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_ObtenerPedidoPorID] ?'
        cursor.execute(sp, (id_pedidos,))
        fila = cursor.fetchone()
        self.bd.cerrarConexionBD()
        return fila
    
    def obtenerPedidosCliente(self, id_cliente):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_ObtenerPedidosCliente] ?'
        cursor.execute(sp, (id_cliente,))
        filas = cursor.fetchall()
        self.bd.cerrarConexionBD()
        return filas
    
    def insertarPedido(self, destino, id_informacion_pedido, total, id_producto, id_cliente, id_produccion, id_catalogo):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_InsertarPedido] ?, ?, ?, ?, ?, ?, ?'
        cursor.execute(sp, (destino, id_informacion_pedido, total, id_producto, id_cliente, id_produccion, id_catalogo))
        self.bd.conexion.commit()
        resultado = cursor.fetchone()
        print(f"Pedido insertado con ID: {resultado[0]}")
        self.bd.cerrarConexionBD()
        return resultado[0]
    
    def actualizarPedido(self, id_pedidos, destino, id_informacion_pedido, total, id_producto, id_cliente, id_produccion, id_catalogo):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_ActualizarPedido] ?, ?, ?, ?, ?, ?, ?, ?'
        cursor.execute(sp, (id_pedidos, destino, id_informacion_pedido, total, id_producto, id_cliente, id_produccion, id_catalogo))
        self.bd.conexion.commit()
        self.bd.cerrarConexionBD()
    
    def eliminarPedido(self, id_pedidos):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_EliminarPedido] ?'
        cursor.execute(sp, (id_pedidos,))
        self.bd.conexion.commit()
        self.bd.cerrarConexionBD()

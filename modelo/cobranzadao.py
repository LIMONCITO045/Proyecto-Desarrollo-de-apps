from modelo.models import Cobranza
from modelo.conexionbd import ConexionBD

class CobranzaDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.cobranza = Cobranza()
    
    def listarCobranzas(self):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_ListarCobranzas]'
        cursor.execute(sp)
        filas = cursor.fetchall()
        for fila in filas:
            print(f"ID Pedido: {fila[0]}, Monto: {fila[1]}, Método: {fila[2]}, Banco: {fila[3]}, Verificación: {fila[4]}")
        self.bd.cerrarConexionBD()
        return filas
    
    def obtenerCobranzaPorPedido(self, id_pedidos):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_ObtenerCobranzaPorPedido] ?'
        cursor.execute(sp, (id_pedidos,))
        fila = cursor.fetchone()
        self.bd.cerrarConexionBD()
        return fila
    
    def registrarPago(self, id_pedidos, monto, metodo_de_pago, banco, verificacion):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_RegistrarPago] ?, ?, ?, ?, ?'
        cursor.execute(sp, (id_pedidos, monto, metodo_de_pago, banco, verificacion))
        self.bd.conexion.commit()
        self.bd.cerrarConexionBD()
    
    def actualizarCobranza(self, id_pedidos, monto, metodo_de_pago, banco, verificacion):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_ActualizarCobranza] ?, ?, ?, ?, ?'
        cursor.execute(sp, (id_pedidos, monto, metodo_de_pago, banco, verificacion))
        self.bd.conexion.commit()
        self.bd.cerrarConexionBD()
    
    def eliminarCobranza(self, id_pedidos):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_EliminarCobranza] ?'
        cursor.execute(sp, (id_pedidos,))
        self.bd.conexion.commit()
        self.bd.cerrarConexionBD()
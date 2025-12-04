from models import Cliente
from conexionbd import ConexionBD

class ClienteDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.cliente = Cliente()
    
    def listarClientes(self):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_ListarClientes]'
        cursor.execute(sp)
        filas = cursor.fetchall()
        for fila in filas:
            print(f"ID: {fila[0]}, Nombre: {fila[1]}, País: {fila[2]}, Región: {fila[3]}, Historial: {fila[4]}")
        self.bd.cerrarConexionBD()
        return filas
    
    def obtenerClientePorID(self, id_cliente):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_ObtenerClientePorID] ?'
        cursor.execute(sp, (id_cliente,))
        fila = cursor.fetchone()
        self.bd.cerrarConexionBD()
        return fila
    
    def insertarCliente(self, nombre, pais, region):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_InsertarCliente] ?, ?, ?'
        cursor.execute(sp, (nombre, pais, region))
        self.bd.conexion.commit()
        resultado = cursor.fetchone()
        print(f"Cliente insertado con ID: {resultado[0]}")
        self.bd.cerrarConexionBD()
        return resultado[0]
    
    def actualizarCliente(self, id_cliente, nombre, pais, region):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_ActualizarCliente] ?, ?, ?, ?'
        cursor.execute(sp, (id_cliente, nombre, pais, region))
        self.bd.conexion.commit()
        self.bd.cerrarConexionBD()
    
    def eliminarCliente(self, id_cliente):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_EliminarCliente] ?'
        cursor.execute(sp, (id_cliente,))
        self.bd.conexion.commit()
        self.bd.cerrarConexionBD()
    
    def listarClientesPorRegion(self, region):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_ListarClientesPorRegion] ?'
        cursor.execute(sp, (region,))
        filas = cursor.fetchall()
        self.bd.cerrarConexionBD()
        return filas
    
    def incrementarHistorialCompras(self, id_cliente):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_IncrementarHistorialCompras] ?'
        cursor.execute(sp, (id_cliente,))
        self.bd.conexion.commit()
        self.bd.cerrarConexionBD()
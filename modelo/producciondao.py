from models import Produccion
from conexionbd import ConexionBD

class ProduccionDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.produccion = Produccion()
    
    def listarProducciones(self):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_ListarProducciones]'
        cursor.execute(sp)
        filas = cursor.fetchall()
        for fila in filas:
            print(f"ID: {fila[0]}, Fábrica: {fila[1]}, Fabricación: {fila[2]}, Empaque: {fila[3]}, Envíos: {fila[4]}, Transporte: {fila[5]}")
        self.bd.cerrarConexionBD()
        return filas
    
    def obtenerProduccionPorID(self, id_produccion):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_ObtenerProduccionPorID] ?'
        cursor.execute(sp, (id_produccion,))
        fila = cursor.fetchone()
        self.bd.cerrarConexionBD()
        return fila
    
    def registrarProduccion(self, fabrica, fabricacion, empaque, envios, transporte):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_RegistrarProduccion] ?, ?, ?, ?, ?'
        cursor.execute(sp, (fabrica, fabricacion, empaque, envios, transporte))
        self.bd.conexion.commit()
        resultado = cursor.fetchone()
        print(f"Producción registrada con ID: {resultado[0]}")
        self.bd.cerrarConexionBD()
        return resultado[0]
    
    def actualizarProduccion(self, id_produccion, fabrica, fabricacion, empaque, envios, transporte):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_ActualizarProduccion] ?, ?, ?, ?, ?, ?'
        cursor.execute(sp, (id_produccion, fabrica, fabricacion, empaque, envios, transporte))
        self.bd.conexion.commit()
        self.bd.cerrarConexionBD()
    
    def eliminarProduccion(self, id_produccion):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_EliminarProduccion] ?'
        cursor.execute(sp, (id_produccion,))
        self.bd.conexion.commit()
        self.bd.cerrarConexionBD()
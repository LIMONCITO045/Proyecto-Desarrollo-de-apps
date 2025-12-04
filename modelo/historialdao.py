from models import HistorialCambios
from conexionbd import ConexionBD

class HistorialDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.historial = HistorialCambios()
    
    def listarHistorial(self):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_ListarHistorial]'
        cursor.execute(sp)
        filas = cursor.fetchall()
        for fila in filas:
            print(f"ID: {fila[0]}, Tabla: {fila[1]}, Acción: {fila[2]}, Fecha: {fila[3]}, Usuario: {fila[4]}")
        self.bd.cerrarConexionBD()
        return filas
    
    def obtenerHistorialPorTabla(self, tabla):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_ObtenerHistorialPorTabla] ?'
        cursor.execute(sp, (tabla,))
        filas = cursor.fetchall()
        self.bd.cerrarConexionBD()
        return filas
    
    def insertarHistorial(self, tabla, accion, usuario):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_InsertarHistorial] ?, ?, ?'
        cursor.execute(sp, (tabla, accion, usuario))
        self.bd.conexion.commit()
        resultado = cursor.fetchone()
        self.bd.cerrarConexionBD()
        return resultado[0]
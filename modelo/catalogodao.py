from models import Catalogo
from conexionbd import ConexionBD

class CatalogoDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.catalogo = Catalogo()
    
    def listarCatalogos(self):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_ListarCatalogos]'
        cursor.execute(sp)
        filas = cursor.fetchall()
        for fila in filas:
            print(f"ID: {fila[0]}, Cantidad Productos: {fila[1]}")
        self.bd.cerrarConexionBD()
        return filas
    
    def insertarCatalogo(self, cantidad_productos):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_InsertarCatalogo] ?'
        cursor.execute(sp, (cantidad_productos,))
        self.bd.conexion.commit()
        resultado = cursor.fetchone()
        print(f"Catálogo insertado con ID: {resultado[0]}")
        self.bd.cerrarConexionBD()
        return resultado[0]
    
    def actualizarCatalogo(self, id_catalogo, cantidad_productos):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_ActualizarCatalogo] ?, ?'
        cursor.execute(sp, (id_catalogo, cantidad_productos))
        self.bd.conexion.commit()
        self.bd.cerrarConexionBD()
    
    def eliminarCatalogo(self, id_catalogo):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_EliminarCatalogo] ?'
        cursor.execute(sp, (id_catalogo,))
        self.bd.conexion.commit()
        self.bd.cerrarConexionBD()
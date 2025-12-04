"""
ClienteDAO - Versión corregida SIN usar fetchone() para INSERT
"""

from modelo.conexionbd import ConexionBD


class ClienteDAO:
    def __init__(self):
        self.bd = ConexionBD()
    
    def listarClientes(self):
        """Lista todos los clientes"""
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_ListarClientes]'
        cursor.execute(sp)
        filas = cursor.fetchall()
        self.bd.cerrarConexionBD()
        return filas
    
    def obtenerClientePorID(self, id_cliente):
        """Obtiene un cliente por su ID"""
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_ObtenerClientePorID] ?'
        cursor.execute(sp, (id_cliente,))
        fila = cursor.fetchone()
        self.bd.cerrarConexionBD()
        return fila
    
    def insertarCliente(self, nombre, pais, region):
        """
        Inserta un cliente nuevo y retorna su ID
        
        SOLUCIÓN: Hacer el INSERT y SELECT por separado
        
        Args:
            nombre (str): Nombre del cliente
            pais (str): País del cliente
            region (str): Región/Estado del cliente
        
        Returns:
            int: ID del cliente insertado
        """
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        
        try:
            # ✅ PASO 1: Hacer el INSERT
            sql_insert = """
                INSERT INTO clientes (Nombre, País, Región, Historial_compras)
                VALUES (?, ?, ?, 0)
            """
            cursor.execute(sql_insert, (nombre, pais, region))
            
            # ✅ PASO 2: Obtener el ID en una query separada
            sql_select = "SELECT @@IDENTITY AS id_cliente"
            cursor.execute(sql_select)
            resultado = cursor.fetchone()
            id_cliente = int(resultado[0])
            
            # ✅ PASO 3: Commit
            self.bd.conexion.commit()
            
            print(f"✓ Cliente insertado con ID: {id_cliente}")
            return id_cliente
            
        except Exception as e:
            self.bd.conexion.rollback()
            print(f"❌ Error al insertar cliente: {e}")
            raise
        finally:
            self.bd.cerrarConexionBD()
    
    def actualizarCliente(self, id_cliente, nombre, pais, region):
        """Actualiza los datos de un cliente"""
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        
        sql = """
            UPDATE clientes
            SET Nombre = ?, País = ?, Región = ?
            WHERE id_cliente = ?
        """
        
        cursor.execute(sql, (nombre, pais, region, id_cliente))
        self.bd.conexion.commit()
        self.bd.cerrarConexionBD()
    
    def eliminarCliente(self, id_cliente):
        """Elimina un cliente"""
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        
        sql = "DELETE FROM clientes WHERE id_cliente = ?"
        cursor.execute(sql, (id_cliente,))
        self.bd.conexion.commit()
        self.bd.cerrarConexionBD()
    
    def listarClientesPorRegion(self, region):
        """Lista clientes de una región específica"""
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = 'EXEC [dbo].[sp_ListarClientesPorRegion] ?'
        cursor.execute(sp, (region,))
        filas = cursor.fetchall()
        self.bd.cerrarConexionBD()
        return filas
    
    def incrementarHistorialCompras(self, id_cliente):
        """Incrementa el contador de compras del cliente"""
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        
        sql = """
            UPDATE clientes
            SET Historial_compras = Historial_compras + 1
            WHERE id_cliente = ?
        """
        
        cursor.execute(sql, (id_cliente,))
        self.bd.conexion.commit()
        self.bd.cerrarConexionBD()


# ============================================
# EJEMPLO DE USO
# ============================================
if __name__ == "__main__":
    dao = ClienteDAO()
    
    try:
        # Insertar cliente
        print("Insertando cliente...")
        id_cliente = dao.insertarCliente(
            nombre="Juan Pérez Test Direct",
            pais="México",
            region="Guanajuato"
        )
        print(f"✓ Cliente creado con ID: {id_cliente}")
        
        # Obtener cliente
        print(f"\nObteniendo cliente {id_cliente}...")
        cliente = dao.obtenerClientePorID(id_cliente)
        if cliente:
            print(f"✓ Cliente encontrado: {cliente[1]} de {cliente[2]}, {cliente[3]}")
        
        # Incrementar historial
        print(f"\nIncrementando historial de compras...")
        dao.incrementarHistorialCompras(id_cliente)
        print("✓ Historial incrementado")
        
        print("\n✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
from models import Pedido
from conexionbd import ConexionBD

class PedidoDAO:
    def __init__(self):
        self.bd = ConexionBD()
    
    def insertarPedidoConDetalle(self, destino, id_informacion_pedido, total, 
                                  id_cliente, id_produccion, id_catalogo, productos):
        """
        Inserta un pedido con múltiples productos
        
        Args:
            destino (str): Dirección de entrega
            id_informacion_pedido (int): ID de información del pedido (puede ser None)
            total (int): Total del pedido completo
            id_cliente (int): ID del cliente
            id_produccion (int): ID de producción
            id_catalogo (int): ID del catálogo
            productos (list): Lista de diccionarios con productos
                [
                    {
                        "id_producto": 1,
                        "cantidad": 2,
                        "precio_unitario": 100
                    },
                    ...
                ]
        
        Returns:
            int: ID del pedido creado
        """
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        
        try:
            # 1. Insertar pedido maestro
            sp = 'EXEC [dbo].[sp_InsertarPedidoMaestro] ?, ?, ?, ?, ?, ?'
            cursor.execute(sp, (destino, id_informacion_pedido, total, 
                              id_cliente, id_produccion, id_catalogo))
            resultado = cursor.fetchone()
            id_pedido = resultado[0]
            
            print(f"✓ Pedido maestro creado con ID: {id_pedido}")
            
            # 2. Insertar detalles de productos
            sp_detalle = 'EXEC [dbo].[sp_InsertarDetallePedido] ?, ?, ?, ?'
            
            for producto in productos:
                cursor.execute(sp_detalle, (
                    id_pedido,
                    producto['id_producto'],
                    producto['cantidad'],
                    producto['precio_unitario']
                ))
                resultado_detalle = cursor.fetchone()
                print(f"  ✓ Detalle agregado: Producto {producto['id_producto']}, "
                      f"cantidad {producto['cantidad']}, ID detalle: {resultado_detalle[0]}")
            
            self.bd.conexion.commit()
            print(f"✓ Pedido completo guardado exitosamente")
            
            return id_pedido
            
        except Exception as e:
            self.bd.conexion.rollback()
            print(f"❌ Error al insertar pedido con detalle: {e}")
            raise
        finally:
            self.bd.cerrarConexionBD()
    
    def insertarPedidoCompletoJSON(self, destino, id_informacion_pedido, total, 
                                    id_cliente, id_produccion, id_catalogo, 
                                    detalle_json):
        """
        Inserta un pedido completo usando JSON (alternativa más rápida)
        
        Args:
            detalle_json (str): JSON string con formato:
                '[{"id_producto":1,"cantidad":2,"precio_unitario":100}, ...]'
        
        Returns:
            int: ID del pedido creado
        """
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        
        try:
            sp = 'EXEC [dbo].[sp_InsertarPedidoCompleto] ?, ?, ?, ?, ?, ?, ?'
            cursor.execute(sp, (destino, id_informacion_pedido, total, 
                              id_cliente, id_produccion, id_catalogo, detalle_json))
            self.bd.conexion.commit()
            resultado = cursor.fetchone()
            id_pedido = resultado[0]
            
            print(f"✓ Pedido completo insertado con ID: {id_pedido}")
            return id_pedido
            
        except Exception as e:
            self.bd.conexion.rollback()
            print(f"❌ Error al insertar pedido completo: {e}")
            raise
        finally:
            self.bd.cerrarConexionBD()
    
    def listarPedidosConDetalle(self, id_pedido=None):
        """
        Lista pedidos con su detalle
        
        Args:
            id_pedido (int, optional): ID del pedido específico. None para todos.
        
        Returns:
            list: Lista de tuplas con información del pedido y productos
        """
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        
        sp = 'EXEC [dbo].[sp_ListarPedidosConDetalle] ?'
        cursor.execute(sp, (id_pedido,))
        filas = cursor.fetchall()
        
        self.bd.cerrarConexionBD()
        return filas
    
    def obtenerDetallePedido(self, id_pedido):
        """
        Obtiene el detalle completo de un pedido específico
        
        Returns:
            dict: Información del pedido con sus productos
        """
        filas = self.listarPedidosConDetalle(id_pedido)
        
        if not filas:
            return None
        
        # Estructurar la información
        pedido = {
            'id_pedido': filas[0][0],
            'destino': filas[0][1],
            'total': filas[0][2],
            'cliente': {
                'nombre': filas[0][3],
                'pais': filas[0][4],
                'region': filas[0][5]
            },
            'productos': []
        }
        
        for fila in filas:
            if fila[6] is not None:  # Si tiene detalle
                pedido['productos'].append({
                    'id_detalle': fila[6],
                    'id_producto': fila[7],
                    'tipo': fila[8],
                    'cantidad': fila[9],
                    'precio_unitario': fila[10],
                    'subtotal': fila[11]
                })
        
        return pedido
    
    # ============================================
    # MÉTODOS LEGACY (para compatibilidad)
    # ============================================
    
    def insertarPedido(self, destino, id_informacion_pedido, total, id_producto, 
                       id_cliente, id_produccion, id_catalogo):
        """
        MÉTODO DEPRECADO - Usar insertarPedidoConDetalle() en su lugar
        
        Mantenido solo para compatibilidad con código antiguo
        """
        print("⚠️ ADVERTENCIA: insertarPedido() está deprecado. "
              "Usar insertarPedidoConDetalle() en su lugar")
        
        # Crear un pedido con un solo producto
        productos = [{
            'id_producto': id_producto,
            'cantidad': 1,
            'precio_unitario': total
        }]
        
        return self.insertarPedidoConDetalle(
            destino, id_informacion_pedido, total, 
            id_cliente, id_produccion, id_catalogo, productos
        )


# ============================================
# EJEMPLO DE USO
# ============================================
if __name__ == "__main__":
    dao = PedidoDAO()
    
    # Ejemplo: Crear pedido con múltiples productos
    productos = [
        {
            'id_producto': 1,
            'cantidad': 2,
            'precio_unitario': 120
        },
        {
            'id_producto': 2,
            'cantidad': 1,
            'precio_unitario': 45
        }
    ]
    
    try:
        id_pedido = dao.insertarPedidoConDetalle(
            destino="Calle Principal #123, León, Guanajuato",
            id_informacion_pedido=None,
            total=285,  # 120*2 + 45*1
            id_cliente=1,
            id_produccion=1,
            id_catalogo=1,
            productos=productos
        )
        
        print(f"\n✓ Pedido creado exitosamente: #{id_pedido}")
        
        # Obtener detalle del pedido
        detalle = dao.obtenerDetallePedido(id_pedido)
        print(f"\nDetalle del pedido:")
        print(f"Cliente: {detalle['cliente']['nombre']}")
        print(f"Total: ${detalle['total']} USD")
        print(f"Productos:")
        for prod in detalle['productos']:
            print(f"  - {prod['tipo']}: {prod['cantidad']} x ${prod['precio_unitario']} = ${prod['subtotal']}")
            
    except Exception as e:
        print(f"Error: {e}")
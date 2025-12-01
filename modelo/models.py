# models/models.py
"""
Modelos de datos para la base de datos Top Flow
Cada clase representa una tabla en la base de datos
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class Cliente:
    """Modelo para la tabla clientes"""
    id_cliente: Optional[int] = None
    Nombre: str = ""
    Pais: str = ""
    Region: str = ""
    Historial_compras: int = 0
    
    def __str__(self):
        return f"Cliente {self.id_cliente}: {self.Nombre} - {self.Pais}"


@dataclass
class Catalogo:
    """Modelo para la tabla catalogo"""
    id_catalogo: Optional[int] = None
    cantidad_productos: int = 0
    
    def __str__(self):
        return f"Catálogo {self.id_catalogo}: {self.cantidad_productos} productos"


@dataclass
class Producto:
    """Modelo para la tabla productos"""
    id_producto: Optional[int] = None
    tipo: str = ""
    precio: int = 0
    talla: str = ""
    id_catalogo: int = 0
    
    def __str__(self):
        return f"Producto {self.id_producto}: {self.tipo} - Talla {self.talla} - ${self.precio}"


@dataclass
class Produccion:
    """Modelo para la tabla produccion"""
    id_produccion: Optional[int] = None
    fabrica: str = ""
    fabricacion: Optional[date] = None
    empaque: Optional[date] = None
    envios: Optional[date] = None
    transporte: str = ""
    
    def __str__(self):
        return f"Producción {self.id_produccion}: {self.fabrica}"


@dataclass
class Pedido:
    """Modelo para la tabla pedidos"""
    id_pedidos: Optional[int] = None
    destino: str = ""
    id_informacion_pedido: int = 0
    total: int = 0
    id_producto: int = 0
    id_cliente: int = 0
    id_produccion: int = 0
    id_catalogo: int = 0
    
    def __str__(self):
        return f"Pedido {self.id_pedidos}: Destino {self.destino} - Total ${self.total}"


@dataclass
class Cobranza:
    """Modelo para la tabla cobranza"""
    id_pedidos: int = 0  # PK
    monto: int = 0
    metodo_de_pago: str = ""
    banco: str = ""
    verificacion: str = ""
    
    def __str__(self):
        return f"Cobranza Pedido {self.id_pedidos}: ${self.monto} - {self.metodo_de_pago}"


@dataclass
class GananciaEmpresa:
    """Modelo para la tabla ganancia_empresa"""
    id_producto: int = 0  # PK
    ganancia: int = 0
    descuento: int = 0
    
    def __str__(self):
        return f"Ganancia Producto {self.id_producto}: ${self.ganancia} - {self.descuento}% desc"


@dataclass
class AtencionCliente:
    """Modelo para la tabla atencion_a_clientes"""
    id_cliente: int = 0
    consulta: str = ""
    solucion: str = ""
    tiempo: int = 0
    
    def __str__(self):
        return f"Atención Cliente {self.id_cliente}: {self.consulta} - {self.tiempo} min"


@dataclass
class HistorialCambios:
    """Modelo para la tabla historial_cambios"""
    id_historial: Optional[int] = None
    tabla: str = ""
    accion: str = ""
    fecha: Optional[datetime] = None
    usuario: str = ""
    
    def __str__(self):
        return f"Cambio {self.id_historial}: {self.accion} en {self.tabla} - {self.fecha}"
    
@dataclass
class Usuario:
    """Modelo para la tabla usuario"""
    nombre: str = ""  # PK
    contraseña: str = ""
    
    def __str__(self):
        return f"Usuario: {self.nombre}"


# Diccionario para mapear nombres de tablas a clases
MODELS = {
    'clientes': Cliente,
    'catalogo': Catalogo,
    'productos': Producto,
    'produccion': Produccion,
    'pedidos': Pedido,
    'cobranza': Cobranza,
    'ganancia_empresa': GananciaEmpresa,
    'atencion_a_clientes': AtencionCliente,
    'historial_cambios': HistorialCambios,
    'usuario' : Usuario
}


def get_model(table_name: str):
    """
    Obtener la clase del modelo según el nombre de la tabla
    
    Args:
        table_name (str): Nombre de la tabla
        
    Returns:
        Class: Clase del modelo correspondiente
    """
    return MODELS.get(table_name.lower())
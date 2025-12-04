"""
Top Flow - Sistema de Gestión Web
Aplicación Reflex con catálogo de productos y carrito de compras
"""

import reflex as rx
from typing import List
from pydantic import BaseModel
import sys
import os

# Agregar la ruta del proyecto al path para importar los DAOs
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modelo.productodao import ProductoDAO
from modelo.pedidodao import PedidoDAO

# Mapeo de productos a emojis - CORREGIDO Y AMPLIADO
EMOJIS_PRODUCTOS = {
    # Ropa superior
    "camisa": "👔", "blusa": "👚", "playera": "👕",
    "polo": "👕", "camiseta": "👕",
    
    # Ropa inferior
    "pantalon": "👖", "pantalón": "👖", "jeans": "👖",
    "short": "🩳", "bermuda": "🩳", "shorts": "🩳",
    "falda": "👗",
    
    # Calzado
    "zapato": "👞", "tenis": "👟", "calzado": "👟",
    "sandalia": "👡", "sandalias": "👡",
    "bota": "🥾", "botas": "🥾",
    "zapatilla": "👟", "zapatillas": "👟",
    
    # Vestidos y trajes
    "vestido": "👗",
    "traje": "🤵", "suit": "🤵",
    
    # Abrigos y chaquetas
    "chaqueta": "🧥", "chamarra": "🧥", "jacket": "🧥",
    "abrigo": "🧥", "chaleco": "🦺",
    "sudadera": "🧥", "hoodie": "🧥",
    
    # Accesorios para la cabeza
    "gorra": "🧢", "cap": "🧢",
    "sombrero": "🎩", "hat": "🎩",
    "kangol": "🎩",
    
    # Bolsos y mochilas
    "bolso": "👜", "bolsa": "👜", "bag": "👜",
    "mochila": "🎒", "backpack": "🎒",
    "jansport": "🎒",
    
    # Accesorios
    "bufanda": "🧣", "scarf": "🧣",
    "corbata": "👔", "tie": "👔",
    "cinturon": "👖", "cinturón": "👖", "belt": "👖",
    "guante": "🧤", "guantes": "🧤", "gloves": "🧤",
    "pañuelo": "🧣",
    "calcetines": "🧦", "calcetín": "🧦", "socks": "🧦",
    
    # Relojes y joyería
    "reloj": "⌚", "watch": "⌚",
    "fossil": "⌚",
    
    # Ropa interior y pijamas
    "pijama": "👔", "pajama": "👔",
    
    # Deportivo
    "nike": "👟", "adidas": "👟",
    
    # Marcas específicas
    "birkenstock": "👡",
    "timberland": "🥾",
    "michael kors": "👜",
    "hugo boss": "🤵",
    "zara": "👔",
    "uniqlo": "🧥",
}


class Producto(BaseModel):
    """Modelo de producto para Reflex"""
    id_producto: int
    tipo: str
    precio: int
    talla: str
    id_catalogo: int
    cantidad: int = 0
    emoji: str = "👔"


class CartItem(BaseModel):
    """Modelo para items del carrito"""
    id_producto: int
    tipo: str
    precio: int
    talla: str
    id_catalogo: int
    cantidad: int = 1
    emoji: str = "👔"


class State(rx.State):
    """Estado global de la aplicación"""
    
    productos: List[Producto] = []
    carrito: List[CartItem] = []
    total: int = 0
    mensaje: str = ""
    cargando: bool = False
    mostrar_checkout: bool = False
    destino: str = ""
    nombre_cliente: str = ""
    pais_cliente: str = ""
    region_cliente: str = ""
    
    def obtener_emoji(self, tipo: str) -> str:
        """Obtener emoji basado en el tipo de producto"""
        tipo_lower = tipo.lower()
        
        # Buscar coincidencias exactas primero
        for palabra_clave, emoji in EMOJIS_PRODUCTOS.items():
            if palabra_clave == tipo_lower:
                return emoji
        
        # Luego buscar palabras contenidas
        for palabra_clave, emoji in EMOJIS_PRODUCTOS.items():
            if palabra_clave in tipo_lower:
                return emoji
        
        # Si no encuentra nada, retornar emoji por defecto
        return "👔"
    
    def cargar_productos(self):
        """Cargar productos desde la base de datos"""
        self.cargando = True
        self.mensaje = ""
        
        try:
            dao = ProductoDAO()
            filas = dao.listarProductos()
            
            if filas:
                self.productos = [
                    Producto(
                        id_producto=fila[0],
                        tipo=fila[1],
                        precio=fila[2],
                        talla=fila[3],
                        id_catalogo=fila[4],
                        cantidad=fila[5] if len(fila) > 5 else 0,
                        emoji=self.obtener_emoji(fila[1])
                    )
                    for fila in filas
                ]
                print(f"✓ Cargados {len(self.productos)} productos desde la BD")
            else:
                self.mensaje = "⚠️ No hay productos en la base de datos"
                self.productos = []
                
        except Exception as e:
            print(f"Error al cargar productos: {e}")
            self.mensaje = f"⚠️ Error al conectar con la base de datos: {str(e)}"
            self.productos = []
        
        self.cargando = False
    
    def agregar_al_carrito(self, producto: Producto):
        """Agregar producto al carrito"""
        if producto.cantidad <= 0:
            self.mensaje = f"⚠️ {producto.tipo} está agotado"
            return
        
        cantidad_en_carrito = 0
        for item in self.carrito:
            if item.id_producto == producto.id_producto:
                cantidad_en_carrito = item.cantidad
                break
        
        if cantidad_en_carrito >= producto.cantidad:
            self.mensaje = f"⚠️ No hay más stock de {producto.tipo} (máximo: {producto.cantidad})"
            return
        
        for item in self.carrito:
            if item.id_producto == producto.id_producto:
                item.cantidad += 1
                self.calcular_total()
                self.mensaje = f"✓ {producto.tipo} agregado (cantidad: {item.cantidad}/{producto.cantidad})"
                return
        
        nuevo_item = CartItem(
            id_producto=producto.id_producto,
            tipo=producto.tipo,
            precio=producto.precio,
            talla=producto.talla,
            id_catalogo=producto.id_catalogo,
            cantidad=1,
            emoji=producto.emoji
        )
        self.carrito.append(nuevo_item)
        self.calcular_total()
        self.mensaje = f"✓ {producto.tipo} agregado al carrito"
    
    def eliminar_del_carrito(self, id_producto: int):
        """Eliminar producto del carrito"""
        self.carrito = [item for item in self.carrito if item.id_producto != id_producto]
        self.calcular_total()
        self.mensaje = "✓ Producto eliminado del carrito"
    
    def aumentar_cantidad(self, id_producto: int):
        """Aumentar cantidad de un producto en el carrito"""
        producto_stock = None
        for p in self.productos:
            if p.id_producto == id_producto:
                producto_stock = p
                break
        
        for item in self.carrito:
            if item.id_producto == id_producto:
                if producto_stock and item.cantidad >= producto_stock.cantidad:
                    self.mensaje = f"⚠️ No hay más stock de {item.tipo} (máximo: {producto_stock.cantidad})"
                    return
                item.cantidad += 1
                self.calcular_total()
                return
    
    def disminuir_cantidad(self, id_producto: int):
        """Disminuir cantidad de un producto en el carrito"""
        for item in self.carrito:
            if item.id_producto == id_producto:
                if item.cantidad > 1:
                    item.cantidad -= 1
                    self.calcular_total()
                else:
                    self.eliminar_del_carrito(id_producto)
                return
    
    def calcular_total(self):
        """Calcular el total del carrito"""
        self.total = sum(item.precio * item.cantidad for item in self.carrito)
    
    def abrir_checkout(self):
        """Mostrar formulario de checkout"""
        if not self.carrito:
            self.mensaje = "⚠️ El carrito está vacío"
            return
        self.mostrar_checkout = True
        self.mensaje = ""
    
    def cancelar_checkout(self):
        """Cancelar checkout"""
        self.mostrar_checkout = False
        self.destino = ""
        self.nombre_cliente = ""
        self.pais_cliente = ""
        self.region_cliente = ""
    
    def realizar_pedido(self):
        """Guardar pedido en la base de datos"""
        if not self.destino or not self.nombre_cliente or not self.pais_cliente or not self.region_cliente:
            self.mensaje = "⚠️ Por favor completa todos los campos"
            return
        
        try:
            from modelo.clientedao import ClienteDAO
            
            # 1. CREAR CLIENTE
            cliente_dao = ClienteDAO()
            id_cliente = cliente_dao.insertarCliente(
                nombre=self.nombre_cliente,
                pais=self.pais_cliente,
                region=self.region_cliente
            )
            print(f"✓ Cliente creado con ID: {id_cliente}")
            
            # 2. PREPARAR LISTA DE PRODUCTOS PARA EL PEDIDO
            productos = []
            for item in self.carrito:
                productos.append({
                    'id_producto': item.id_producto,
                    'cantidad': item.cantidad,
                    'precio_unitario': item.precio
                })
            
            # 3. CREAR UN SOLO PEDIDO CON TODOS LOS PRODUCTOS
            pedido_dao = PedidoDAO()
            id_pedido = pedido_dao.insertarPedidoConDetalle(
                destino=self.destino,
                id_informacion_pedido=None,
                total=self.total,  # Total completo del carrito
                id_cliente=id_cliente,
                id_produccion=1,
                id_catalogo=self.carrito[0].id_catalogo if self.carrito else 1,
                productos=productos
            )
            
            print(f"✓ Pedido #{id_pedido} creado con {len(productos)} productos")
            
            # 4. INCREMENTAR HISTORIAL DE COMPRAS
            cliente_dao.incrementarHistorialCompras(id_cliente)
            
            # 5. PREPARAR RESUMEN DE PRODUCTOS
            resumen_productos = "\n".join([
                f"  • {item.emoji} {item.tipo} (Talla {item.talla}) x{item.cantidad} - ${item.precio * item.cantidad} USD"
                for item in self.carrito
            ])
            
            self.mensaje = f"✓ ¡Pedido #{id_pedido} realizado exitosamente!\n\n" \
                          f"👤 Cliente: {self.nombre_cliente}\n" \
                          f"🌍 País: {self.pais_cliente}\n" \
                          f"📍 Región: {self.region_cliente}\n" \
                          f"🏠 Destino: {self.destino}\n\n" \
                          f"📦 Productos ({len(self.carrito)}):\n{resumen_productos}\n\n" \
                          f"💰 Total: ${self.total} USD"
            
            self.carrito = []
            self.total = 0
            self.mostrar_checkout = False
            self.destino = ""
            self.nombre_cliente = ""
            self.pais_cliente = ""
            self.region_cliente = ""
            
        except Exception as e:
            import traceback
            error_detallado = traceback.format_exc()
            print(f"Error detallado al realizar pedido:\n{error_detallado}")
            self.mensaje = f"⚠️ Error al procesar el pedido: {str(e)}"


def navbar() -> rx.Component:
    """Barra de navegación"""
    return rx.box(
        rx.hstack(
            rx.heading("Top Flow", size="7", color="white", weight="bold"),
            rx.spacer(),
            rx.hstack(
                rx.link(rx.button(rx.hstack(rx.icon("home", size=18), rx.text("Inicio"), spacing="2"), variant="ghost", color_scheme="gray"), href="/"),
                rx.link(rx.button(rx.hstack(rx.icon("package", size=18), rx.text("Productos"), spacing="2"), variant="ghost", color_scheme="gray"), href="/productos"),
                rx.link(
                    rx.button(
                        rx.hstack(
                            rx.icon("shopping-cart", size=18),
                            rx.text("Carrito"),
                            rx.cond(State.carrito.length() > 0, rx.badge(State.carrito.length(), color_scheme="red", variant="solid")),
                            spacing="2"
                        ),
                        variant="ghost",
                        color_scheme="gray"
                    ),
                    href="/carrito"
                ),
                spacing="2",
            ),
            align="center",
            padding_x="2em",
            padding_y="1em",
        ),
        background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        box_shadow="0 4px 6px rgba(0,0,0,0.1)",
        width="100%",
        position="sticky",
        top="0",
        z_index="1000",
    )


def producto_card(producto: Producto) -> rx.Component:
    """Tarjeta de producto con emoji"""
    return rx.card(
        rx.vstack(
            rx.text(
                producto.emoji,
                font_size="72px",
                line_height="1",
            ),
            rx.heading(producto.tipo, size="5", weight="bold", text_align="center"),
            rx.text(f"Talla: {producto.talla}", color="gray", size="2"),
            # Badge de stock con rx.cond
            rx.cond(
                producto.cantidad > 10,
                rx.badge(f"{producto.cantidad} disponibles", color_scheme="green", size="2"),
                rx.cond(
                    producto.cantidad > 0,
                    rx.badge(f"{producto.cantidad} disponibles", color_scheme="orange", size="2"),
                    rx.badge("Agotado", color_scheme="red", size="2"),
                ),
            ),
            rx.spacer(),
            rx.text(f"${producto.precio} USD", size="7", weight="bold", color="#667eea"),
            rx.button(
                rx.hstack(rx.icon("shopping-cart", size=16), rx.text("Agregar"), spacing="2"),
                on_click=lambda: State.agregar_al_carrito(producto),
                color_scheme="purple",
                width="100%",
                size="3",
                disabled=producto.cantidad <= 0,
            ),
            spacing="3",
            align="center",
            height="100%",
        ),
        padding="1.5em",
    )


def carrito_item(item: CartItem) -> rx.Component:
    """Item del carrito"""
    subtotal = item.precio * item.cantidad
    
    return rx.card(
        rx.hstack(
            rx.text(item.emoji, font_size="48px", line_height="1"),
            rx.vstack(
                rx.heading(item.tipo, size="4", weight="bold"),
                rx.text(f"Talla: {item.talla}", color="gray", size="2"),
                rx.hstack(
                    rx.icon_button(rx.icon("minus", size=14), on_click=lambda: State.disminuir_cantidad(item.id_producto), size="1", variant="soft", color_scheme="purple"),
                    rx.text(f"{item.cantidad}", weight="bold", size="3"),
                    rx.icon_button(rx.icon("plus", size=14), on_click=lambda: State.aumentar_cantidad(item.id_producto), size="1", variant="soft", color_scheme="purple"),
                    spacing="2",
                ),
                spacing="1",
                align="start",
            ),
            rx.spacer(),
            rx.vstack(
                rx.text(f"${subtotal} USD", size="5", weight="bold", color="#667eea"),
                rx.text(f"${item.precio} c/u", size="1", color="gray"),
                rx.icon_button(rx.icon("trash-2", size=16), on_click=lambda: State.eliminar_del_carrito(item.id_producto), color_scheme="red", variant="ghost", size="2"),
                spacing="2",
                align="end",
            ),
            align="center",
            width="100%",
        ),
        padding="1em",
    )


def formulario_checkout() -> rx.Component:
    """Formulario de checkout"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Finalizar Pedido"),
            rx.dialog.description("Completa la información para realizar tu pedido"),
            rx.vstack(
                # Información del Cliente
                rx.text("Información del Cliente", weight="bold", size="4", color="#667eea"),
                rx.input(
                    placeholder="Nombre completo",
                    value=State.nombre_cliente,
                    on_change=State.set_nombre_cliente,
                    size="3"
                ),
                
                # País
                rx.text("País", weight="bold", size="3", margin_top="0.5em"),
                rx.select(
                    ["México", "Estados Unidos", "Canadá", "España", "Colombia", "Argentina", "Chile", "Perú"],
                    placeholder="Selecciona tu país",
                    value=State.pais_cliente,
                    on_change=State.set_pais_cliente,
                    size="3",
                ),
                
                # Región/Estado
                rx.text("Región/Estado", weight="bold", size="3", margin_top="0.5em"),
                rx.input(
                    placeholder="Ej: Guanajuato, Ciudad de México, California",
                    value=State.region_cliente,
                    on_change=State.set_region_cliente,
                    size="3"
                ),
                
                # Dirección de Envío
                rx.text("Dirección de Envío", weight="bold", size="4", color="#667eea", margin_top="1em"),
                rx.text_area(
                    placeholder="Calle, número, colonia, código postal, ciudad",
                    value=State.destino,
                    on_change=State.set_destino,
                    rows="4"
                ),
                
                rx.divider(),
                
                # Total
                rx.hstack(
                    rx.text("Total a pagar:", weight="bold", size="4"),
                    rx.spacer(),
                    rx.text(f"${State.total} USD", weight="bold", size="5", color="#667eea"),
                    width="100%",
                ),
                spacing="2",
                width="100%",
            ),
            rx.hstack(
                rx.dialog.close(
                    rx.button(
                        "Cancelar",
                        variant="soft",
                        color_scheme="gray",
                        on_click=State.cancelar_checkout
                    )
                ),
                rx.button(
                    rx.hstack(
                        rx.icon("check-check", size=18),
                        rx.text("Confirmar Pedido"),
                        spacing="2"
                    ),
                    on_click=State.realizar_pedido,
                    color_scheme="purple"
                ),
                spacing="3",
                justify="end",
                width="100%",
                margin_top="1em",
            ),
            max_width="550px",
            padding="1.5em",
        ),
        open=State.mostrar_checkout,
    )


def index() -> rx.Component:
    """Página principal"""
    return rx.box(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("Bienvenido a Top Flow", size="9", background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)", background_clip="text", weight="bold"),
                rx.text("Tu tienda de ropa en línea - León, Guanajuato", size="5", color="gray"),
                rx.box(height="3em"),
                rx.grid(
                    rx.card(rx.vstack(rx.text("👕", font_size="48px"), rx.heading("Productos de Calidad", size="5", weight="bold"), rx.text("Ropa de las mejores marcas", color="gray", text_align="center", size="2"), spacing="3", align="center"), padding="2em"),
                    rx.card(rx.vstack(rx.text("🚚", font_size="48px"), rx.heading("Envío Rápido", size="5", weight="bold"), rx.text("Entrega a domicilio", color="gray", text_align="center", size="2"), spacing="3", align="center"), padding="2em"),
                    rx.card(rx.vstack(rx.text("💳", font_size="48px"), rx.heading("Precios en USD", size="5", weight="bold"), rx.text("Pagos internacionales", color="gray", text_align="center", size="2"), spacing="3", align="center"), padding="2em"),
                    columns="3",
                    spacing="4",
                ),
                rx.box(height="2em"),
                rx.link(rx.button(rx.hstack(rx.text("Ver Catálogo"), rx.icon("arrow-right", size=18), spacing="2"), size="4", color_scheme="purple"), href="/productos"),
                spacing="5",
                justify="center",
                min_height="80vh",
                padding="2em",
            ),
            max_width="1200px",
        ),
    )


def productos() -> rx.Component:
    """Página de productos"""
    return rx.box(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("Catálogo de Productos", size="8", weight="bold"),
                rx.text("Precios en USD - Stock disponible", color="gray", size="3"),
                rx.cond(State.mensaje != "", rx.callout(State.mensaje, icon="info", color_scheme="green")),
                rx.box(height="1em"),
                rx.cond(
                    State.cargando,
                    rx.center(rx.spinner(size="3", color="purple"), padding="4em"),
                    rx.cond(
                        State.productos.length() > 0,
                        rx.grid(rx.foreach(State.productos, producto_card), columns="3", spacing="4", width="100%"),
                        rx.center(rx.vstack(rx.icon("package-x", size=64, color="gray"), rx.heading("No hay productos", size="6", color="gray"), spacing="4", align="center"), padding="4em"),
                    ),
                ),
                spacing="4",
                padding="2em",
                width="100%",
            ),
            max_width="1200px",
        ),
        on_mount=State.cargar_productos,
    )


def carrito() -> rx.Component:
    """Página del carrito"""
    return rx.box(
        navbar(),
        formulario_checkout(),
        rx.container(
            rx.vstack(
                rx.heading("Tu Carrito de Compras", size="8", weight="bold"),
                rx.cond(State.mensaje != "", rx.callout(State.mensaje, icon="info")),
                rx.box(height="1em"),
                rx.cond(
                    State.carrito.length() > 0,
                    rx.vstack(
                        rx.foreach(State.carrito, carrito_item),
                        rx.divider(),
                        rx.card(
                            rx.vstack(
                                rx.hstack(rx.heading("Total:", size="6"), rx.spacer(), rx.heading(f"${State.total} USD", size="7", color="#667eea"), width="100%"),
                                rx.button(rx.hstack(rx.icon("package-check", size=18), rx.text("Realizar Pedido"), spacing="2"), on_click=State.abrir_checkout, size="4", color_scheme="purple", width="100%"),
                                spacing="3",
                            ),
                            padding="1.5em",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    rx.center(
                        rx.vstack(
                            rx.text("🛒", font_size="64px"),
                            rx.heading("Tu carrito está vacío", size="6", color="gray"),
                            rx.link(rx.button(rx.hstack(rx.icon("package", size=18), rx.text("Ir a Productos"), spacing="2"), color_scheme="purple", size="3"), href="/productos"),
                            spacing="4",
                            align="center",
                        ),
                        padding="4em",
                    ),
                ),
                spacing="4",
                padding="2em",
                width="100%",
            ),
            max_width="800px",
        ),
    )


app = rx.App(theme=rx.theme(appearance="dark", accent_color="purple"))
app.add_page(index, route="/")
app.add_page(productos, route="/productos")
app.add_page(carrito, route="/carrito")
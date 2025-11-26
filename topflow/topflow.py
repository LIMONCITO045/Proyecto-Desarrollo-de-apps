import reflex as rx

def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("Top Flow - Sistema de Gestión", size="9"),
            rx.text("Bienvenido al sistema de gestión de productos"),
            rx.button("Ir a Productos", on_click=rx.redirect("/productos")),
            spacing="5",
            justify="center",
            min_height="85vh",
        )
    )

def productos() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("Lista de Productos", size="7"),
            rx.text("Aquí irá la tabla de productos"),
            rx.button("Volver", on_click=rx.redirect("/")),
            spacing="4",
        )
    )

app = rx.App()
app.add_page(index)
app.add_page(productos, route="/productos")
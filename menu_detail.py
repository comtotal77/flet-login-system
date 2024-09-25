import flet as ft

class MenuDetail:
    def __init__(self):
        self.hola = 1

    def build(self) -> ft.Container:
        return ft.Container(
            bgcolor = ft.colors.BLUE_100,
            width = 800,
            height = 40,
            padding = 0,
            content=ft.Column([
                ft.Text("Control Inventario CID", size=20,color="BLACK"),
            ])
        )
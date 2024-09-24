import flet as ft

class MenuDetail:
    def __init__(self):
        self.hola = 1

    def build(self) -> ft.Container:
        return ft.Container(
            bgcolor = ft.colors.RED_500,
            width = 800,
            height = 50,
            padding = 0,
            content=ft.Column([
                ft.Text("Ojoooo", size=20),
            ])
        )
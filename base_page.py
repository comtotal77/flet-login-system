import flet as ft
from menu_detail import MenuDetail

class BasePage:
    def __init__(self, page):
        self.page = page  # Referencia a la página
        self.configure_page()  # Configura las propiedades comunes de la página

    def configure_page(self):
        """Método para aplicar las configuraciones comunes de la página"""
        self.page.bgcolor = ft.colors.BLUE_500
        self.page.padding = 10
        self.page.window_width = 800
        self.page.window_height = 600

    def common_layout(self, content):
        """Método para aplicar un layout común a todas las páginas"""
        return ft.Container(
            bgcolor=self.page.bgcolor,
            width=self.page.width,
            height=self.page.height,
            padding=self.page.padding,

            content=ft.Column(
                [
                    MenuDetail().build(),
                    content,  # Contenido específico de la página
                    ft.Text("Footer", size=20),  # Footer común
                ],
                # alignment=ft.MainAxisAlignment.CENTER,
            ),
        )    
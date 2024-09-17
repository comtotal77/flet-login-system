import flet as ft

class PrivatePage:
    def __init__(self, page):
        self.page = page  # Guardamos la referencia a la página

    def build(self) -> ft.Container:
        msg = ''
        if self.page.session.contains_key("loginme"):
            datalogin = self.page.session.get("loginme")
            if datalogin["value"]:
                name = datalogin["username"]
                msg = f"Hello {name}"
        return ft.Container(
            bgcolor=ft.colors.BLUE_200,
            padding=10,
            content=ft.Column([
                ft.Text("Sección del usuario", size=30),
                ft.Text(f"{msg}"),
                ft.Row([ft.ElevatedButton("Logout",
                                  bgcolor=ft.colors.RED,
                                  color=ft.colors.WHITE,
                                  on_click=self.logout
                                  ),
                        ft.ElevatedButton("Ir a segunda",
                                        bgcolor=ft.colors.BLUE,
                                        color=ft.colors.YELLOW,
                                        on_click=self.segunda
                                        )
                ])
            ])
        )

    def logout(self, e):
        self.page.session.clear()
        self.page.go('/login')
        self.page.update()

    def segunda(self, e):
        self.page.go('/conteo')
        self.page.update()
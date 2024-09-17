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
                ft.Text("Welcome to inner section", size=30),
                ft.Text(f"{msg}"),
                ft.ElevatedButton("Logout",
                                  bgcolor=ft.colors.RED,
                                  color=ft.colors.WHITE,
                                  on_click=self.logout
                                  )
            ])
        )

    def logout(self, e):
        self.page.session.clear()
        self.page.go('/login')
        self.page.update()

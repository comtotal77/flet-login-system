import flet as ft
import json

class RegisterPage:
    def __init__(self, page):
        self.page = page  # Guardamos la referencia a la página
        self.username = ft.TextField(label="User name")
        self.password = ft.TextField(label="Password")

    def build(self) -> ft.Container:
        return ft.Container(
            bgcolor=ft.colors.GREEN_200,
            padding=10,
            content=ft.Column([
                ft.Text("Register", size=30),
                self.username,
                self.password,
                ft.ElevatedButton("Register",
                                  bgcolor="blue", color="white",
                                  on_click=self.registerbtn
                                  ),
                ft.TextButton("Cancel",
                              on_click=self.cancelbtn),
            ])
        )

    def registerbtn(self, e):
        new_user = {
            "name": self.username.value,
            "password": self.password.value,
        }
        data = {"users": [new_user]}
        with open('login.json', 'w') as f:
            f.write(json.dumps(data))

        self.page.go("/login")
        self.page.update()

    def cancelbtn(self, e):
        self.page.go("/login")
        self.page.update()



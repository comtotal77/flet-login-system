import flet as ft
import json

from data_base import DataAccess
from base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page  # Guardamos la referencia a la página
        self.username = ft.TextField(label="User name")
        self.password = ft.TextField(label="Password", password=True, can_reveal_password=True)

    def build(self) -> ft.Container:
        
        login_content = ft.Column(
            [
                
                ft.Text("Login Account", size=30),
                self.username,
                self.password,
                ft.ElevatedButton("Login Now",
                                bgcolor="blue", color="white",
                                on_click=self.loginbtn
                                ),
                ft.TextButton("Register me",
                            on_click=self.registerbtn
                            ),

            ]
        )
        # Llama al layout común con el contenido específico de login
        return self.common_layout(login_content)

    def loginbtn(self, e):
        found = False
        username = self.username.value
        password = self.password.value
        found= DataAccess()
        encontro=found.buscaLogin(username,password)
        if encontro:
            print("Redirecting...")
            datalogin = {
                "value": True,
                "datos": encontro
            }

            self.page.session.set("loginme", datalogin)
            self.page.go("/private")
        else:
            print("Login failed !!!")
            snack_bar = ft.SnackBar(
                ft.Text("Wrong login", size=30),
                bgcolor="red"
            )
            # Añadir snack bar a la página usando overlay
            self.page.overlay.append(snack_bar)
            snack_bar.open = True
            self.username.value=""
            self.password.value=""
        self.page.update()

    def registerbtn(self, e):
        self.page.go("/register")
        self.page.update()
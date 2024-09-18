import flet as ft
import json


class LoginPage:
    def __init__(self, page):
        self.page = page  # Guardamos la referencia a la página
        self.username = ft.TextField(label="Usuario")
        self.password = ft.TextField(label="Contraseña")

    def build(self) -> ft.Container:
        return ft.Container(
            gradient= ft.LinearGradient(['indigo', 'blue']),     
            width=380,
            height=300,
            border_radius=20,
            padding=10,
            content=ft.Column([
                ft.Text("Ingresar", size=30, width=360, weight="w900", text_align="center"),
                self.username,
                self.password,
                ft.Container(
                            ft.ElevatedButton(
                                content = ft.Text(
                                    'INICIAR',
                                    color = 'white',
                                    weight ='w500',
                                    ),
                                width =280,
                                bgcolor = 'blue',
                                on_click=self.loginbtn,
                                ),
                                padding = ft.padding.only(25,10)
                            ),
                ft.Container(
                            ft.Row([
                                ft.Text(
                                    '¿No tienes una cuenta?'
                                    ),
                                ft.TextButton(
                                    'Crear una cuenta', on_click=self.registerbtn
                                    ),
                                ], spacing=8),
                            padding = ft.padding.only(40)
                ),
            ])
        )

    def loginbtn(self, e):
        with open('login.json', 'r') as f:
            data = json.load(f)
        username = self.username.value
        password = self.password.value

        found = False
        for user in data["users"]:
            if user['name'] == username and user['password'] == password:
                found = True
                print("Login success !!!")
                datalogin = {
                    "value": True,
                    "username": username
                }
                break

        if found:
            print("Redirecting...")
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
        self.page.update()

    def registerbtn(self, e):
        self.page.go("/register")
        self.page.update()
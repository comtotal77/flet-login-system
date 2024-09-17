import flet as ft
import json


class LoginPage:
    def __init__(self, page):
        self.page = page  # Guardamos la referencia a la página
        self.username = ft.TextField(label="User name")
        self.password = ft.TextField(label="Password")

    def build(self) -> ft.Container:
        return ft.Container(
            bgcolor=ft.colors.YELLOW_200,
            padding=10,
            content=ft.Column([
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
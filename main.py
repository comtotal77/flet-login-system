import json
import os
import flet as ft


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


def main(page: ft.Page):
    current_working_directory = os.getcwd()
    print(f"Current working folder: {current_working_directory}")

    page.window.width = 800
    page.window.height = 600
    page.window.center()

    # Pasamos la referencia de la página a cada vista
    page.views.append(
        ft.View(
            "/login",
            [LoginPage(page).build()]
        )
    )

    def route_change(e: ft.RouteChangeEvent):
        print(f"Route changed to {e.route}")
        page.views.clear()

        if page.route == '/login':
            page.views.append(
                ft.View(
                    "/login",
                    [LoginPage(page).build()]
                )
            )

        if page.route == '/private':
            page.views.append(
                ft.View(
                    "/private",
                    [PrivatePage(page).build()]
                )
            )

        if page.route == '/register':
            page.views.append(
                ft.View(
                    "/register",
                    [RegisterPage(page).build()]
                )
            )

        page.update()

    page.on_route_change = route_change
    page.update()


ft.app(target=main)

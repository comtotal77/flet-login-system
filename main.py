import json
import os
import flet as ft

from login_page import LoginPage
from private_page import PrivatePage
from register_page import RegisterPage
from cont_page import ContPage

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

        if page.route == '/conteo':
            page.views.append(
                ft.View(
                    "/conteo",
                    [ContPage(page).build()]
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


if __name__ == '__main__':
    modo="e" #por defecto.  si comento la siguiente línea siempre será modo escritorio (e)
    modo = input("¿Desea ejecutar la aplicación en modo web o escritorio? (web(w)/escritorio(e)): ").strip().lower()
    if modo == "w":
        ft.app(target=main,view="web_browser",port=8550)
    else:
        ft.app(target=main)

import flet as ft

class PrivatePage:
    def __init__(self, page):
        self.page = page  # Guardamos la referencia a la página

    def build(self) -> ft.Container:
        msg = ''

        mydt = ft.DataTable (
                columns=[
                    ft.DataColumn(ft.Text("id")),
                    ft.DataColumn(ft.Text("fecha_inic")),
                    ft.DataColumn(ft.Text("almacen")),
                    ft.DataColumn(ft.Text("actions")),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text("1")),
                            ft.DataCell(ft.Text("17/09/2024")),
                            ft.DataCell(ft.Text("12")),
                            ft.DataCell(ft.Row(
                                [
                                    ft.IconButton(ft.icons.PLAY_ARROW,icon_color="red",data=1,on_click=self.segunda),
                                    ft.IconButton("create",icon_color="red",data=1,on_click=self.otraopcion),
                                ])
                            )
                        ],
                    ),
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text("2")),
                            ft.DataCell(ft.Text("16/09/2024")),
                            ft.DataCell(ft.Text("19")),
                            ft.DataCell(ft.Row(
                                [
                                    ft.IconButton(ft.icons.PLAY_ARROW,icon_color="red",data=1,on_click=self.segunda),
                                    ft.IconButton("create",icon_color="red",data=1,on_click=self.otraopcion),
                                ])
                            )
                        ],
                    ),
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text("3")),
                            ft.DataCell(ft.Text("16/09/2024")),
                            ft.DataCell(ft.Text("25")),
                            ft.DataCell(ft.Row(
                                [
                                    ft.IconButton(ft.icons.PLAY_ARROW,icon_color="red",data=1,on_click=self.segunda),
                                    ft.IconButton("create",icon_color="red",data=1,on_click=self.otraopcion),
                                ])
                            )
                        ],
                    ),        
                ]
            )


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
                mydt,
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
        self.page.session.set("idConteo", {"number":"145"})
        self.page.go('/conteo')
        self.page.update()

    def otraopcion(self, e):
        pass
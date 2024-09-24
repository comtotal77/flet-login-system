import flet as ft
from data_base import DataAccess
from base_page import BasePage

class PrivatePage(BasePage):
    def __init__(self, page):
        super().__init__(page)        
        self.page = page  # Guardamos la referencia a la página

    def build(self) -> ft.Container:

        def create_data_table(data):
            columns = [
                ft.DataColumn(ft.Text("id_conteo")),
                ft.DataColumn(ft.Text("fecha_inic")),
                ft.DataColumn(ft.Text("fecha_fin")),
                ft.DataColumn(ft.Text("almacen")),
                ft.DataColumn(ft.Text("status")),
                ft.DataColumn(ft.Text("actions"))
            ]

            rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(row[1])),
                        ft.DataCell(ft.Text(row[2])),
                        ft.DataCell(ft.Text(row[3])),
                        ft.DataCell(ft.Text(row[4])),
                        ft.DataCell(ft.Text(row[5])),
                        ft.DataCell(ft.Row([
                            ft.IconButton(ft.icons.PLAY_ARROW, icon_color="red", data=row[0], on_click=lambda e, r1=row[1], r4=row[4]: self.segunda(e, r1, r4)),
                            ft.IconButton("create", icon_color="red", data=row[0], on_click=self.otraopcion)
                        ]))
                    ]
                )
                for row in data
            ]

            return ft.DataTable(columns=columns, rows=rows)

        if not self.page.session.contains_key("loginme"):
            self.page.go('/login')  # Redirigir al login si no está logueado
        msg = ''

        datalogin = self.page.session.get("loginme")
        if datalogin["value"]:
            sessData= datalogin["datos"]
            name = sessData[3]
            msg = f"Hello {name}"

        searchData= DataAccess()
        searchData.cierraProcesoConteo(0,sessData[0],0)        ##Cierra conteos abiertos del usuario
        tablaConteos=searchData.conteosxUsuario(sessData[0])
        datalogin['tablaconteos'] = tablaConteos
        self.page.session.set("loginme", datalogin)
        mydt= create_data_table(tablaConteos)

        content=ft.Column([
            ft.Text("Sección del usuario", size=30),
            ft.Text(f"{msg}"),
            mydt,
            ft.Row([ft.ElevatedButton("Logout",
                                bgcolor=ft.colors.RED,
                                color=ft.colors.WHITE,
                                on_click=self.logout
                                )
            ])
        ])
        # Llama al layout común con el contenido específico de login
        return self.common_layout(content)    



    def logout(self, e):
        self.page.session.clear()
        self.page.go('/login')
        self.page.update()

    def segunda(self, e, idConteo, almacen):
        self.page.session.set("datosConteo", {"id":idConteo,"almacen":almacen})
        self.page.go('/conteo')
        self.page.update()

    def otraopcion(self, e):
        pass
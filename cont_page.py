import flet as ft
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv(".env")
###Esto es de la segunda rama - commit 1
#aprendizaje: txtSku lo defino en init y después lo llamo en todas ls instancias de la clase con self
#             en cambio los demás (txtNombre,txtCantidad,btnInsertCount,txtResult) los creo en buid pero para poder llamarlos
#             necesito decirle que son global
class ContPage:
    def __init__(self, page):
        self.page = page  # Guardamos la referencia a la página
        self.txtSku=ft.TextField(label="Indica el SKU a buscar")
        self.existencia=0

    def build(self) -> ft.Container:
        if not self.page.session.contains_key("loginme"):
            self.page.go('/login')  # Redirigir al login si no está logueado

        global txtNombre,txtCantidad,btnInsertCount,txtResult,almacen
        msg = ''
        msg2 = ''
        datalogin = self.page.session.get("loginme")
        datalogin2 = self.page.session.get("datosConteo")
        idConteo = datalogin2["id"]
        almacen = datalogin2["almacen"]
        sessData= datalogin["datos"]
        if datalogin["value"]:
            name = sessData[3]
            msg = f"Hello {name} estás en el conteo {idConteo}"
            msg2 = f"Correspondiente al almacen {almacen}"
        #txtSku=ft.TextField(label="Indica el SKU a buscar")
        self.txtSku.on_focus = self.borrarSku
        txtNombre = ft.TextField(label="Nombre", visible=False, read_only=True)
        txtCantidad = ft.TextField(label="Cantidad", visible=False,input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string=""))
        btnInsertCount=ft.ElevatedButton("siguiente",visible=False,on_click=self.addToDB)
        txtResult=ft.Text("No encontrado", visible=False)                
        return ft.Container(
            bgcolor=ft.colors.BLUE_200,
            padding=10,
            content=ft.Column([
                ft.Text(f"{msg}"),
                ft.Text(f"{msg2}"),
                self.txtSku,
                ft.Row([ft.ElevatedButton("buscar",on_click=self.getDataArticle),txtResult]),
                txtNombre,
                txtCantidad,
                btnInsertCount,
                ft.ElevatedButton("Logout",
                                  bgcolor=ft.colors.RED,
                                  color=ft.colors.WHITE,
                                  on_click=self.logout)
            ])
        )


    def borrarSku(self, e):
        self.txtSku.value = ""
        txtResult.visible=False
        self.page.update()


    def getDataArticle(self, e):
        #requests con la información de un artículo según esl sku
        url="http://127.0.0.1:5000/infoArt/SKU123456"
        url = os.getenv("URL_ENDPOINT")
        url += "/getAlmacenByArti/"+str(self.txtSku.value)+'/'+almacen

        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)

        jsonresult=json.loads(response.text)
        #linea para probar rama
        # jsonresult=[
        #                 {
        #                     "sku":"sku1",
        #                     "nombre":"Articulo1",
        #                     "descrip":"Otro articulo más de la tienda",
        #                 },
        #                 {
        #                     "sku":"sku2",
        #                     "nombre":"Articulo2",
        #                     "descrip":"Otro articulo2 más de la tienda",
        #                 }
        #            ]
        for item in jsonresult:
            print(item["codigo"])
            if item["codigo"] == self.txtSku.value:
                txtNombre.value =str(item["nombre"])
                self.existencia =item["existencia"]
                txtNombre.visible = True
                txtResult.visible = True
                txtCantidad.visible=True
                btnInsertCount.visible=True
                break
            else:
                txtNombre.value = "No encontrado"
                txtResult.visible=True
        self.page.update()

    def addToDB(self, e):
        print("presiono")
        cantidad_interna=int(txtCantidad.value)-int(self.existencia)
        print("en la BD se insertara la  diferencia:"+str(cantidad_interna))
        url="http://127.0.0.1:5000/addCont/idproducto/idconteo"

        res=200 #producto procesado

        snack_bar = ft.SnackBar(
            ft.Text("Insertado", size=15),
            bgcolor="green"
        )
        # Añadir snack bar a la página usando overlay
        self.page.overlay.append(snack_bar)
        snack_bar.open = True
        self.existencia=0
        txtResult.visible = False 
        txtNombre.visible = False   
        txtCantidad.visible=False
        btnInsertCount.visible=False
        self.txtSku.value=""
        self.page.update()

    def logout(self, e):
        self.page.session.clear()
        self.page.go('/login')
        self.page.update()

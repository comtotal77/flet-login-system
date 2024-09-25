import flet as ft
import requests
import json
import time
from dotenv import load_dotenv
import os
import random
import string

from data_base import DataAccess
from base_page import BasePage

load_dotenv(".env")
###Esto es de la segunda rama - commit 1
#aprendizaje: txtSku lo defino en init y después lo llamo en todas ls instancias de la clase con self
#             en cambio los demás (txtNombre,txtCantidad,btnInsertCount,txtResult) los creo en buid pero para poder llamarlos
#             necesito decirle que son global
class ContPage(BasePage):
    def __init__(self, page):
        super().__init__(page)        
        self.page = page  # Guardamos la referencia a la página
        self.txtSku=ft.TextField(label="Indica el SKU a buscar")
        self.existencia=0
        self.searchData=DataAccess()
        self.sessionData=0

    def build(self) -> ft.Container:
        if not self.page.session.contains_key("loginme"):
            self.page.go('/login')  # Redirigir al login si no está logueado

        caracteres = string.ascii_letters + string.digits  # Letras mayúsculas, minúsculas y dígitos
        self.sessionData=''.join(random.choices(caracteres, k=20))

        global txtNombre,imgProd,txtCantidad,btnInsertCount,txtResult,almacen,idConteo,idUsuario
        msg = ''
        msg2 = ''
        datalogin = self.page.session.get("loginme")
        datalogin2 = self.page.session.get("datosConteo")
        idConteo = datalogin2["id"]
        almacen = datalogin2["almacen"]
        sessData= datalogin["datos"]
        if datalogin["value"]:
            name = sessData[3]
            idUsuario=sessData[0]
            msg = f"Hello {name} estás en el conteo {idConteo}"
            msg2 = f"Correspondiente al almacen {almacen}"
        #txtSku=ft.TextField(label="Indica el SKU a buscar")
        self.txtSku.on_focus = self.borrarSku
        txtNombre = ft.TextField(label="Nombre", visible=False, read_only=True)
        imgProd = ft.Image(
            src=f"",
            width=100,
            height=100,
            visible=False,
            fit=ft.ImageFit.CONTAIN,
        )
        txtCantidad = ft.TextField(label="Cantidad", visible=False,input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string=""))
        btnInsertCount=ft.ElevatedButton("siguiente",visible=False,on_click=self.addToDB)
        txtResult=ft.Text("No encontrado", visible=False)                
  
        content=ft.Column([
            ft.Text(f"{msg}"),
            ft.Text(f"{msg2}"),
            self.txtSku,
            ft.Row([ft.ElevatedButton("buscar",on_click=self.getDataArticle),txtResult]),
            txtNombre,
            imgProd,
            txtCantidad,
            btnInsertCount,
            ft.ElevatedButton("Cerrar sesion de conteo",
                                bgcolor=ft.colors.RED,
                                color=ft.colors.WHITE,
                                on_click=self.logoutCount)
        ])

        # Llama al layout común con el contenido específico de login
        return self.common_layout(content)    


    def borrarSku(self, e):
        self.txtSku.value = ""
        txtResult.visible=False
        self.page.update()


    def getDataArticle(self, e):

        def verifica_url(url):
            try:
                payload = {}
                headers = {}
                response = requests.request("GET", url, headers=headers, data=payload)
                if response.status_code == 200:
                    return True
                else:
                    return False
            except requests.exceptions.RequestException as e:
                print(f"Error al verificar la URL: {e}")
                return False


        #requests con la información de un artículo según esl sku
        url="http://127.0.0.1:5000/infoArt/SKU123456"
        url = os.getenv("URL_ENDPOINT")
        url += "/getAlmacenByArti/"+str(self.txtSku.value)+'/'+almacen

        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)

        jsonresult=json.loads(response.text)

        ##buscar si el código ya está contado select el codigo si ya está en idconteo y su estatus es 1

        ##de ser así debe indicarlo en txtResult 
        if jsonresult !=[]:

            ##buscar si el código ya está contado select el codigo si ya está en idconteo y su estatus es 1
            #if self.txtSku.value==1:
            item=jsonresult[0]
            print(item["codigo"])

            if self.searchData.articuloContado(idConteo,self.txtSku.value):
                self.txtResultMsg(self,mensaje="Este artículo ya fue contado")

            ##OJOOO si no hay más articulos que contar
            elif item["codigo"].strip() == self.txtSku.value.strip():
                txtNombre.value =str(item["nombre"])
                urlImages = os.getenv("URL_IMAGES")
                foto=str(item["rutafoto"]).strip()
                indice = foto.rfind("\\")  # Encuentra la última aparición de \
                nombre_archivo = foto[indice + 1:]  # Extrae todo después del último backslash
                print(urlImages+nombre_archivo)
                url=urlImages+nombre_archivo

                # payload = {}
                # headers = {}
                # response = requests.request("GET", url, headers=headers, data=payload)
                imgProd.src=urlImages+nombre_archivo

                self.existencia =item["existencia"]
                txtNombre.visible = True
                imgProd.visible = True
                txtResult.visible = True
                txtCantidad.visible=True
                btnInsertCount.visible=True
                self.page.update()
        else:
            self.txtResultMsg(self,mensaje="No Encontrado")

    def txtResultMsg(self,e,mensaje):
        txtResult.value = mensaje
        txtResult.visible=True
        self.page.update()
        time.sleep(5)
        self.txtSku.focus()
        self.page.update()

    def addToDB(self, e):
        print("presiono")
        cantidad_interna=int(txtCantidad.value)-int(self.existencia)
        print("en la BD se insertara la  diferencia:"+str(cantidad_interna))
        url="http://127.0.0.1:5000/addCont/idproducto/idconteo"

        self.searchData.insertaArticuloCont(idConteo,self.txtSku.value,txtCantidad.value,cantidad_interna,self.sessionData)
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
        imgProd.visible = False 
        txtCantidad.visible=False
        txtCantidad.value=0
        btnInsertCount.visible=False
        self.txtSku.value=""
        self.page.update()

    def logoutCount(self, e):
        #self.page.session.clear()
        #eliminar datos de la sesión
        #productos contados en la sesion van a 1
        self.searchData.cierraProcesoConteo(idConteo,idUsuario,self.sessionData)
        self.page.go('/private')
        self.page.update()

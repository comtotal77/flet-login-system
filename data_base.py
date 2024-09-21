import flet as ft
import json
import sqlite3

class DataAccess:
    def __init__(self):
        # Conectar a la base de datos (se crea si no existe)
        self.dbStr='conteo_inventario.db'
        self.conn = sqlite3.connect(self.dbStr, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.conn_abierta = True

    def verifyConex(self):
        if not self.conn_abierta:
            self.conn = sqlite3.connect(self.dbStr, check_same_thread=False)
            self.cursor = self.conn.cursor()            

    def buscaLogin(self,email,password):
        # Consulta para verificar la coincidencia
        # conn = sqlite3.connect(self.dbStr)
        # cursor = conn.cursor()

        self.verifyConex()


        self.cursor.execute('''SELECT * FROM usuario WHERE email = ? AND pass = ?''', (email, password))
        
        # Obtener el resultado de la consulta
        usuario = self.cursor.fetchone()
        self.conn_abierta=not self.conn_abierta
        
        # Cerrar la conexión
        self.conn.close()
        
        # Verificar si el usuario fue encontrado
        if usuario:
            print("Usuario encontrado:", usuario)
            return usuario
            return True
        else:
            print("No se encontró el usuario con los credenciales proporcionados.")
            return False
        
    def conteosxUsuario(self,idUsuario):
        # Consulta para verificar la coincidencia
        
        self.verifyConex()
        self.cursor.execute(f'''SELECT * FROM conteos WHERE dni_usuario = {idUsuario}''')
        
        # Obtener el resultado de la consulta
        usuario = self.cursor.fetchall()
        
        # Cerrar la conexión
        self.conn.close()
        
        self.conn_abierta=not self.conn_abierta
        
        # Verificar si el usuario fue encontrado
        if usuario:
            return usuario
        else:
            print("No se encontraron conteos para este usuario")
            return False
        
    def articuloContado(self,idConteo,sku):
        # Consulta para verificar la coincidencia

        self.verifyConex()
        self.cursor.execute(f'''SELECT * FROM conteo_proceso WHERE sku='{sku}' and status=1''')
        
        # Obtener el resultado de la consulta
        usuario = self.cursor.fetchone()
        
        # Cerrar la conexión
        self.conn.close()
        self.conn_abierta=not self.conn_abierta
        
        # Verificar si el usuario fue encontrado
        if usuario:
            return True
        else:
            print("No se encontraron conteos para este usuario")
            return False
    
    def insertaArticuloCont(self,idConteo,sku,contado,diferencia,sesion):
        # Insertar un nuevo usuario
        
        self.verifyConex()

        import datetime

        ahora = datetime.datetime.now()
        fecha_formateada = ahora.strftime("%Y-%m-%d %H:%M:%S")
        fecha_hora=fecha_formateada

        self.cursor.execute('''
            INSERT INTO conteo_proceso (id_Conteo, SKU, contado, diferencia,fecha_hora,status,sesion)
            VALUES (?, ?, ?, ?, ?, ?, ?)''', (idConteo, sku, contado, diferencia,fecha_hora,0,sesion))
        self.conn.commit()
        self.conn.close()
        self.conn_abierta=False

    def cierraProcesoConteo(self,idConteo,idUsuario,sesion):
        
        self.verifyConex()
        
        
        if idConteo==0 and sesion==0:
            sqlSentence=f'''UPDATE conteo_proceso set status=1 where dni_usuario={idUsuario}'''
            sqlSentence = f"""
            UPDATE conteo_proceso p
            INNER JOIN cnteos c ON p.id_conteo = c.id_conteo
            SET p.status = 1
            WHERE c.dni_usuario = {idUsuario}
            """
            sqlSentence=f'''
            UPDATE conteo_proceso
            SET status = 1
            WHERE id_conteo IN (
                SELECT id_conteo
                FROM conteos
                WHERE dni_usuario = {idUsuario}
            );
            '''
        else:
            sqlSentence=f'''UPDATE conteo_proceso set status=1 WHERE sesion="{sesion}"'''
        self.cursor.execute(sqlSentence)
        self.conn.commit()
        self.conn.close()
        self.conn_abierta=False
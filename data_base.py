import flet as ft
import json
import sqlite3

class DataAccess:
    def __init__(self):
        # Conectar a la base de datos (se crea si no existe)
        self.dbStr='conteo_inventario.db'
        pass

    def buscaLogin(self,email,password):
        # Consulta para verificar la coincidencia
        conn = sqlite3.connect(self.dbStr)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM usuario WHERE email = ? AND pass = ?''', (email, password))
        
        # Obtener el resultado de la consulta
        usuario = cursor.fetchone()
        
        # Cerrar la conexión
        conn.close()
        
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
        conn = sqlite3.connect(self.dbStr)
        cursor = conn.cursor()
        cursor.execute(f'''SELECT * FROM conteos WHERE dni_usuario = {idUsuario}''')
        
        # Obtener el resultado de la consulta
        usuario = cursor.fetchall()
        
        # Cerrar la conexión
        conn.close()
        
        # Verificar si el usuario fue encontrado
        if usuario:
            return usuario
        else:
            print("No se encontraron conteos para este usuario")
            return False
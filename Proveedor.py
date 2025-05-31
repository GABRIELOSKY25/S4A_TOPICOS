# Gabriel Flores Urbina
# https://github.com/GABRIELOSKY25/S4A_TOPICOS

import wx
import mysql.connector
import wx.grid
from mysql.connector import Error

# Conexión a la base de datos
try:
    conexion = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        password="peresoso888", 
        database="COSTCO"
    )

    if conexion.is_connected():
        print("Conexión exitosa a MySQL/MariaDB")
        cursor = conexion.cursor()
except Error as ex:
    print("Error al conectar:", ex)

def Proveedor(parent_frame=None):
    ventana = wx.Frame(None, title='Proveedor', size=(500, 450))  
    panel = wx.Panel(ventana)
    ventana.parent_frame = parent_frame  

    # Título
    titulo = wx.StaticText(panel, label = "Proveedor", pos = (180, 30))
    titulo.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD))

    # Campos
    wx.StaticText(panel, label="idProveedor:", pos=(60, 80)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_idProveedor = wx.TextCtrl(panel, pos=(140, 76), size=(200, -1))
    txt_idProveedor.SetBackgroundColour(wx.Colour(254, 241, 147))

    wx.StaticText(panel, label="Nombre:", pos=(60, 120)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Nombre = wx.TextCtrl(panel, pos=(140, 116), size=(200, -1))
    txt_Nombre.SetBackgroundColour(wx.Colour(181, 242, 248))

    wx.StaticText(panel, label="Apellidos:", pos=(60, 160)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Apellidos = wx.TextCtrl(panel, pos=(140, 156), size=(200, -1))
    txt_Apellidos.SetBackgroundColour(wx.Colour(210, 255, 254))

    wx.StaticText(panel, label="Telefono:", pos=(60, 200)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Telefono = wx.TextCtrl(panel, pos=(140, 196), size=(200, -1))
    txt_Telefono.SetBackgroundColour(wx.Colour(210, 255, 254))

    wx.StaticText(panel, label="Direccion:", pos=(60, 240)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Direccion = wx.TextCtrl(panel, pos=(140, 236), size=(200, -1))
    txt_Direccion.SetBackgroundColour(wx.Colour(181, 242, 248))

    # Funciones para botones
    def insertar_proveedor(event):
        try:
            query = "INSERT INTO proveedor (idProveedor, Nombre, Apellidos, Telefono, Direccion) VALUES (%s, %s, %s, %s, %s)"
            valores = (
                txt_idProveedor.GetValue(),
                txt_Nombre.GetValue(),
                txt_Apellidos.GetValue(),
                txt_Telefono.GetValue(),
                txt_Direccion.GetValue()
            )
            cursor.execute(query, valores)
            conexion.commit()
            wx.MessageBox("Proveedor insertado correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al insertar proveedor: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def actualizar_proveedor(event):
        try:
            query = "UPDATE proveedor SET Nombre=%s, Apellidos=%s, Telefono=%s, Direccion=%s WHERE idProveedor=%s"
            valores = (
                txt_Nombre.GetValue(),
                txt_Apellidos.GetValue(),
                txt_Telefono.GetValue(),
                txt_Direccion.GetValue(),
                txt_idProveedor.GetValue()
            )
            cursor.execute(query, valores)
            conexion.commit()
            wx.MessageBox("Proveedor actualizado correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al actualizar proveedor: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def eliminar_proveedor(event):
        try:
            query = "DELETE FROM proveedor WHERE idProveedor=%s"
            valores = (txt_idProveedor.GetValue(),)
            cursor.execute(query, valores)
            conexion.commit()
            wx.MessageBox("Proveedor eliminado correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al eliminar proveedor: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def leer_proveedor(event):
        try:
            query = "SELECT * FROM proveedor"
            cursor.execute(query)
            resultados = cursor.fetchall()

            if resultados:
         
                num_registros = len(resultados)
                altura_tabla = min(400, 600 + num_registros * 25)  
                
                
                ventana_emergente = wx.Frame(None, title="Listado de Proveedores", 
                                        size=(800, altura_tabla + 100))  
                panel = wx.Panel(ventana_emergente)
                
                
                titulo = wx.StaticText(panel, label="Listado de Proveedores", pos=(250, 15))
                titulo.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))

                list_ctrl = wx.ListCtrl(panel, pos=(20, 50), size=(750, altura_tabla),
                                    style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
                
                columnas = [
                    ("ID", 80),
                    ("Nombre", 150),
                    ("Apellidos", 150),
                    ("Teléfono", 150),
                    ("Dirección", 220)
                ]
                
                for i, (col_name, col_width) in enumerate(columnas):
                    list_ctrl.InsertColumn(i, col_name, width=col_width)

                for proveedor in resultados:
                    index = list_ctrl.InsertItem(list_ctrl.GetItemCount(), str(proveedor[0]))

                    for col in range(1, 5): 
                        list_ctrl.SetItem(index, col, str(proveedor[col]))

                    list_ctrl.SetItemBackgroundColour(index, wx.WHITE)
                
                list_ctrl.SetBackgroundColour(wx.WHITE)
                list_ctrl.SetForegroundColour(wx.BLACK)
                
                ventana_emergente.Show()
            else:
                wx.MessageBox("No hay proveedores registrados", "Información", wx.OK | wx.ICON_INFORMATION)

        except Error as e:
            wx.MessageBox(f"Error al consultar proveedores: {e}", "Error", wx.OK | wx.ICON_ERROR)
    
    def regresar_menu(event):
        """Regresa al menú principal"""
        if ventana.parent_frame:
            ventana.parent_frame.Show() 
        ventana.Destroy() 

    def on_close(event):
        """Maneja el evento cuando se cierra la ventana"""
        if ventana.parent_frame:
            ventana.parent_frame.Show() 
        ventana.Destroy()

    # Botones CRUD
    wx.Button(panel, label="Guardar", pos=(30, 300), size=(100, 30)).Bind(wx.EVT_BUTTON, insertar_proveedor)
    wx.Button(panel, label="Actualizar", pos=(140, 300), size=(100, 30)).Bind(wx.EVT_BUTTON, actualizar_proveedor)
    wx.Button(panel, label="Eliminar", pos=(250, 300), size=(100, 30)).Bind(wx.EVT_BUTTON, eliminar_proveedor)
    wx.Button(panel, label="Leer", pos=(360, 300), size=(100, 30)).Bind(wx.EVT_BUTTON, leer_proveedor)
    
    # Botón para regresar al menú
    wx.Button(panel, label="Regresar al menú", pos=(180, 350), size=(150, 30)).Bind(wx.EVT_BUTTON, regresar_menu)

    # Manejar el evento de cerrar ventana
    ventana.Bind(wx.EVT_CLOSE, on_close)

    ventana.Show()

if __name__ == "__main__":
    Ventana = wx.App()
    Proveedor()
    Ventana.MainLoop()
# Gabriel Flores Urbina
# https://github.com/GABRIELOSKY25/S4A_TOPICOS

import wx
import mysql.connector
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

def Categoria(parent_frame=None):
    ventana = wx.Frame(None, title='Categoría', size=(500, 340))  
    panel = wx.Panel(ventana)
    ventana.parent_frame = parent_frame  

    # Título
    titulo = wx.StaticText(panel, label="Categorías", pos=(187, 30))
    titulo.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD))

    # Campos
    wx.StaticText(panel, label="idCategoria:", pos=(60, 80)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_idCategoria = wx.TextCtrl(panel, pos=(140, 76), size=(200, -1))
    txt_idCategoria.SetBackgroundColour(wx.Colour(254, 241, 147))

    wx.StaticText(panel, label="Nombre:", pos=(60, 120)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Nombre = wx.TextCtrl(panel, pos=(140, 116), size=(200, -1))
    txt_Nombre.SetBackgroundColour(wx.Colour(181, 242, 248))

    # Funciones CRUD
    def insertar_categoria(event):
        try:
            query = "INSERT INTO categoria (idCategoria, Nombre) VALUES (%s, %s)"
            valores = (
                txt_idCategoria.GetValue(),
                txt_Nombre.GetValue()
            )
            cursor.execute(query, valores)
            conexion.commit()
            wx.MessageBox("Categoría insertada correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al insertar categoría: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def actualizar_categoria(event):
        try:
            query = "UPDATE categoria SET Nombre=%s WHERE idCategoria=%s"
            valores = (
                txt_Nombre.GetValue(),
                txt_idCategoria.GetValue()
            )
            cursor.execute(query, valores)
            conexion.commit()
            wx.MessageBox("Categoría actualizada correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al actualizar categoría: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def eliminar_categoria(event):
        try:
            query = "DELETE FROM categoria WHERE idCategoria=%s"
            valores = (txt_idCategoria.GetValue(),)
            cursor.execute(query, valores)
            conexion.commit()
            wx.MessageBox("Categoría eliminada correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al eliminar categoría: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def leer_categoria(event):
        try:
            query = "SELECT * FROM categoria"
            cursor.execute(query)
            resultados = cursor.fetchall()

            if resultados:
                ventana_emergente = wx.Frame(None, title="Listado de Categorías", size=(600, 500))
                panel = wx.Panel(ventana_emergente)
                
                titulo = wx.StaticText(panel, label="Listado de Categorías", pos=(200, 15))
                titulo.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))

                list_ctrl = wx.ListCtrl(panel, pos=(20, 50), size=(550, 400), style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
                
                list_ctrl.InsertColumn(0, "ID Categoría", width=150)
                list_ctrl.InsertColumn(1, "Nombre", width=380)
                
                for categoria in resultados:
                    index = list_ctrl.InsertItem(list_ctrl.GetItemCount(), str(categoria[0]))
                    list_ctrl.SetItem(index, 1, str(categoria[1]))
                    

                    if index % 2 == 0:
                        list_ctrl.SetItemBackgroundColour(index, wx.Colour(240, 240, 240))
                    else:
                        list_ctrl.SetItemBackgroundColour(index, wx.WHITE)
                
                ventana_emergente.Show()
            else:
                wx.MessageBox("No hay categorías registradas", "Información", wx.OK | wx.ICON_INFORMATION)
                
        except Error as e:
            wx.MessageBox(f"Error al consultar categorías: {e}", "Error", wx.OK | wx.ICON_ERROR)

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
    wx.Button(panel, label="Guardar", pos=(30, 180), size=(100, 30)).Bind(wx.EVT_BUTTON, insertar_categoria)
    wx.Button(panel, label="Actualizar", pos=(140, 180), size=(100, 30)).Bind(wx.EVT_BUTTON, actualizar_categoria)
    wx.Button(panel, label="Eliminar", pos=(250, 180), size=(100, 30)).Bind(wx.EVT_BUTTON, eliminar_categoria)
    wx.Button(panel, label="Leer", pos=(360, 180), size=(100, 30)).Bind(wx.EVT_BUTTON, leer_categoria)

    # Botón para regresar al menú
    wx.Button(panel, label="Regresar al menú", pos=(180, 230), size=(150, 30)).Bind(wx.EVT_BUTTON, regresar_menu)

    # Manejar el evento de cerrar ventana
    ventana.Bind(wx.EVT_CLOSE, on_close)

    ventana.Show()

if __name__ == "__main__":
    Ventana = wx.App()
    Categoria()
    Ventana.MainLoop()
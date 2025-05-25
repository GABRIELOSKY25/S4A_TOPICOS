# Gabriel Flores Urbina

#https://github.com/GABRIELOSKY25/S4A_TOPICOS

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

def Categoria():
    ventana = wx.Frame(None, title='Categoría', size=(500, 290))
    panel = wx.Panel(ventana)

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
                ventana_emergente = wx.Frame(None, title="Listado de Categorías", size=(500, 400))
                panel = wx.Panel(ventana_emergente)

                wx.StaticText(panel, label="Listado de Categorías", pos=(150, 15)).SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))

                # Encabezados
                headers = ["ID Categoría", "Nombre"]
                for i, header in enumerate(headers):
                    wx.StaticText(panel, label=header, pos=(50 + i * 200, 50)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))

                # Mostrar cada categoría
                for row_index, categoria in enumerate(resultados):
                    y = 70 + row_index * 30  # Espaciado entre filas
                    for col_index, valor in enumerate(categoria):
                        wx.StaticText(panel, label=str(valor), pos=(50 + col_index * 200, y))

                ventana_emergente.Show()
            else:
                wx.MessageBox("No hay categorías registradas", "Información", wx.OK | wx.ICON_INFORMATION)

        except Error as e:
            wx.MessageBox(f"Error al consultar categorías: {e}", "Error", wx.OK | wx.ICON_ERROR)

    # Botones
    wx.Button(panel, label="Guardar", pos=(30, 180), size=(100, 30)).Bind(wx.EVT_BUTTON, insertar_categoria)
    wx.Button(panel, label="Actualizar", pos=(140, 180), size=(100, 30)).Bind(wx.EVT_BUTTON, actualizar_categoria)
    wx.Button(panel, label="Eliminar", pos=(250, 180), size=(100, 30)).Bind(wx.EVT_BUTTON, eliminar_categoria)
    wx.Button(panel, label="Leer", pos=(360, 180), size=(100, 30)).Bind(wx.EVT_BUTTON, leer_categoria)

    ventana.Show()

if __name__ == "__main__":
    Ventana = wx.App()
    Categoria()
    Ventana.MainLoop()

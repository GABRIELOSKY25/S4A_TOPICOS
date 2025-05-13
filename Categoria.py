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

Menu = wx.App()

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
            query = "SELECT * FROM categoria WHERE idCategoria=%s"
            cursor.execute(query, (txt_idCategoria.GetValue(),))
            resultado = cursor.fetchone()
            if resultado:
                txt_Nombre.SetValue(resultado[1])
            else:
                wx.MessageBox("Categoría no encontrada", "Info", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al leer categoría: {e}", "Error", wx.OK | wx.ICON_ERROR)

    # Botones
    wx.Button(panel, label="Guardar", pos=(30, 180), size=(100, 30)).Bind(wx.EVT_BUTTON, insertar_categoria)
    wx.Button(panel, label="Actualizar", pos=(140, 180), size=(100, 30)).Bind(wx.EVT_BUTTON, actualizar_categoria)
    wx.Button(panel, label="Eliminar", pos=(250, 180), size=(100, 30)).Bind(wx.EVT_BUTTON, eliminar_categoria)
    wx.Button(panel, label="Leer", pos=(360, 180), size=(100, 30)).Bind(wx.EVT_BUTTON, leer_categoria)

    ventana.Show()

Categoria()
Menu.MainLoop()



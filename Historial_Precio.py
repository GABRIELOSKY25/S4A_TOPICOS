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

def Historial_Precio():
    ventana = wx.Frame(None, title='Historial Precio', size=(500, 370))
    panel = wx.Panel(ventana)

    # Título
    titulo = wx.StaticText(panel, label="Historial Precios", pos=(159, 30))
    titulo.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD))

    # Campos
    wx.StaticText(panel, label="idHistorial Precio:", pos=(30, 80)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_idHistorial_Precio = wx.TextCtrl(panel, pos=(140, 76), size=(200, -1))
    txt_idHistorial_Precio.SetBackgroundColour(wx.Colour(254, 241, 147))

    wx.StaticText(panel, label="Precio Anterior:", pos=(30, 120)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Precio_Anterior = wx.TextCtrl(panel, pos=(140, 116), size=(200, -1))
    txt_Precio_Anterior.SetBackgroundColour(wx.Colour(181, 242, 248))

    wx.StaticText(panel, label="Precio Nuevo:", pos=(30, 160)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Precio_Nuevo = wx.TextCtrl(panel, pos=(140, 156), size=(200, -1))
    txt_Precio_Nuevo.SetBackgroundColour(wx.Colour(181, 242, 248))

    wx.StaticText(panel, label="Fecha Cambio:", pos=(30, 200)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Fecha_Cambio = wx.TextCtrl(panel, pos=(140, 196), size=(200, -1))
    txt_Fecha_Cambio.SetBackgroundColour(wx.Colour(210, 255, 254))

    # Funciones de botones
    def insertar_historial(event):
        try:
            query = "INSERT INTO historial_precio (idHistorial_Precio, Precio_Anterior, Precio_Nuevo, Fecha_Cambio) VALUES (%s, %s, %s, %s)"
            valores = (
                txt_idHistorial_Precio.GetValue(),
                txt_Precio_Anterior.GetValue(),
                txt_Precio_Nuevo.GetValue(),
                txt_Fecha_Cambio.GetValue()
            )
            cursor.execute(query, valores)
            conexion.commit()
            wx.MessageBox("Historial insertado correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al insertar historial: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def actualizar_historial(event):
        try:
            query = "UPDATE historial_precio SET Precio_Anterior=%s, Precio_Nuevo=%s, Fecha_Cambio=%s WHERE idHistorial_Precio=%s"
            valores = (
                txt_Precio_Anterior.GetValue(),
                txt_Precio_Nuevo.GetValue(),
                txt_Fecha_Cambio.GetValue(),
                txt_idHistorial_Precio.GetValue()
            )
            cursor.execute(query, valores)
            conexion.commit()
            wx.MessageBox("Historial actualizado correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al actualizar historial: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def eliminar_historial(event):
        try:
            query = "DELETE FROM historial_precio WHERE idHistorial_Precio=%s"
            valores = (txt_idHistorial_Precio.GetValue(),)
            cursor.execute(query, valores)
            conexion.commit()
            wx.MessageBox("Historial eliminado correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al eliminar historial: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def leer_historial(event):
        try:
            query = "SELECT * FROM historial_precio WHERE idHistorial_Precio=%s"
            cursor.execute(query, (txt_idHistorial_Precio.GetValue(),))
            resultado = cursor.fetchone()
            if resultado:
                txt_Precio_Anterior.SetValue(str(resultado[1]))
                txt_Precio_Nuevo.SetValue(str(resultado[2]))
                txt_Fecha_Cambio.SetValue(str(resultado[3]))
            else:
                wx.MessageBox("Historial no encontrado", "Info", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al leer historial: {e}", "Error", wx.OK | wx.ICON_ERROR)

    # Botones
    wx.Button(panel, label="Guardar", pos=(30, 260), size=(100, 30)).Bind(wx.EVT_BUTTON, insertar_historial)
    wx.Button(panel, label="Actualizar", pos=(140, 260), size=(100, 30)).Bind(wx.EVT_BUTTON, actualizar_historial)
    wx.Button(panel, label="Eliminar", pos=(250, 260), size=(100, 30)).Bind(wx.EVT_BUTTON, eliminar_historial)
    wx.Button(panel, label="Leer", pos=(360, 260), size=(100, 30)).Bind(wx.EVT_BUTTON, leer_historial)

    ventana.Show()

Historial_Precio()
Menu.MainLoop()

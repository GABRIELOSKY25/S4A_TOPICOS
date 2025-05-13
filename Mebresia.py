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
except Error as ex:
    print("Error al conectar:", ex)

Menu = wx.App()

def Membresia():
    ventana = wx.Frame(None, title='Membresía', size=(500, 370))
    panel = wx.Panel(ventana)

    # Título
    titulo = wx.StaticText(panel, label="Membresías", pos=(180, 30))
    titulo.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD))

    # Campos
    idCodigo = wx.StaticText(panel, label="idCodigo: ", pos=(30, 80))
    txt_idCodigo = wx.TextCtrl(panel, pos=(140, 76), size=(200, -1))
    txt_idCodigo.SetBackgroundColour(wx.Colour(254, 241, 147))
    idCodigo.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))

    Fecha_Activacion = wx.StaticText(panel, label="Fecha Activacion: ", pos=(30, 120))
    txt_Fecha_Activacion = wx.TextCtrl(panel, pos=(140, 116), size=(200, -1))
    txt_Fecha_Activacion.SetBackgroundColour(wx.Colour(181, 242, 248))
    Fecha_Activacion.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))

    Fecha_Vigencia = wx.StaticText(panel, label="Fecha Vigencia: ", pos=(30, 160))
    txt_Fecha_Vigencia = wx.TextCtrl(panel, pos=(140, 156), size=(200, -1))
    txt_Fecha_Vigencia.SetBackgroundColour(wx.Colour(181, 242, 248))
    Fecha_Vigencia.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))

    Tipo = wx.StaticText(panel, label="Tipo: ", pos=(30, 200))
    opciones = ["Ejecutiva", "Dorada"]
    txt_Tipo = wx.ComboBox(panel, pos=(140, 196), size=(200, -1), choices=opciones, style=wx.CB_DROPDOWN)
    txt_Tipo.SetBackgroundColour(wx.Colour(181, 242, 248))
    Tipo.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))

    # Funciones
    def guardar_membresia(event):
        try:
            cursor = conexion.cursor()
            sql = "INSERT INTO membresia (idCodigo, Fecha_Activacion, Fecha_Vigencia, Tipo) VALUES (%s, %s, %s, %s)"
            datos = (
                txt_idCodigo.GetValue(),
                txt_Fecha_Activacion.GetValue(),
                txt_Fecha_Vigencia.GetValue(),
                txt_Tipo.GetValue()
            )
            cursor.execute(sql, datos)
            conexion.commit()
            wx.MessageBox("Membresía guardada correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Error as ex:
            wx.MessageBox(f"Error al guardar membresía: {ex}", "Error", wx.OK | wx.ICON_ERROR)

    def actualizar_membresia(event):
        try:
            cursor = conexion.cursor()
            sql = "UPDATE membresia SET Fecha_Activacion=%s, Fecha_Vigencia=%s, Tipo=%s WHERE idCodigo=%s"
            datos = (
                txt_Fecha_Activacion.GetValue(),
                txt_Fecha_Vigencia.GetValue(),
                txt_Tipo.GetValue(),
                txt_idCodigo.GetValue()
            )
            cursor.execute(sql, datos)
            conexion.commit()
            wx.MessageBox("Membresía actualizada correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Error as ex:
            wx.MessageBox(f"Error al actualizar membresía: {ex}", "Error", wx.OK | wx.ICON_ERROR)

    def eliminar_membresia(event):
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM membresia WHERE idCodigo=%s"
            cursor.execute(sql, (txt_idCodigo.GetValue(),))
            conexion.commit()
            wx.MessageBox("Membresía eliminada correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
            # Limpiar campos
            txt_idCodigo.SetValue("")
            txt_Fecha_Activacion.SetValue("")
            txt_Fecha_Vigencia.SetValue("")
            txt_Tipo.SetValue("")
        except Error as ex:
            wx.MessageBox(f"Error al eliminar membresía: {ex}", "Error", wx.OK | wx.ICON_ERROR)

    def leer_membresia(event):
        try:
            cursor = conexion.cursor()
            sql = "SELECT * FROM membresia WHERE idCodigo=%s"
            cursor.execute(sql, (txt_idCodigo.GetValue(),))
            resultado = cursor.fetchone()
            if resultado:
                txt_Fecha_Activacion.SetValue(str(resultado[1]))
                txt_Fecha_Vigencia.SetValue(str(resultado[2]))
                txt_Tipo.SetValue(str(resultado[3]))
            else:
                wx.MessageBox("Membresía no encontrada", "Atención", wx.OK | wx.ICON_WARNING)
        except Error as ex:
            wx.MessageBox(f"Error al leer membresía: {ex}", "Error", wx.OK | wx.ICON_ERROR)

    # Botones
    boton_Guardar = wx.Button(panel, label="Guardar", pos=(30, 260), size=(100, 30))
    boton_Actualizar = wx.Button(panel, label="Actualizar", pos=(140, 260), size=(100, 30))
    boton_Eliminar = wx.Button(panel, label="Eliminar", pos=(250, 260), size=(100, 30))
    boton_Leer = wx.Button(panel, label="Leer", pos=(360, 260), size=(100, 30))

    # Eventos
    boton_Guardar.Bind(wx.EVT_BUTTON, guardar_membresia)
    boton_Actualizar.Bind(wx.EVT_BUTTON, actualizar_membresia)
    boton_Eliminar.Bind(wx.EVT_BUTTON, eliminar_membresia)
    boton_Leer.Bind(wx.EVT_BUTTON, leer_membresia)

    ventana.Show()

Membresia()
Menu.MainLoop()

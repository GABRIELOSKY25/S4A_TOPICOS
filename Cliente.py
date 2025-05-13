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

def Cliente():
    ventana = wx.Frame(None, title='Cliente', size=(500, 550))
    panel = wx.Panel(ventana)

    wx.StaticText(panel, label="Clientes", pos=(195, 30)).SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD))

    labels = [
        ("idCliente", 80), ("idCodigo", 120), ("Nombre", 160), ("Apellidos", 200),
        ("Edad", 240), ("Correo", 280), ("Telefono", 320), ("Direccion", 360)
    ]
    
    campos = {}
    for nombre, y in labels:
        wx.StaticText(panel, label=f"{nombre}: ", pos=(60, y)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        txt = wx.TextCtrl(panel, pos=(140, y - 4), size=(200, -1))
        txt.SetBackgroundColour(wx.Colour(210, 255, 254))
        campos[nombre] = txt

    def guardar_cliente(event):
        try:
            cursor = conexion.cursor()
            consulta = """
                INSERT INTO cliente (idCliente, idCodigo, Nombre, Apellidos, Edad, Correo, Telefono, Direccion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            valores = tuple(campos[k].GetValue() for k in labels_dict)
            cursor.execute(consulta, valores)
            conexion.commit()
            wx.MessageBox("Cliente guardado exitosamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al insertar cliente: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def leer_cliente(event):
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM cliente WHERE idCliente = %s", (campos["idCliente"].GetValue(),))
            cliente = cursor.fetchone()
            if cliente:
                for i, k in enumerate(labels_dict):
                    campos[k].SetValue(str(cliente[i]))
            else:
                wx.MessageBox("Cliente no encontrado", "Atención", wx.OK | wx.ICON_WARNING)
        except Error as e:
            wx.MessageBox(f"Error al leer cliente: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def actualizar_cliente(event):
        try:
            cursor = conexion.cursor()
            consulta = """
                UPDATE cliente SET idCodigo=%s, Nombre=%s, Apellidos=%s, Edad=%s, Correo=%s, Telefono=%s, Direccion=%s
                WHERE idCliente = %s
            """
            valores = tuple(campos[k].GetValue() for k in list(labels_dict)[1:]) + (campos["idCliente"].GetValue(),)
            cursor.execute(consulta, valores)
            conexion.commit()
            wx.MessageBox("Cliente actualizado exitosamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al actualizar cliente: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def eliminar_cliente(event):
        try:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM cliente WHERE idCliente = %s", (campos["idCliente"].GetValue(),))
            conexion.commit()
            for txt in campos.values():
                txt.SetValue("")
            wx.MessageBox("Cliente eliminado", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al eliminar cliente: {e}", "Error", wx.OK | wx.ICON_ERROR)

    labels_dict = {k: v for k, v in labels}

    wx.Button(panel, label="Guardar", pos=(30, 420)).Bind(wx.EVT_BUTTON, guardar_cliente)
    wx.Button(panel, label="Actualizar", pos=(140, 420)).Bind(wx.EVT_BUTTON, actualizar_cliente)
    wx.Button(panel, label="Eliminar", pos=(250, 420)).Bind(wx.EVT_BUTTON, eliminar_cliente)
    wx.Button(panel, label="Leer", pos=(360, 420)).Bind(wx.EVT_BUTTON, leer_cliente)

    ventana.Show()

Cliente()
Menu.MainLoop()

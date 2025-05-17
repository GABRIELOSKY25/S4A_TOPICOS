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

App = wx.App()

def Cliente():
    ventana = wx.Frame(None, title='Clientes', size=(500, 450))
    panel = wx.Panel(ventana)

    # Título
    titulo = wx.StaticText(panel, label="Clientes", pos=(180, 30))
    titulo.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD))

    # Campos
    ventana = wx.Frame(None, title='Cliente', size=(500, 550))
    panel = wx.Panel(ventana)

    # Título
    titulo = wx.StaticText(panel, label="Clientes", pos=(195, 30))
    titulo.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD))

    # Campos
    wx.StaticText(panel, label="idCliente:", pos=(60, 80)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_idCliente = wx.TextCtrl(panel, pos=(140, 76), size=(200, -1))
    txt_idCliente.SetBackgroundColour(wx.Colour(254, 241, 147))

    wx.StaticText(panel, label="idCodigo:", pos=(60, 120)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_idCodigo = wx.TextCtrl(panel, pos=(140, 116), size=(200, -1))
    txt_idCodigo.SetBackgroundColour(wx.Colour(254, 241, 147))

    wx.StaticText(panel, label="Nombre:", pos=(60, 160)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Nombre = wx.TextCtrl(panel, pos=(140, 156), size=(200, -1))
    txt_Nombre.SetBackgroundColour(wx.Colour(181, 242, 248))

    wx.StaticText(panel, label="Apellidos:", pos=(60, 200)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Apellidos = wx.TextCtrl(panel, pos=(140, 196), size=(200, -1))
    txt_Apellidos.SetBackgroundColour(wx.Colour(210, 255, 254))

    wx.StaticText(panel, label="Edad:", pos=(60, 240)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Edad = wx.TextCtrl(panel, pos=(140, 236), size=(200, -1))
    txt_Edad.SetBackgroundColour(wx.Colour(210, 255, 254))

    wx.StaticText(panel, label="Correo:", pos=(60, 280)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Correo = wx.TextCtrl(panel, pos=(140, 276), size=(200, -1))
    txt_Correo.SetBackgroundColour(wx.Colour(181, 242, 248))

    wx.StaticText(panel, label="Telefono:", pos=(60, 320)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Telefono = wx.TextCtrl(panel, pos=(140, 316), size=(200, -1))
    txt_Telefono.SetBackgroundColour(wx.Colour(181, 242, 248))

    wx.StaticText(panel, label="Direccion:", pos=(60, 360)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Direccion = wx.TextCtrl(panel, pos=(140, 356), size=(200, -1))
    txt_Direccion.SetBackgroundColour(wx.Colour(181, 242, 248))

    # Funciones CRUD
    def insertar_cliente(event):
        try:
            query = "INSERT INTO cliente (idCliente, idCodigo, Nombre, Apellidos, Edad, Correo, Telefono, Direccion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            valores = (
                txt_idCliente.GetValue(),
                txt_idCodigo.GetValue(),
                txt_Nombre.GetValue(),
                txt_Apellidos.GetValue(),
                txt_Edad.GetValue(),
                txt_Correo.GetValue(),
                txt_Telefono.GetValue(),
                txt_Direccion.GetValue()
            )
            cursor.execute(query, valores)
            conexion.commit()
            wx.MessageBox("Cliente insertado correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al insertar cliente: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def actualizar_cliente(event):
        try:
            query = "UPDATE cliente SET idCodigo=%s, Nombre=%s, Apellidos=%s, Edad=%s, Correo=%s, Telefono=%s, Direccion=%s WHERE idCliente=%s"
            valores = (
                txt_idCodigo.GetValue(),
                txt_Nombre.GetValue(),
                txt_Apellidos.GetValue(),
                txt_Edad.GetValue(),
                txt_Correo.GetValue(),
                txt_Telefono.GetValue(),
                txt_Direccion.GetValue(),
                txt_idCliente.GetValue()
            )
            cursor.execute(query, valores)
            conexion.commit()
            wx.MessageBox("Cliente actualizado correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al actualizar cliente: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def eliminar_cliente(event):
        try:
            query = "DELETE FROM cliente WHERE idCliente=%s"
            cursor.execute(query, (txt_idCliente.GetValue(),))
            conexion.commit()
            wx.MessageBox("Cliente eliminado correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al eliminar cliente: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def leer_cliente(event):
        try:
            query = "SELECT idCliente, idCodigo, Nombre, Apellidos, Edad, Correo, Telefono, Direccion FROM cliente"
            cursor.execute(query)
            resultados = cursor.fetchall()

            if resultados:
                ventana_emergente = wx.Frame(None, title="Listado de Clientes", size=(900, 500))
                panel = wx.Panel(ventana_emergente)

                wx.StaticText(panel, label="Listado de Clientes", pos=(330, 15)).SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))

                headers = ["ID", "Código", "Nombre", "Apellidos", "Edad", "Correo", "Teléfono", "Dirección"]
                for i, header in enumerate(headers):
                    wx.StaticText(panel, label=header, pos=(10 + i * 110, 50)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))

                for row_index, cliente in enumerate(resultados):
                    y = 70 + row_index * 25
                    for col_index, valor in enumerate(cliente):
                        wx.StaticText(panel, label=str(valor), pos=(10 + col_index * 110, y))

                ventana_emergente.Show()
            else:
                wx.MessageBox("No hay clientes registrados", "Información", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al consultar clientes: {e}", "Error", wx.OK | wx.ICON_ERROR)

    # Botones
    wx.Button(panel, label="Guardar", pos=(30, 420), size=(100, 30)).Bind(wx.EVT_BUTTON, insertar_cliente)
    wx.Button(panel, label="Actualizar", pos=(140, 420), size=(100, 30)).Bind(wx.EVT_BUTTON, actualizar_cliente)
    wx.Button(panel, label="Eliminar", pos=(250, 420), size=(100, 30)).Bind(wx.EVT_BUTTON, eliminar_cliente)
    wx.Button(panel, label="Leer", pos=(360, 420), size=(100, 30)).Bind(wx.EVT_BUTTON, leer_cliente)

    ventana.Show()

Cliente()
App.MainLoop()


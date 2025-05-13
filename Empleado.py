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

def Empleado():
    ventana = wx.Frame(None, title='Empleado', size=(500, 490))
    panel = wx.Panel(ventana)

    # Título
    titulo = wx.StaticText(panel, label="Empleados", pos=(180, 30))
    titulo.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD))

    # Campos
    wx.StaticText(panel, label="idEmpleado:", pos=(60, 80)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_idEmpleado = wx.TextCtrl(panel, pos=(140, 76), size=(200, -1))
    txt_idEmpleado.SetBackgroundColour(wx.Colour(254, 241, 147))

    wx.StaticText(panel, label="Contraseña:", pos=(60, 120)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Contraseña = wx.TextCtrl(panel, pos=(140, 116), size=(200, -1), style=wx.TE_PASSWORD)
    txt_Contraseña.SetBackgroundColour(wx.Colour(254, 241, 147))

    wx.StaticText(panel, label="Nombre:", pos=(60, 160)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Nombre = wx.TextCtrl(panel, pos=(140, 156), size=(200, -1))
    txt_Nombre.SetBackgroundColour(wx.Colour(181, 242, 248))

    wx.StaticText(panel, label="Apellidos:", pos=(60, 200)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Apellidos = wx.TextCtrl(panel, pos=(140, 196), size=(200, -1))
    txt_Apellidos.SetBackgroundColour(wx.Colour(210, 255, 254))

    wx.StaticText(panel, label="Edad:", pos=(60, 240)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Edad = wx.TextCtrl(panel, pos=(140, 236), size=(200, -1))
    txt_Edad.SetBackgroundColour(wx.Colour(210, 255, 254))

    wx.StaticText(panel, label="Puesto:", pos=(60, 280)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Puesto = wx.TextCtrl(panel, pos=(140, 276), size=(200, -1))
    txt_Puesto.SetBackgroundColour(wx.Colour(181, 242, 248))

    wx.StaticText(panel, label="Salario:", pos=(60, 320)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Salario = wx.TextCtrl(panel, pos=(140, 316), size=(200, -1))
    txt_Salario.SetBackgroundColour(wx.Colour(181, 242, 248))

    # Funciones CRUD
    def insertar_empleado(event):
        try:
            query = "INSERT INTO empleado (idEmpleado, Contraseña, Nombre, Apellidos, Edad, Puesto, Salario) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            valores = (
                txt_idEmpleado.GetValue(),
                txt_Contraseña.GetValue(),
                txt_Nombre.GetValue(),
                txt_Apellidos.GetValue(),
                txt_Edad.GetValue(),
                txt_Puesto.GetValue(),
                txt_Salario.GetValue()
            )
            cursor.execute(query, valores)
            conexion.commit()
            wx.MessageBox("Empleado insertado correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al insertar empleado: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def actualizar_empleado(event):
        try:
            query = "UPDATE empleado SET Contraseña=%s, Nombre=%s, Apellidos=%s, Edad=%s, Puesto=%s, Salario=%s WHERE idEmpleado=%s"
            valores = (
                txt_Contraseña.GetValue(),
                txt_Nombre.GetValue(),
                txt_Apellidos.GetValue(),
                txt_Edad.GetValue(),
                txt_Puesto.GetValue(),
                txt_Salario.GetValue(),
                txt_idEmpleado.GetValue()
            )
            cursor.execute(query, valores)
            conexion.commit()
            wx.MessageBox("Empleado actualizado correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al actualizar empleado: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def eliminar_empleado(event):
        try:
            query = "DELETE FROM empleado WHERE idEmpleado=%s"
            cursor.execute(query, (txt_idEmpleado.GetValue(),))
            conexion.commit()
            wx.MessageBox("Empleado eliminado correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al eliminar empleado: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def leer_empleado(event):
        try:
            query = "SELECT * FROM empleado WHERE idEmpleado=%s"
            cursor.execute(query, (txt_idEmpleado.GetValue(),))
            resultado = cursor.fetchone()
            if resultado:
                txt_Contraseña.SetValue(resultado[1])
                txt_Nombre.SetValue(resultado[2])
                txt_Apellidos.SetValue(resultado[3])
                txt_Edad.SetValue(str(resultado[4]))
                txt_Puesto.SetValue(resultado[5])
                txt_Salario.SetValue(str(resultado[6]))
            else:
                wx.MessageBox("Empleado no encontrado", "Info", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al leer empleado: {e}", "Error", wx.OK | wx.ICON_ERROR)

    # Botones
    wx.Button(panel, label="Guardar", pos=(30, 380), size=(100, 30)).Bind(wx.EVT_BUTTON, insertar_empleado)
    wx.Button(panel, label="Actualizar", pos=(140, 380), size=(100, 30)).Bind(wx.EVT_BUTTON, actualizar_empleado)
    wx.Button(panel, label="Eliminar", pos=(250, 380), size=(100, 30)).Bind(wx.EVT_BUTTON, eliminar_empleado)
    wx.Button(panel, label="Leer", pos=(360, 380), size=(100, 30)).Bind(wx.EVT_BUTTON, leer_empleado)

    ventana.Show()

Empleado()
Menu.MainLoop()

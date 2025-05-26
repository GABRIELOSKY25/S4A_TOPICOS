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

def Empleado(parent_frame=None):
    ventana = wx.Frame(None, title='Empleado', size=(500, 500))  # Aumenté el tamaño para el botón de regresar
    panel = wx.Panel(ventana)
    ventana.parent_frame = parent_frame  # Guardar referencia al frame padre (menú)

    # Título
    titulo = wx.StaticText(panel, label="Empleados", pos=(180, 30))
    titulo.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD))

    # Campos
    wx.StaticText(panel, label="idEmpleado:", pos=(60, 80)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_idEmpleado = wx.TextCtrl(panel, pos=(140, 76), size=(200, -1))
    txt_idEmpleado.SetBackgroundColour(wx.Colour(254, 241, 147))

    wx.StaticText(panel, label="Nombre:", pos=(60, 120)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Nombre = wx.TextCtrl(panel, pos=(140, 116), size=(200, -1))
    txt_Nombre.SetBackgroundColour(wx.Colour(181, 242, 248))

    wx.StaticText(panel, label="Apellidos:", pos=(60, 160)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Apellidos = wx.TextCtrl(panel, pos=(140, 156), size=(200, -1))
    txt_Apellidos.SetBackgroundColour(wx.Colour(210, 255, 254))

    wx.StaticText(panel, label="Edad:", pos=(60, 200)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Edad = wx.TextCtrl(panel, pos=(140, 196), size=(200, -1))
    txt_Edad.SetBackgroundColour(wx.Colour(210, 255, 254))

    wx.StaticText(panel, label="Puesto:", pos=(60, 240)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Puesto = wx.TextCtrl(panel, pos=(140, 236), size=(200, -1))
    txt_Puesto.SetBackgroundColour(wx.Colour(181, 242, 248))

    wx.StaticText(panel, label="Salario:", pos=(60, 280)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Salario = wx.TextCtrl(panel, pos=(140, 276), size=(200, -1))
    txt_Salario.SetBackgroundColour(wx.Colour(181, 242, 248))

    # Funciones CRUD
    def insertar_empleado(event):
        try:
            query = "INSERT INTO empleado (idEmpleado, Nombre, Apellido, Edad, Puesto, Salario) VALUES (%s, %s, %s, %s, %s, %s)"
            valores = (
                txt_idEmpleado.GetValue(),
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
            query = "UPDATE empleado SET Nombre=%s, Apellido=%s, Edad=%s, Puesto=%s, Salario=%s WHERE idEmpleado=%s"
            valores = (
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
            query = "SELECT idEmpleado, Nombre, Apellido, Puesto, Salario FROM empleado"
            cursor.execute(query)
            resultados = cursor.fetchall()

            if resultados:
                ventana_emergente = wx.Frame(None, title="Listado de Empleados", size=(800, 500))
                panel = wx.Panel(ventana_emergente)

                wx.StaticText(panel, label="Listado de Empleados", pos=(300, 15)).SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))

                headers = ["ID", "Nombre", "Apellido", "Puesto", "Salario"]
                for i, header in enumerate(headers):
                    wx.StaticText(panel, label=header, pos=(20 + i * 150, 50)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))

                for row_index, empleado in enumerate(resultados):
                    y = 70 + row_index * 30
                    for col_index, valor in enumerate(empleado):
                        if col_index == len(empleado)-1:
                            valor = f"${float(valor):,.2f}"
                        wx.StaticText(panel, label=str(valor), pos=(20 + col_index * 150, y))

                ventana_emergente.Show()
            else:
                wx.MessageBox("No hay empleados registrados", "Información", wx.OK | wx.ICON_INFORMATION)

        except Error as e:
            wx.MessageBox(f"Error al consultar empleados: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def regresar_menu(event):
        """Regresa al menú principal"""
        if ventana.parent_frame:
            ventana.parent_frame.Show()  # Mostrar el menú
        ventana.Destroy()  # Cerrar esta ventana

    def on_close(event):
        """Maneja el evento cuando se cierra la ventana"""
        if ventana.parent_frame:
            ventana.parent_frame.Show()  # Mostrar el menú al cerrar
        ventana.Destroy()

    # Botones CRUD
    wx.Button(panel, label="Guardar", pos=(30, 340), size=(100, 30)).Bind(wx.EVT_BUTTON, insertar_empleado)
    wx.Button(panel, label="Actualizar", pos=(140, 340), size=(100, 30)).Bind(wx.EVT_BUTTON, actualizar_empleado)
    wx.Button(panel, label="Eliminar", pos=(250, 340), size=(100, 30)).Bind(wx.EVT_BUTTON, eliminar_empleado)
    wx.Button(panel, label="Leer", pos=(360, 340), size=(100, 30)).Bind(wx.EVT_BUTTON, leer_empleado)
    
    # Botón para regresar al menú
    wx.Button(panel, label="Regresar al menú", pos=(180, 400), size=(150, 30)).Bind(wx.EVT_BUTTON, regresar_menu)

    # Manejar el evento de cerrar ventana
    ventana.Bind(wx.EVT_CLOSE, on_close)

    ventana.Show()

if __name__ == "__main__":
    Ventana = wx.App()
    Empleado()
    Ventana.MainLoop()
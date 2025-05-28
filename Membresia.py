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
except Error as ex:
    print("Error al conectar:", ex)

def Membresia(parent_frame=None):
    ventana = wx.Frame(None, title='Membresía', size=(500, 400))  # Aumenté el tamaño para el botón de regresar
    panel = wx.Panel(ventana)
    ventana.parent_frame = parent_frame  # Guardar referencia al frame padre (menú)

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
            query = "SELECT idCodigo, Fecha_Activacion, Fecha_Vigencia, Tipo FROM membresia"
            cursor.execute(query)
            resultados = cursor.fetchall()

            if resultados:
                # Crear ventana con tamaño adecuado
                ventana_emergente = wx.Frame(None, title="Listado de Membresías", size=(900, 600))
                panel = wx.Panel(ventana_emergente)
                
                # Título centrado
                titulo = wx.StaticText(panel, label="Listado de Membresías", pos=(350, 15))
                titulo.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))

                # Crear ListCtrl (tabla más profesional)
                list_ctrl = wx.ListCtrl(panel, pos=(20, 50), size=(850, 500),
                                    style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
                
                # Configurar columnas con anchos adecuados
                columnas = [
                    ("Código", 150),
                    ("Fecha Activación", 200),
                    ("Fecha Vigencia", 200),
                    ("Tipo", 250)
                ]
                
                for i, (col_name, col_width) in enumerate(columnas):
                    list_ctrl.InsertColumn(i, col_name, width=col_width)
                
                # Llenar tabla con datos
                for membresia in resultados:
                    index = list_ctrl.InsertItem(list_ctrl.GetItemCount(), str(membresia[0]))
                    
                    # Formatear fechas (mostrar solo fecha sin hora)
                    fecha_activacion = str(membresia[1]).split()[0] if membresia[1] else ""
                    fecha_vigencia = str(membresia[2]).split()[0] if membresia[2] else ""
                    
                    # Agregar datos a cada columna
                    list_ctrl.SetItem(index, 1, fecha_activacion)
                    list_ctrl.SetItem(index, 2, fecha_vigencia)
                    list_ctrl.SetItem(index, 3, str(membresia[3]))
                    
                    # Color de fondo blanco para todas las filas
                    list_ctrl.SetItemBackgroundColour(index, wx.WHITE)
                
                # Configuración visual adicional
                list_ctrl.SetBackgroundColour(wx.WHITE)
                list_ctrl.SetForegroundColour(wx.BLACK)
                
                # Ajustar automáticamente el tamaño de las filas
                for i in range(list_ctrl.GetItemCount()):
                    list_ctrl.SetItemState(i, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
                
                ventana_emergente.Show()
            else:
                wx.MessageBox("No hay membresías registradas", "Información", wx.OK | wx.ICON_INFORMATION)

        except Error as ex:
            wx.MessageBox(f"Error al consultar membresías: {ex}", "Error", wx.OK | wx.ICON_ERROR)

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
    boton_Guardar = wx.Button(panel, label="Guardar", pos=(30, 260), size=(100, 30))
    boton_Actualizar = wx.Button(panel, label="Actualizar", pos=(140, 260), size=(100, 30))
    boton_Eliminar = wx.Button(panel, label="Eliminar", pos=(250, 260), size=(100, 30))
    boton_Leer = wx.Button(panel, label="Leer", pos=(360, 260), size=(100, 30))
    
    # Botón para regresar al menú
    boton_Regresar = wx.Button(panel, label="Regresar al menú", pos=(180, 320), size=(150, 30))

    # Eventos
    boton_Guardar.Bind(wx.EVT_BUTTON, guardar_membresia)
    boton_Actualizar.Bind(wx.EVT_BUTTON, actualizar_membresia)
    boton_Eliminar.Bind(wx.EVT_BUTTON, eliminar_membresia)
    boton_Leer.Bind(wx.EVT_BUTTON, leer_membresia)
    boton_Regresar.Bind(wx.EVT_BUTTON, regresar_menu)
    
    # Manejar el evento de cerrar ventana
    ventana.Bind(wx.EVT_CLOSE, on_close)

    ventana.Show()

if __name__ == "__main__":
    Ventana = wx.App()
    Membresia()
    Ventana.MainLoop()
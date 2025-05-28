# Gabriel Flores Urbina

#https://github.com/GABRIELOSKY25/S4A_TOPICOS

import wx
import mysql.connector
from mysql.connector import Error
from Historial_Precio import Historial_Precio

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

def Articulo(parent_frame=None):
    ventana = wx.Frame(None, title='Articulo', size=(500, 550))  # Aumenté el tamaño para el botón de regresar
    panel = wx.Panel(ventana)
    ventana.parent_frame = parent_frame  # Guardar referencia al frame padre (menú)

    # Título
    titulo = wx.StaticText(panel, label="Articulos", pos=(195, 30))
    titulo.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD))

    # Campos
    wx.StaticText(panel, label="idCodigo Barra:", pos=(40, 80)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_idCodigo_Barra = wx.TextCtrl(panel, pos=(140, 76), size=(200, -1))
    txt_idCodigo_Barra.SetBackgroundColour(wx.Colour(254, 241, 147))

    # Campo idCategoria como ComboBox
    wx.StaticText(panel, label="idCategoria:", pos=(40, 120)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    
    # Obtener categorías de la base de datos
    categorias = []
    try:
        cursor.execute("SELECT idCategoria, Nombre FROM categoria")
        categorias = cursor.fetchall()
    except Error as e:
        wx.MessageBox(f"Error al cargar categorías: {e}", "Error", wx.OK | wx.ICON_ERROR)
    
    # Crear ComboBox con las categorías
    combo_categorias = wx.ComboBox(panel, pos=(140, 116), size=(200, -1), style=wx.CB_READONLY)
    combo_categorias.SetBackgroundColour(wx.Colour(254, 241, 147))
    
    # Llenar el ComboBox con los datos
    for cat in categorias:
        combo_categorias.Append(f"{cat[0]} - {cat[1]}", str(cat[0]))  # Mostrar: "ID - Nombre", valor: ID

    wx.StaticText(panel, label="Nombre:", pos=(40, 160)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Nombre = wx.TextCtrl(panel, pos=(140, 156), size=(200, -1))
    txt_Nombre.SetBackgroundColour(wx.Colour(181, 242, 248))

    wx.StaticText(panel, label="Precio:", pos=(40, 200)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Precio = wx.TextCtrl(panel, pos=(140, 196), size=(200, -1))
    txt_Precio.SetBackgroundColour(wx.Colour(181, 242, 248))

    wx.StaticText(panel, label="Existencia:", pos=(40, 240)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Existencia = wx.TextCtrl(panel, pos=(140,236), size=(200, -1))
    txt_Existencia.SetBackgroundColour(wx.Colour(181, 242, 248))

    wx.StaticText(panel, label="Marca:", pos=(40, 280)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Marca = wx.TextCtrl(panel, pos=(140, 276), size=(200, -1))
    txt_Marca.SetBackgroundColour(wx.Colour(181, 242, 248))

    wx.StaticText(panel, label="Caracteristicas:", pos=(40, 320)).SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
    txt_Caracteristicas = wx.TextCtrl(panel, pos=(140, 316), size=(200, -1))
    txt_Caracteristicas.SetBackgroundColour(wx.Colour(181, 242, 248))

    # Funciones CRUD
    def insertar_articulo(event):
        try:
            query = "INSERT INTO articulo (idCodigo_Barra, idCategoria, Nombre, Precio, Existencia, Marca, Caracteristicas) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            valores = (
                txt_idCodigo_Barra.GetValue(),
                combo_categorias.GetClientData(combo_categorias.GetSelection()),
                txt_Nombre.GetValue(),
                txt_Precio.GetValue(),
                txt_Existencia.GetValue(),
                txt_Marca.GetValue(),
                txt_Caracteristicas.GetValue()
            )
            cursor.execute(query, valores)
            conexion.commit()
            wx.MessageBox("Articulo insertado correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al insertar articulo: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def actualizar_articulo(event):
        try:
            query = "UPDATE articulo SET idCategoria=%s, Nombre=%s, Precio=%s, Existencia=%s, Marca=%s, Caracteristicas=%s WHERE idCodigo_Barra=%s"
            valores = (
                combo_categorias.GetClientData(combo_categorias.GetSelection()),
                txt_Nombre.GetValue(),
                txt_Precio.GetValue(),
                txt_Existencia.GetValue(),
                txt_Marca.GetValue(),
                txt_Caracteristicas.GetValue(),
                txt_idCodigo_Barra.GetValue()
            )
            cursor.execute(query, valores)
            conexion.commit()
            wx.MessageBox("Articulo actualizado correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al actualizar el articulo: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def eliminar_articulo(event):
        try:
            query = "DELETE FROM articulo WHERE idCodigo_Barra=%s"
            valores = (txt_idCodigo_Barra.GetValue(),)
            cursor.execute(query, valores)
            conexion.commit()
            wx.MessageBox("Articulo eliminado correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al eliminar articulo: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def leer_articulo(event):
        try:
            query = "SELECT * FROM articulo"
            cursor.execute(query)
            resultados = cursor.fetchall()

            if resultados:
                # Crear ventana emergente
                ventana_emergente = wx.Frame(None, title="Listado de Artículos", size=(1200, 600))
                panel = wx.Panel(ventana_emergente)
                
                # Título
                titulo = wx.StaticText(panel, label="Listado de Artículos", pos=(450, 15))
                titulo.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))

                # Crear ListCtrl con fondo completamente blanco
                list_ctrl = wx.ListCtrl(panel, pos=(20, 50), size=(1150, 500),
                                    style=wx.LC_REPORT)
                
                # Configurar columnas
                columnas = [
                    ("Código Barras", 150),
                    ("ID Categoría", 100),
                    ("Nombre", 200),
                    ("Precio", 100),
                    ("Existencia", 100),
                    ("Marca", 150),
                    ("Características", 300)
                ]
                
                for i, (col_name, col_width) in enumerate(columnas):
                    list_ctrl.InsertColumn(i, col_name, width=col_width)
                
                # Llenar con datos
                for articulo in resultados:
                    index = list_ctrl.InsertItem(list_ctrl.GetItemCount(), str(articulo[0]))
                    
                    for col in range(1, 7):
                        if col == 3:  # Columna de Precio
                            list_ctrl.SetItem(index, col, f"${float(articulo[col]):.2f}")
                        else:
                            list_ctrl.SetItem(index, col, str(articulo[col]))
                    
                    # Fondo blanco para todas las filas
                    list_ctrl.SetItemBackgroundColour(index, wx.WHITE)
                
                # Configurar color blanco para toda la tabla
                list_ctrl.SetBackgroundColour(wx.WHITE)
                list_ctrl.SetForegroundColour(wx.BLACK)  # Texto en negro
                
                ventana_emergente.Show()
            else:
                wx.MessageBox("No hay artículos registrados", "Información", wx.OK | wx.ICON_INFORMATION)

        except Error as e:
            wx.MessageBox(f"Error al consultar artículos: {e}", "Error", wx.OK | wx.ICON_ERROR)

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
    wx.Button(panel, label="Guardar", pos=(30, 380), size=(100, 30)).Bind(wx.EVT_BUTTON, insertar_articulo)
    wx.Button(panel, label="Actualizar", pos=(140, 380), size=(100, 30)).Bind(wx.EVT_BUTTON, actualizar_articulo)
    wx.Button(panel, label="Eliminar", pos=(250, 380), size=(100, 30)).Bind(wx.EVT_BUTTON, eliminar_articulo)
    wx.Button(panel, label="Leer", pos=(360, 380), size=(100, 30)).Bind(wx.EVT_BUTTON, leer_articulo)

    def abrir_historial(event):
        Historial_Precio()

    # Botón para Historial de Precios
    wx.Button(panel, label="Historial Precios", pos=(180, 430), size=(150, 30)).Bind(wx.EVT_BUTTON, abrir_historial)

    # Botón para regresar al menú
    wx.Button(panel, label="Regresar al menú", pos=(180, 470), size=(150, 30)).Bind(wx.EVT_BUTTON, regresar_menu)

    # Manejar el evento de cerrar ventana
    ventana.Bind(wx.EVT_CLOSE, on_close)

    ventana.Show()

if __name__ == "__main__":
    Ventana = wx.App()
    Articulo()
    Ventana.MainLoop()
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

def Articulo():
    ventana = wx.Frame(None, title='Articulo', size=(500, 500))
    panel = wx.Panel(ventana)

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
                ventana_emergente = wx.Frame(None, title="Listado de Articulos", size=(850, 500))
                panel = wx.Panel(ventana_emergente)

                wx.StaticText(panel, label="Listado de Articulos", pos=(150, 15)).SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))

                # Encabezados
                headers = ["Código Barras", "ID Categoría", "Nombre", "Precio", "Existencia", "Marca", "Características"]
                for i, header in enumerate(headers):
                    wx.StaticText(panel, label=header, pos=(20 + i * 100, 50)).SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD))

                # Mostrar cada categoría
                for row_index, articulo in enumerate(resultados):
                    y = 70 + row_index * 30
                    for col_index, valor in enumerate(articulo):
                        wx.StaticText(panel, label=str(valor), pos=(20 + col_index * 100, y))


                ventana_emergente.Show()
            else:
                wx.MessageBox("No hay articulos registrados", "Información", wx.OK | wx.ICON_INFORMATION)

        except Error as e:
            wx.MessageBox(f"Error al consultar articulos: {e}", "Error", wx.OK | wx.ICON_ERROR)

    # Botones
    wx.Button(panel, label="Guardar", pos=(30, 380), size=(100, 30)).Bind(wx.EVT_BUTTON, insertar_articulo)
    wx.Button(panel, label="Actualizar", pos=(140, 380), size=(100, 30)).Bind(wx.EVT_BUTTON, actualizar_articulo)
    wx.Button(panel, label="Eliminar", pos=(250, 380), size=(100, 30)).Bind(wx.EVT_BUTTON, eliminar_articulo)
    wx.Button(panel, label="Leer", pos=(360, 380), size=(100, 30)).Bind(wx.EVT_BUTTON, leer_articulo)

    ventana.Show()

if __name__ == "__main__":
    Ventana = wx.App()
    Articulo()
    Ventana.MainLoop()
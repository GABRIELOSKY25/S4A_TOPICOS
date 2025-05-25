# Gabriel Flores Urbina

#https://github.com/GABRIELOSKY25/S4A_TOPICOS

import wx
from Membresia import Membresia
from Cliente import Cliente
from Empleado import Empleado
from Punto_Venta import PuntoVenta
from Articulo import Articulo
from Categoria import Categoria
from Proveedor import Proveedor
from Punto_Pedido import PedidoFrame

Ventana = wx.App()  

def Menu():
    ventana = wx.Frame(None, title='Menu', size=(500, 370))
    panel = wx.Panel(ventana)

    # Título
    titulo = wx.StaticText(panel, label="Menu", pos=(210, 30))
    titulo.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD))

    # Botones
    boton_Membresia = wx.Button(panel, label = "Membresia", pos=(60, 70), size=(100, 30))
    boton_Cliente = wx.Button(panel, label = "Cliente", pos=(60, 120), size=(100, 30))
    boton_Empledado = wx.Button(panel, label = "Empledado", pos=(60, 170), size=(100, 30))
    boton_Punto_Venta = wx.Button(panel, label = "Punto de Venta", pos=(60, 220), size=(100, 30))
    
    boton_Articulo = wx.Button(panel, label = "Articulo", pos=(310, 70), size=(100, 30))
    boton_Categoria = wx.Button(panel, label = "Categoria", pos=(310, 120), size=(100, 30))
    boton_Proveedor = wx.Button(panel, label = "Proveedor", pos=(310, 170), size=(100, 30))
    boton_Punto_Pedido = wx.Button(panel, label = "Pedido", pos=(310, 220), size=(100, 30))

    # Eventos
    boton_Membresia.Bind(wx.EVT_BUTTON, lambda event: Membresia())
    boton_Cliente.Bind(wx.EVT_BUTTON, lambda event: Cliente())
    boton_Empledado.Bind(wx.EVT_BUTTON, lambda event: Empleado())
    boton_Punto_Venta.Bind(wx.EVT_BUTTON, lambda event: PuntoVenta())
    boton_Articulo.Bind(wx.EVT_BUTTON, lambda event: Articulo())
    boton_Categoria.Bind(wx.EVT_BUTTON, lambda event: Categoria())
    boton_Proveedor.Bind(wx.EVT_BUTTON, lambda event: Proveedor())
    boton_Punto_Pedido.Bind(wx.EVT_BUTTON, lambda event: PedidoFrame())
    
    ventana.Show()

Menu()
Ventana.MainLoop()
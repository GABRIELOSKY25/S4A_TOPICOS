# Gabriel Flores Urbina
# https://github.com/GABRIELOSKY25/S4A_TOPICOS

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
    boton_Membresia = wx.Button(panel, label="Membresia", pos=(60, 70), size=(100, 30))
    boton_Cliente = wx.Button(panel, label="Cliente", pos=(60, 120), size=(100, 30))
    boton_Empledado = wx.Button(panel, label="Empledado", pos=(60, 170), size=(100, 30))
    boton_Punto_Venta = wx.Button(panel, label="Punto de Venta", pos=(60, 220), size=(100, 30))
    
    boton_Articulo = wx.Button(panel, label="Articulo", pos=(310, 70), size=(100, 30))
    boton_Categoria = wx.Button(panel, label="Categoria", pos=(310, 120), size=(100, 30))
    boton_Proveedor = wx.Button(panel, label="Proveedor", pos=(310, 170), size=(100, 30))
    boton_Punto_Pedido = wx.Button(panel, label="Punto de Pedido", pos=(310, 220), size=(100, 30))
    
    # Botón de Salida (nuevo)
    boton_Salir = wx.Button(panel, label="Salir", pos=(185, 280), size=(100, 30))

    # Funciones para abrir ventanas
    def abrir_membresia(event):
        ventana.Hide()
        Membresia(ventana)  

    def abrir_cliente(event):
        ventana.Hide() 
        Cliente(ventana)  
    
    def abrir_empleado(event):
        ventana.Hide()  
        Empleado(ventana)   

    def abrir_punto_venta(event):
        ventana.Hide() 
        PuntoVenta(ventana)  

    def abrir_articulo(event):
        ventana.Hide()  
        Articulo(ventana) 

    def abrir_categoria(event):
        ventana.Hide()  
        Categoria(ventana) 

    def abrir_proveedor(event):
        ventana.Hide()  
        Proveedor(ventana)  

    def abrir_pedidos(event):
        ventana.Hide()  
        PedidoFrame(ventana) 
        
    def salir(event):
        ventana.Close()

    # Eventos de los botones
    boton_Membresia.Bind(wx.EVT_BUTTON, abrir_membresia)
    boton_Cliente.Bind(wx.EVT_BUTTON, abrir_cliente)
    boton_Empledado.Bind(wx.EVT_BUTTON, abrir_empleado)
    boton_Punto_Venta.Bind(wx.EVT_BUTTON, abrir_punto_venta)
    boton_Articulo.Bind(wx.EVT_BUTTON, abrir_articulo)
    boton_Categoria.Bind(wx.EVT_BUTTON, abrir_categoria)
    boton_Proveedor.Bind(wx.EVT_BUTTON, abrir_proveedor)
    boton_Punto_Pedido.Bind(wx.EVT_BUTTON, abrir_pedidos)
    boton_Salir.Bind(wx.EVT_BUTTON, salir)  
    
    ventana.Show()

Menu()
Ventana.MainLoop()
import wx
import mysql.connector
from datetime import datetime, timedelta

# Conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="peresoso888",
    database="COSTCO"
)
cursor = conexion.cursor(dictionary=True)

class PedidoFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Sistema de Pedidos - COSTCO", size=(1000, 600))
        panel = wx.Panel(self)
        self.detalle_pedido = []
        self.total = 0.0

        # Lista de productos
        self.lst_productos = wx.ListCtrl(panel, style=wx.LC_REPORT, pos=(10, 10), size=(450, 400))
        self.lst_productos.InsertColumn(0, "Código", width=120)
        self.lst_productos.InsertColumn(1, "Nombre", width=150)
        self.lst_productos.InsertColumn(2, "Precio", width=80)
        self.lst_productos.InsertColumn(3, "Existencia", width=80)
        self.cargar_productos()

        # Lista detalle de pedido
        self.lst_detalle = wx.ListCtrl(panel, style=wx.LC_REPORT, pos=(480, 10), size=(500, 400))
        self.lst_detalle.InsertColumn(0, "Producto", width=150)
        self.lst_detalle.InsertColumn(1, "Cantidad", width=100)
        self.lst_detalle.InsertColumn(2, "Subtotal", width=100)

        # Total
        wx.StaticText(panel, label="Total:", pos=(480, 420))
        self.txt_total = wx.TextCtrl(panel, pos=(530, 416), size=(100, -1), style=wx.TE_READONLY)

        # Campo ID Proveedor
        wx.StaticText(panel, label="ID Proveedor:", pos=(10, 420))
        self.txt_idProveedor = wx.TextCtrl(panel, pos=(110, 416), size=(100, -1))

        # Botones
        wx.Button(panel, label="Agregar Producto", pos=(10, 460), size=(150, 30)).Bind(wx.EVT_BUTTON, self.agregar_producto)
        wx.Button(panel, label="Guardar Pedido", pos=(180, 460), size=(150, 30)).Bind(wx.EVT_BUTTON, self.guardar_pedido)
        wx.Button(panel, label="Consultar Proveedores", pos=(350, 460), size=(180, 30)).Bind(wx.EVT_BUTTON, self.consultar_proveedores)

        self.Show()

    def cargar_productos(self):
        self.lst_productos.DeleteAllItems()
        cursor.execute("SELECT idCodigo_Barra, Nombre, Precio, Existencia FROM Articulo")
        for row in cursor.fetchall():
            index = self.lst_productos.InsertItem(self.lst_productos.GetItemCount(), row["idCodigo_Barra"])
            self.lst_productos.SetItem(index, 1, row["Nombre"])
            self.lst_productos.SetItem(index, 2, str(row["Precio"]))
            self.lst_productos.SetItem(index, 3, str(row["Existencia"]))

    def agregar_producto(self, event):
        index = self.lst_productos.GetFirstSelected()
        if index == -1:
            wx.MessageBox("Seleccione un producto", "Advertencia", wx.OK | wx.ICON_WARNING)
            return

        codigo = self.lst_productos.GetItem(index, 0).GetText()
        nombre = self.lst_productos.GetItem(index, 1).GetText()
        precio = float(self.lst_productos.GetItem(index, 2).GetText())

        cantidad = wx.GetNumberFromUser(f"Ingrese cantidad para '{nombre}'", "Cantidad:", "Cantidad", 1, 1, 100)
        if cantidad == -1:
            return

        subtotal = precio * cantidad
        self.total += subtotal
        self.txt_total.SetValue(f"{self.total:.2f}")

        idx = self.lst_detalle.InsertItem(self.lst_detalle.GetItemCount(), nombre)
        self.lst_detalle.SetItem(idx, 1, str(cantidad))
        self.lst_detalle.SetItem(idx, 2, f"{subtotal:.2f}")

        self.detalle_pedido.append((codigo, nombre, precio, cantidad, subtotal))

    def guardar_pedido(self, event):
        idProveedor = self.txt_idProveedor.GetValue()

        if not idProveedor or not self.detalle_pedido:
            wx.MessageBox("Complete el ID del proveedor y agregue productos", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            cursor.execute("SELECT MAX(idPedido) + 1 AS nuevo_id FROM Pedido")
            idPedido = cursor.fetchone()["nuevo_id"] or 1

            fecha_pedido = datetime.now()
            fecha_entrega = fecha_pedido + timedelta(days=7)

            cursor.execute("""
                INSERT INTO Pedido (idPedido, idProveedor, Fecha_Pedido, Fecha_Entrega, Importe, Estado)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (idPedido, idProveedor, fecha_pedido, fecha_entrega, self.total, "Preparando"))

            for codigo, nombre, precio, cantidad, subtotal in self.detalle_pedido:
                cursor.execute("""
                    INSERT INTO detalle_pedido (idCodigo_Barra, idPedido, Cantidad, Subtotal, Precio_Unitario)
                    VALUES (%s, %s, %s, %s, %s)
                """, (codigo, idPedido, cantidad, subtotal, precio))

                # Actualizar inventario (aumentar existencia)
                cursor.execute("""
                    UPDATE Articulo SET Existencia = Existencia + %s WHERE idCodigo_Barra = %s
                """, (cantidad, codigo))

            conexion.commit()
            wx.MessageBox("Pedido registrado correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.limpiar_formulario()

        except Exception as e:
            conexion.rollback()
            wx.MessageBox(f"Error al guardar pedido:\n{e}", "Error", wx.OK | wx.ICON_ERROR)

    def limpiar_formulario(self):
        self.detalle_pedido = []
        self.total = 0.0
        self.txt_total.SetValue("")
        self.txt_idProveedor.SetValue("")
        self.lst_detalle.DeleteAllItems()
        self.cargar_productos()

    def consultar_proveedores(self, event):
        cursor.execute("SELECT idProveedor, Nombre FROM Proveedor")
        proveedores = cursor.fetchall()
        lista = "\n".join([f"ID: {p['idProveedor']} - {p['Nombre']}" for p in proveedores])
        wx.MessageBox(lista if lista else "No hay proveedores registrados", "IDs de Proveedores", wx.OK | wx.ICON_INFORMATION)

if __name__ == "__main__":
    app = wx.App(False)
    frame = PedidoFrame()
    app.MainLoop()
import wx
import mysql.connector
from datetime import datetime

# Conexión a la base de datos MySQL
conexion = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="peresoso888",
    database="COSTCO"
)
cursor = conexion.cursor(dictionary=True)

class PuntoVenta(wx.Frame):
    def __init__(self, parent_frame=None):
        super().__init__(None, title="Punto de Venta COSTCO", size=(1005, 600))
        self.parent_frame = parent_frame  # Referencia al frame padre (menú)
        panel = wx.Panel(self)
        self.detalle_venta = []
        self.total = 0.0

        # Lista de productos
        self.lst_productos = wx.ListCtrl(panel, style=wx.LC_REPORT, pos=(10, 10), size=(450, 400))
        self.lst_productos.InsertColumn(0, "Código", width=120)
        self.lst_productos.InsertColumn(1, "Nombre", width=150)
        self.lst_productos.InsertColumn(2, "Precio", width=80)
        self.lst_productos.InsertColumn(3, "Existencia", width=80)
        self.cargar_productos()

        # Lista detalle de venta
        self.lst_detalle = wx.ListCtrl(panel, style=wx.LC_REPORT, pos=(480, 10), size=(500, 400))
        self.lst_detalle.InsertColumn(0, "Producto", width=150)
        self.lst_detalle.InsertColumn(1, "Cantidad", width=100)
        self.lst_detalle.InsertColumn(2, "Subtotal", width=100)

        # Total
        wx.StaticText(panel, label="Total:", pos=(480, 420))
        self.txt_total = wx.TextCtrl(panel, pos=(530, 416), size=(100, -1), style=wx.TE_READONLY)

        # Campos
        wx.StaticText(panel, label="ID Cliente:", pos=(10, 420))
        self.txt_idCliente = wx.TextCtrl(panel, pos=(90, 416), size=(80, -1))

        wx.StaticText(panel, label="Código Membresía:", pos=(180, 420))
        self.txt_idCodigo = wx.TextCtrl(panel, pos=(310, 416), size=(120, -1))

        wx.StaticText(panel, label="ID Empleado:", pos=(10, 460))
        self.txt_idEmpleado = wx.TextCtrl(panel, pos=(90, 456), size=(80, -1))

        # Campo de entrada para lector de código de barras
        wx.StaticText(panel, label="Código de Barras:", pos=(740, 420))
        self.txt_codigo_barras = wx.TextCtrl(panel, pos=(850, 416), size=(130, -1))
        self.txt_codigo_barras.SetHint("Escanea aquí")
        self.txt_codigo_barras.SetWindowStyleFlag(wx.TE_PROCESS_ENTER)
        self.txt_codigo_barras.Bind(wx.EVT_TEXT_ENTER, self.on_codigo_barras)
        self.txt_codigo_barras.SetFocus()

        # Botones
        wx.Button(panel, label="Agregar", pos=(10, 500), size=(100, 30)).Bind(wx.EVT_BUTTON, self.agregar_producto)
        wx.Button(panel, label="Guardar Venta", pos=(120, 500), size=(120, 30)).Bind(wx.EVT_BUTTON, self.guardar_venta)
        wx.Button(panel, label="Consultar Clientes", pos=(250, 500), size=(150, 30)).Bind(wx.EVT_BUTTON, self.consultar_clientes)
        wx.Button(panel, label="Consultar Empleado", pos=(410, 500), size=(150, 30)).Bind(wx.EVT_BUTTON, self.consultar_empleado)
        wx.Button(panel, label="Consultar Membresia", pos=(570, 500), size=(150, 30)).Bind(wx.EVT_BUTTON, self.consultar_membresia)
        wx.Button(panel, label="Regresar al menu", pos=(730, 500), size=(150, 30)).Bind(wx.EVT_BUTTON, self.regresar_menu)

        # Manejar el evento de cerrar ventana
        self.Bind(wx.EVT_CLOSE, self.on_close)

        # Manejar el evento de cerrar ventana
        self.Bind(wx.EVT_CLOSE, self.on_close)

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

        existencia = int(self.lst_productos.GetItem(index, 3).GetText())
        if existencia <= 0:
            wx.MessageBox("El producto seleccionado no tiene existencia disponible.", "Advertencia", wx.OK | wx.ICON_WARNING)
            return

        nombre = self.lst_productos.GetItem(index, 1).GetText()
        precio = float(self.lst_productos.GetItem(index, 2).GetText())
        codigo = self.lst_productos.GetItem(index, 0).GetText()

        cantidad = wx.GetNumberFromUser(f"Ingrese cantidad para '{nombre}'", "Cantidad:", "Cantidad", 1, 1, existencia)
        if cantidad == -1:
            return

        subtotal = precio * cantidad
        self.total += subtotal
        self.txt_total.SetValue(f"{self.total:.2f}")

        index_detalle = self.lst_detalle.InsertItem(self.lst_detalle.GetItemCount(), nombre)
        self.lst_detalle.SetItem(index_detalle, 1, str(cantidad))
        self.lst_detalle.SetItem(index_detalle, 2, f"{subtotal:.2f}")

        self.detalle_venta.append((codigo, nombre, precio, cantidad, subtotal))

    def on_codigo_barras(self, event):
        codigo = self.txt_codigo_barras.GetValue().strip()
        if not codigo:
            return

        for i in range(self.lst_productos.GetItemCount()):
            item_codigo = self.lst_productos.GetItem(i, 0).GetText()
            if item_codigo == codigo:
                self.lst_productos.Select(i)
                self.lst_productos.Focus(i)
                self.txt_codigo_barras.SetValue("")
                self.agregar_producto(None)
                return

        wx.MessageBox("Producto no encontrado con ese código de barras", "Error", wx.OK | wx.ICON_ERROR)
        self.txt_codigo_barras.SetValue("")

    def guardar_venta(self, event):
        idCliente = self.txt_idCliente.GetValue()
        idCodigo = self.txt_idCodigo.GetValue()
        idEmpleado = self.txt_idEmpleado.GetValue()

        if not (idCliente and idCodigo and idEmpleado and self.detalle_venta):
            wx.MessageBox("Complete todos los campos y agregue productos", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("SELECT MAX(idVenta) + 1 AS nuevo_id FROM Venta")
            idVenta = cursor.fetchone()["nuevo_id"] or 1

            cursor.execute("""
                INSERT INTO Venta (idVenta, idCliente, idCodigo, idEmpleado, Importe, Fecha_Hora)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (idVenta, idCliente, idCodigo, idEmpleado, self.total, fecha_hora))

            for codigo, nombre, precio, cantidad, subtotal in self.detalle_venta:
                cursor.execute("""
                    INSERT INTO Detalles_Venta (idVenta, idCodigo_Barra, Cantidad, Subtotal, Precio_Unitario)
                    VALUES (%s, %s, %s, %s, %s)
                """, (idVenta, codigo, cantidad, subtotal, precio))

                cursor.execute("""
                    UPDATE Articulo SET Existencia = Existencia - %s WHERE idCodigo_Barra = %s
                """, (cantidad, codigo))

            conexion.commit()
            wx.MessageBox("Venta registrada correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.limpiar_pantalla()

        except Exception as e:
            wx.MessageBox(f"Error al guardar venta:\n{e}", "Error", wx.OK | wx.ICON_ERROR)

    def limpiar_pantalla(self):
        self.txt_idCliente.SetValue("")
        self.txt_idCodigo.SetValue("")
        self.txt_idEmpleado.SetValue("")
        self.txt_codigo_barras.SetValue("")
        self.lst_detalle.DeleteAllItems()
        self.detalle_venta = []
        self.total = 0.0
        self.txt_total.SetValue("")
        self.cargar_productos()

    def consultar_clientes(self, event):
        cursor.execute("SELECT idCliente, Nombre FROM Cliente")
        clientes = cursor.fetchall()
        lista = "\n".join([f"ID: {c['idCliente']} - {c['Nombre']}" for c in clientes])
        wx.MessageBox(lista if lista else "No hay clientes registrados", "IDs de Clientes", wx.OK | wx.ICON_INFORMATION)

    def consultar_empleado(self, event):
        cursor.execute("SELECT idEmpleado, Nombre FROM Empleado")
        clientes = cursor.fetchall()
        lista = "\n".join([f"ID: {c['idEmpleado']} - {c['Nombre']}" for c in clientes])
        wx.MessageBox(lista if lista else "No hay empleados registrados", "IDs de Empleados", wx.OK | wx.ICON_INFORMATION)

    def consultar_membresia(self, event):
        cursor.execute("SELECT idCodigo, Tipo FROM Membresia")
        clientes = cursor.fetchall()
        lista = "\n".join([f"ID: {c['idCodigo']} - {c['Tipo']}" for c in clientes])
        wx.MessageBox(lista if lista else "No hay membresias registradas", "IDs de Membresia", wx.OK | wx.ICON_INFORMATION)

    def regresar_menu(self, event):
        """Regresa al menú principal"""
        if self.parent_frame:
            self.parent_frame.Show()  # Mostrar el menú
        self.Close()  # Cerrar esta ventana

    def on_close(self, event):
        """Maneja el evento cuando se cierra la ventana"""
        if self.parent_frame:
            self.parent_frame.Show()  # Mostrar el menú al cerrar
        self.Destroy()

if __name__ == "__main__":
    app = wx.App(False)
    frame = PuntoVenta()
    app.MainLoop()
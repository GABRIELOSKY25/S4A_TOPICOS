import wx
import mysql.connector
from datetime import datetime, timedelta
import textwrap

# Conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="peresoso888",
    database="COSTCO"
)
cursor = conexion.cursor(dictionary=True)

class PedidoFrame(wx.Frame):
    def __init__(self, parent_frame=None):
        super().__init__(None, title="Sistema de Pedidos - COSTCO", size=(1000, 600))
        self.parent_frame = parent_frame  # Referencia al frame padre (menú)
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

        # Campo de entrada para lector de código de barras
        wx.StaticText(panel, label="Código de Barras:", pos=(740, 420))
        self.txt_codigo_barras = wx.TextCtrl(panel, pos=(850, 416), size=(130, -1), style=wx.TE_PROCESS_ENTER)
        self.txt_codigo_barras.SetHint("Escanea aquí")
        self.txt_codigo_barras.Bind(wx.EVT_TEXT_ENTER, self.on_codigo_barras)
        self.txt_codigo_barras.SetFocus()

        # Botones
        wx.Button(panel, label="Agregar Producto", pos=(10, 460), size=(150, 30)).Bind(wx.EVT_BUTTON, self.agregar_producto)
        wx.Button(panel, label="Guardar Pedido", pos=(180, 460), size=(150, 30)).Bind(wx.EVT_BUTTON, self.guardar_pedido)
        wx.Button(panel, label="Consultar Proveedores", pos=(350, 460), size=(180, 30)).Bind(wx.EVT_BUTTON, self.consultar_proveedores)
        wx.Button(panel, label="Regresar al menu", pos=(550, 460), size=(150, 30)).Bind(wx.EVT_BUTTON, self.regresar_menu)

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

        codigo = self.lst_productos.GetItem(index, 0).GetText()
        nombre = self.lst_productos.GetItem(index, 1).GetText()
        precio = float(self.lst_productos.GetItem(index, 2).GetText())
        existencia_total = int(self.lst_productos.GetItem(index, 3).GetText())

        # Calcular cantidad ya agregada
        cantidad_ya_agregada = sum([item[3] for item in self.detalle_pedido if item[0] == codigo])

        cantidad = wx.GetNumberFromUser(
            f"Ingrese cantidad para '{nombre}'\n(Existencia actual: {existencia_total})", 
            "Cantidad:", 
            "Cantidad", 
            1, 1, 1000)  # Permitir pedir más de lo que hay en existencia
        
        if cantidad <= 0:
            return

        # Verificar si el producto ya está en el detalle
        producto_existente = next((item for item in self.detalle_pedido if item[0] == codigo), None)
        
        if producto_existente:
            # Actualizar cantidad y subtotal
            idx = self.detalle_pedido.index(producto_existente)
            nueva_cantidad = producto_existente[3] + cantidad
            nuevo_subtotal = nueva_cantidad * precio
            
            # Actualizar lista detalle
            for i in range(self.lst_detalle.GetItemCount()):
                if self.lst_detalle.GetItem(i, 0).GetText() == nombre:
                    self.lst_detalle.SetItem(i, 1, str(nueva_cantidad))
                    self.lst_detalle.SetItem(i, 2, f"{nuevo_subtotal:.2f}")
                    break
            
            # Actualizar detalle_pedido
            self.detalle_pedido[idx] = (codigo, nombre, precio, nueva_cantidad, nuevo_subtotal)
        else:
            # Agregar nuevo producto
            subtotal = precio * cantidad
            index_detalle = self.lst_detalle.InsertItem(self.lst_detalle.GetItemCount(), nombre)
            self.lst_detalle.SetItem(index_detalle, 1, str(cantidad))
            self.lst_detalle.SetItem(index_detalle, 2, f"{subtotal:.2f}")
            self.detalle_pedido.append((codigo, nombre, precio, cantidad, subtotal))

        # Actualizar total
        self.total = sum(item[4] for item in self.detalle_pedido)
        self.txt_total.SetValue(f"{self.total:.2f}")

    def on_codigo_barras(self, event):
        codigo = self.txt_codigo_barras.GetValue().strip()
        if not codigo:
            return

        encontrado = False
        for i in range(self.lst_productos.GetItemCount()):
            item_codigo = self.lst_productos.GetItem(i, 0).GetText()
            if item_codigo == codigo:
                self.lst_productos.Select(i)
                self.lst_productos.Focus(i)
                encontrado = True
                self.agregar_producto(None)
                break

        if not encontrado:
            wx.MessageBox("Producto no encontrado con ese código de barras", "Error", wx.OK | wx.ICON_ERROR)
        
        self.txt_codigo_barras.SetValue("")
        self.txt_codigo_barras.SetFocus()

    def guardar_pedido(self, event):
        idProveedor = self.txt_idProveedor.GetValue()

        if not idProveedor or not self.detalle_pedido:
            wx.MessageBox("Complete el ID del proveedor y agregue productos", "Error", wx.OK | wx.ICON_ERROR)
            return

        # Mostrar diálogo para ingresar el pago
        dlg = wx.TextEntryDialog(self, f"Ingrese el monto con el que paga (Total: ${self.total:.2f})", "Pago")
        dlg.SetValue(f"{self.total:.2f}")
        
        if dlg.ShowModal() != wx.ID_OK:
            return
        
        try:
            pago = float(dlg.GetValue())
        except ValueError:
            wx.MessageBox("Ingrese un monto válido", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        if pago < self.total:
            wx.MessageBox(f"El pago (${pago:.2f}) es menor al total (${self.total:.2f})", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        cambio = pago - self.total

        try:
            cursor.execute("SELECT MAX(idPedido) + 1 AS nuevo_id FROM Pedido")
            result = cursor.fetchone()
            idPedido = result["nuevo_id"] if result["nuevo_id"] is not None else 1

            fecha_pedido = datetime.now()
            fecha_entrega = fecha_pedido + timedelta(days=7)

            # Obtener información del proveedor para el ticket
            cursor.execute("SELECT Nombre FROM Proveedor WHERE idProveedor = %s", (idProveedor,))
            proveedor = cursor.fetchone()
            nombre_proveedor = proveedor["Nombre"] if proveedor else "Proveedor no encontrado"

            # Insertar pedido con todos los campos requeridos
            cursor.execute("""
                INSERT INTO Pedido (idPedido, idProveedor, Fecha_Pedido, Fecha_Entrega, Importe, Pago, Cambio, Estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (idPedido, idProveedor, fecha_pedido, fecha_entrega, self.total, pago, cambio, "Preparando"))

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
            
            # Generar y mostrar el ticket
            self.generar_ticket_pedido(idPedido, fecha_pedido, fecha_entrega, nombre_proveedor, pago, cambio)
            self.limpiar_formulario()

        except Exception as e:
            conexion.rollback()
            wx.MessageBox(f"Error al guardar pedido:\n{e}", "Error", wx.OK | wx.ICON_ERROR)
        finally:
            dlg.Destroy()

    def generar_ticket_pedido(self, id_pedido, fecha_pedido, fecha_entrega, nombre_proveedor, pago, cambio):
        # Crear el contenido del ticket
        ticket = f"""
        {'COSTCO - ORDEN DE COMPRA'.center(50)}
        {'\n'.join(textwrap.wrap('Av. de los Insurgentes Sur 1800, Florida, 01030 Ciudad de México, CDMX', width=50))}
        {'\n'.join(textwrap.wrap('Tel: 55 5261 9100', width=50))}
        
        {'='*50}
        Fecha Pedido: {fecha_pedido.strftime('%Y-%m-%d %H:%M:%S')}
        Fecha Entrega: {fecha_entrega.strftime('%Y-%m-%d %H:%M:%S')}
        Pedido: #{id_pedido}
        {'='*50}
        Proveedor: {nombre_proveedor}
        {'='*50}
        PRODUCTOS:
        """
        
        for item in self.detalle_pedido:
            producto_line = f"{item[1]} x{item[3]} @${item[2]:.2f}"
            subtotal_line = f"${item[4]:.2f}".rjust(50 - len(producto_line))
            ticket += f"\n{producto_line}{subtotal_line}"
        
        ticket += f"""
        {'='*50}
        {'TOTAL:'.ljust(40)} ${self.total:.2f}
        {'PAGO:'.ljust(40)} ${pago:.2f}
        {'CAMBIO:'.ljust(40)} ${cambio:.2f}
        {'='*50}
        {'ESTADO: Preparando'.center(50)}
        {'='*50}
        {'¡ORDEN REGISTRADA!'.center(50)}
        """
        
        # Mostrar el ticket en un diálogo
        dlg = wx.Dialog(self, title="Ticket de Pedido", size=(600, 700))
        panel = wx.Panel(dlg)
        text = wx.TextCtrl(panel, value=ticket, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        font = wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        text.SetFont(font)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text, 1, wx.EXPAND|wx.ALL, 10)
        panel.SetSizer(sizer)
        
        btn_imprimir = wx.Button(panel, label="Imprimir")
        btn_imprimir.Bind(wx.EVT_BUTTON, lambda e: wx.MessageBox("Enviando a impresora...", "Imprimir"))
        
        btn_cerrar = wx.Button(panel, label="Cerrar")
        btn_cerrar.Bind(wx.EVT_BUTTON, lambda e: dlg.EndModal(wx.ID_OK))
        
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(btn_imprimir, 0, wx.ALL, 5)
        btn_sizer.Add(btn_cerrar, 0, wx.ALL, 5)
        
        sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 10)
        
        dlg.ShowModal()
        dlg.Destroy()

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
    frame = PedidoFrame()
    app.MainLoop()
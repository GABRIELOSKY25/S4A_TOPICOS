import wx
import mysql.connector
from datetime import datetime
import textwrap

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

        # Calcular existencia disponible (restando lo ya agregado)
        cantidad_ya_agregada = sum([item[3] for item in self.detalle_venta if item[0] == codigo])
        existencia_disponible = existencia_total - cantidad_ya_agregada

        if existencia_disponible <= 0:
            wx.MessageBox(f"No hay suficiente existencia de '{nombre}'. Existencia total: {existencia_total}, ya agregados: {cantidad_ya_agregada}", "Advertencia", wx.OK | wx.ICON_WARNING)
            return

        cantidad = wx.GetNumberFromUser(
            f"Ingrese cantidad para '{nombre}'\n(Disponible: {existencia_disponible})", 
            "Cantidad:", 
            "Cantidad", 
            1, 1, existencia_disponible)
        
        if cantidad <= 0:
            return

        # Verificar si el producto ya está en el detalle
        producto_existente = next((item for item in self.detalle_venta if item[0] == codigo), None)
        
        if producto_existente:
            # Actualizar cantidad y subtotal
            idx = self.detalle_venta.index(producto_existente)
            nueva_cantidad = producto_existente[3] + cantidad
            nuevo_subtotal = nueva_cantidad * precio
            
            # Actualizar lista detalle
            for i in range(self.lst_detalle.GetItemCount()):
                if self.lst_detalle.GetItem(i, 0).GetText() == nombre:
                    self.lst_detalle.SetItem(i, 1, str(nueva_cantidad))
                    self.lst_detalle.SetItem(i, 2, f"{nuevo_subtotal:.2f}")
                    break
            
            # Actualizar detalle_venta
            self.detalle_venta[idx] = (codigo, nombre, precio, nueva_cantidad, nuevo_subtotal)
        else:
            # Agregar nuevo producto
            subtotal = precio * cantidad
            index_detalle = self.lst_detalle.InsertItem(self.lst_detalle.GetItemCount(), nombre)
            self.lst_detalle.SetItem(index_detalle, 1, str(cantidad))
            self.lst_detalle.SetItem(index_detalle, 2, f"{subtotal:.2f}")
            self.detalle_venta.append((codigo, nombre, precio, cantidad, subtotal))

        # Actualizar total
        self.total = sum(item[4] for item in self.detalle_venta)
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
                # Agregar el producto
                self.agregar_producto(None)
                break

        if not encontrado:
            wx.MessageBox("Producto no encontrado con ese código de barras", "Error", wx.OK | wx.ICON_ERROR)
        
        # Limpiar y regresar el foco al campo de código de barras
        self.txt_codigo_barras.SetValue("")
        self.txt_codigo_barras.SetFocus()

    def guardar_venta(self, event):
        idCliente = self.txt_idCliente.GetValue()
        idCodigo = self.txt_idCodigo.GetValue()
        idEmpleado = self.txt_idEmpleado.GetValue()

        if not (idCliente and idCodigo and idEmpleado and self.detalle_venta):
            wx.MessageBox("Complete todos los campos y agregue productos", "Error", wx.OK | wx.ICON_ERROR)
            return

        # Mostrar diálogo para ingresar el pago
        dlg = wx.TextEntryDialog(self, f"Ingrese el monto con el que paga el cliente (Total: ${self.total:.2f})", "Pago")
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
            fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("SELECT MAX(idVenta) + 1 AS nuevo_id FROM Venta")
            result = cursor.fetchone()
            idVenta = result["nuevo_id"] if result["nuevo_id"] is not None else 1

            # Obtener información del cliente, empleado y membresía para el ticket
            cursor.execute("SELECT Nombre FROM Cliente WHERE idCliente = %s", (idCliente,))
            cliente = cursor.fetchone()
            nombre_cliente = cliente["Nombre"] if cliente else "Cliente no encontrado"

            cursor.execute("SELECT Nombre FROM Empleado WHERE idEmpleado = %s", (idEmpleado,))
            empleado = cursor.fetchone()
            nombre_empleado = empleado["Nombre"] if empleado else "Empleado no encontrado"

            cursor.execute("SELECT Tipo FROM Membresia WHERE idCodigo = %s", (idCodigo,))
            membresia = cursor.fetchone()
            tipo_membresia = membresia["Tipo"] if membresia else "Membresía no encontrada"

            # Verificar que todos los valores necesarios estén presentes
            if None in (idVenta, idCliente, idCodigo, idEmpleado, self.total, pago, cambio, fecha_hora):
                raise ValueError("Uno o más valores requeridos para la venta son nulos")

            # INSERT con todos los campos necesarios
            query = """
                INSERT INTO Venta (idVenta, idCliente, idCodigo, idEmpleado, Importe, Pago, Cambio, Fecha_Hora)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (idVenta, idCliente, idCodigo, idEmpleado, self.total, pago, cambio, fecha_hora)
            
            cursor.execute(query, params)

            for codigo, nombre, precio, cantidad, subtotal in self.detalle_venta:
                cursor.execute("""
                    INSERT INTO Detalles_Venta (idVenta, idCodigo_Barra, Cantidad, Subtotal, Precio_Unitario)
                    VALUES (%s, %s, %s, %s, %s)
                """, (idVenta, codigo, cantidad, subtotal, precio))

                cursor.execute("""
                    UPDATE Articulo SET Existencia = Existencia - %s WHERE idCodigo_Barra = %s
                """, (cantidad, codigo))

            conexion.commit()

            self.generar_ticket(idVenta, fecha_hora, nombre_cliente, nombre_empleado, tipo_membresia, pago, cambio)
            self.limpiar_pantalla()

        except Exception as e:
            conexion.rollback()
            wx.MessageBox(f"Error al guardar venta:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)
        finally:
            dlg.Destroy()


    def generar_ticket(self, id_venta, fecha_hora, nombre_cliente, nombre_empleado, tipo_membresia, pago, cambio):
        # Crear el contenido del ticket
        ticket = f"""
        {'COSTCO'.center(50)}
        {'Punto de Venta'.center(50)}
        {'\n'.join(textwrap.wrap('Av. de los Insurgentes Sur 1800, Florida, 01030 Ciudad de México, CDMX', width=50))}
        {'\n'.join(textwrap.wrap('Tel: 55 5261 9100', width=50))}
        
        {'='*50}
        Fecha: {fecha_hora.split()[0]}
        Hora: {fecha_hora.split()[1]}
        Venta: #{id_venta}
        {'='*50}
        Cliente: {nombre_cliente}
        Membresía: {tipo_membresia}
        Atendido por: {nombre_empleado}
        {'='*50}
        PRODUCTOS:
        """
        
        for item in self.detalle_venta:
            producto_line = f"{item[1]} x{item[3]} @${item[2]:.2f}"
            subtotal_line = f"${item[4]:.2f}".rjust(50 - len(producto_line))
            ticket += f"\n{producto_line}{subtotal_line}"
        
        ticket += f"""
        {'='*50}
        {'TOTAL:'.ljust(40)} ${self.total:.2f}
        {'PAGO:'.ljust(40)} ${pago:.2f}
        {'CAMBIO:'.ljust(40)} ${cambio:.2f}
        {'='*50}
        {'¡GRACIAS POR SU COMPRA!'.center(50)}
        {'Vuelva pronto'.center(50)}
        """
        
        # Mostrar el ticket en un diálogo
        dlg = wx.Dialog(self, title="Ticket de Venta", size=(600, 700))
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
# Gabriel Flores Urbina
# https://github.com/GABRIELOSKY25/S4A_TOPICOS

import wx
import mysql.connector
import textwrap
from datetime import datetime
from mysql.connector import Error

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
        super().__init__(None, title="Punto de Venta COSTCO", size=(1005, 620))
        self.parent_frame = parent_frame  
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

        wx.StaticText(panel, label="Código Membresía:", pos=(190, 420))
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
        wx.Button(panel, label="Eliminar", pos=(10, 535), size=(100, 30)).Bind(wx.EVT_BUTTON, self.eliminar_producto)  # Nuevo botón
        wx.Button(panel, label="Guardar Venta", pos=(120, 500), size=(120, 30)).Bind(wx.EVT_BUTTON, self.guardar_venta)
        wx.Button(panel, label="Consultar Clientes", pos=(250, 500), size=(150, 30)).Bind(wx.EVT_BUTTON, self.leer_cliente)
        wx.Button(panel, label="Consultar Empleado", pos=(410, 500), size=(150, 30)).Bind(wx.EVT_BUTTON, self.leer_empleado)
        wx.Button(panel, label="Consultar Membresia", pos=(570, 500), size=(150, 30)).Bind(wx.EVT_BUTTON, self.leer_membresia)
        wx.Button(panel, label="Regresar al menu", pos=(849, 500), size=(134, 30)).Bind(wx.EVT_BUTTON, self.regresar_menu)

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

        producto_existente = next((item for item in self.detalle_venta if item[0] == codigo), None)
        
        if producto_existente:
            idx = self.detalle_venta.index(producto_existente)
            nueva_cantidad = producto_existente[3] + cantidad
            nuevo_subtotal = nueva_cantidad * precio

            for i in range(self.lst_detalle.GetItemCount()):
                if self.lst_detalle.GetItem(i, 0).GetText() == nombre:
                    self.lst_detalle.SetItem(i, 1, str(nueva_cantidad))
                    self.lst_detalle.SetItem(i, 2, f"{nuevo_subtotal:.2f}")
                    break

            self.detalle_venta[idx] = (codigo, nombre, precio, nueva_cantidad, nuevo_subtotal)
        else:
            subtotal = precio * cantidad
            index_detalle = self.lst_detalle.InsertItem(self.lst_detalle.GetItemCount(), nombre)
            self.lst_detalle.SetItem(index_detalle, 1, str(cantidad))
            self.lst_detalle.SetItem(index_detalle, 2, f"{subtotal:.2f}")
            self.detalle_venta.append((codigo, nombre, precio, cantidad, subtotal))

        self.total = sum(item[4] for item in self.detalle_venta)
        self.txt_total.SetValue(f"{self.total:.2f}")

    def eliminar_producto(self, event):
        """Elimina el producto seleccionado del detalle de venta, permitiendo seleccionar cantidad a eliminar"""
        index = self.lst_detalle.GetFirstSelected()
        if index == -1:
            wx.MessageBox("Seleccione un producto del detalle para eliminar", "Advertencia", wx.OK | wx.ICON_WARNING)
            return

        nombre_producto = self.lst_detalle.GetItem(index, 0).GetText()
        cantidad_actual = int(self.lst_detalle.GetItem(index, 1).GetText())
        precio_unitario = float(self.detalle_venta[index][2])  

        cantidad = wx.GetNumberFromUser(
            f"Ingrese cantidad a eliminar de '{nombre_producto}'\n(En detalle: {cantidad_actual})", 
            "Cantidad a eliminar:", 
            "Eliminar Producto", 
            1, 1, cantidad_actual)
        
        if cantidad <= 0:
            return 

        producto = self.detalle_venta[index]
        
        if cantidad == cantidad_actual:
            self.lst_detalle.DeleteItem(index)
            self.detalle_venta.pop(index)
        else:
            nueva_cantidad = cantidad_actual - cantidad
            nuevo_subtotal = nueva_cantidad * precio_unitario
            
            self.lst_detalle.SetItem(index, 1, str(nueva_cantidad))
            self.lst_detalle.SetItem(index, 2, f"{nuevo_subtotal:.2f}")
            
            self.detalle_venta[index] = (
                producto[0],  
                producto[1],  
                producto[2],  
                nueva_cantidad,
                nuevo_subtotal
            )

        self.total = sum(item[4] for item in self.detalle_venta)
        self.txt_total.SetValue(f"{self.total:.2f}")
        
        self.cargar_productos()

    def on_codigo_barras(self, event):
        codigo = self.txt_codigo_barras.GetValue().strip()

        self.txt_codigo_barras.SetValue("")
        
        if not codigo:
            return
        
        wx.CallLater(100, self.procesar_codigo_barras, codigo)

    def procesar_codigo_barras(self, codigo):
        """Procesa el código de barras después de un pequeño retraso"""
        encontrado = False
        
        for i in range(self.lst_productos.GetItemCount()):
            item_codigo = self.lst_productos.GetItem(i, 0).GetText()
            if item_codigo == codigo:
                self.lst_productos.Select(i)
                self.lst_productos.Focus(i)
                encontrado = True
                
                nombre = self.lst_productos.GetItem(i, 1).GetText()
                precio = float(self.lst_productos.GetItem(i, 2).GetText())
                existencia_total = int(self.lst_productos.GetItem(i, 3).GetText())

                cantidad_ya_agregada = sum([item[3] for item in self.detalle_venta if item[0] == codigo])
                existencia_disponible = existencia_total - cantidad_ya_agregada

                if existencia_disponible <= 0:
                    wx.MessageBox(f"No hay suficiente existencia de '{nombre}'. Existencia total: {existencia_total}, ya agregados: {cantidad_ya_agregada}", 
                                "Advertencia", wx.OK | wx.ICON_WARNING)
                    return

                cantidad = wx.GetNumberFromUser(
                    f"Ingrese cantidad para '{nombre}'\n(Disponible: {existencia_disponible})", 
                    "Cantidad:", 
                    "Cantidad", 
                    1, 1, existencia_disponible)
                
                if cantidad <= 0:
                    return

                producto_existente = next((item for item in self.detalle_venta if item[0] == codigo), None)
                
                if producto_existente:
                    idx = self.detalle_venta.index(producto_existente)
                    nueva_cantidad = producto_existente[3] + cantidad
                    nuevo_subtotal = nueva_cantidad * precio
                    
                    for j in range(self.lst_detalle.GetItemCount()):
                        if self.lst_detalle.GetItem(j, 0).GetText() == nombre:
                            self.lst_detalle.SetItem(j, 1, str(nueva_cantidad))
                            self.lst_detalle.SetItem(j, 2, f"{nuevo_subtotal:.2f}")
                            break
                    
                    self.detalle_venta[idx] = (codigo, nombre, precio, nueva_cantidad, nuevo_subtotal)
                else:
                    subtotal = precio * cantidad
                    index_detalle = self.lst_detalle.InsertItem(self.lst_detalle.GetItemCount(), nombre)
                    self.lst_detalle.SetItem(index_detalle, 1, str(cantidad))
                    self.lst_detalle.SetItem(index_detalle, 2, f"{subtotal:.2f}")
                    self.detalle_venta.append((codigo, nombre, precio, cantidad, subtotal))

                self.total = sum(item[4] for item in self.detalle_venta)
                self.txt_total.SetValue(f"{self.total:.2f}")
                
                break

        if not encontrado:
            wx.MessageBox("Producto no encontrado con ese código de barras", "Error", wx.OK | wx.ICON_ERROR)
        
        self.txt_codigo_barras.SetFocus()

    def guardar_venta(self, event):
        idCliente = self.txt_idCliente.GetValue()
        idCodigo = self.txt_idCodigo.GetValue()
        idEmpleado = self.txt_idEmpleado.GetValue()

        if not (idCliente and idCodigo and idEmpleado and self.detalle_venta):
            wx.MessageBox("Complete todos los campos y agregue productos", "Error", wx.OK | wx.ICON_ERROR)
            return

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

            cursor.execute("SELECT Nombre FROM Cliente WHERE idCliente = %s", (idCliente,))
            cliente = cursor.fetchone()
            nombre_cliente = cliente["Nombre"] if cliente else "Cliente no encontrado"

            cursor.execute("SELECT Nombre FROM Empleado WHERE idEmpleado = %s", (idEmpleado,))
            empleado = cursor.fetchone()
            nombre_empleado = empleado["Nombre"] if empleado else "Empleado no encontrado"

            cursor.execute("SELECT Tipo FROM Membresia WHERE idCodigo = %s", (idCodigo,))
            membresia = cursor.fetchone()
            tipo_membresia = membresia["Tipo"] if membresia else "Membresía no encontrada"

            if None in (idVenta, idCliente, idCodigo, idEmpleado, self.total, pago, cambio, fecha_hora):
                raise ValueError("Uno o más valores requeridos para la venta son nulos")

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

    def leer_cliente(self, event):
        try:
            query = "SELECT idCliente, idCodigo, Nombre, Apellidos, Edad, Correo, Telefono, Direccion FROM cliente"
            cursor.execute(query)
            resultados = cursor.fetchall()

            if resultados:
                ventana_emergente = wx.Frame(None, title="Listado de Clientes", size=(1100, 600))
                panel = wx.Panel(ventana_emergente)

                titulo = wx.StaticText(panel, label="Listado de Clientes", pos=(400, 15))
                titulo.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))

                list_ctrl = wx.ListCtrl(panel, pos=(10, 50), size=(1060, 500), 
                                    style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
                
                columnas = [
                    ("ID Cliente", 100),
                    ("Código", 100),
                    ("Nombre", 150),
                    ("Apellidos", 150),
                    ("Edad", 80),
                    ("Correo", 200),
                    ("Teléfono", 120),
                    ("Dirección", 200)
                ]
                
                for i, (col_name, col_width) in enumerate(columnas):
                    list_ctrl.InsertColumn(i, col_name, width=col_width)
                
                for cliente in resultados:
                    id_cliente = str(cliente["idCliente"])
                    codigo = str(cliente["idCodigo"])
                    nombre = str(cliente["Nombre"])
                    apellidos = str(cliente["Apellidos"])
                    edad = str(cliente["Edad"]) if cliente["Edad"] is not None else ""
                    correo = str(cliente["Correo"]) if cliente["Correo"] is not None else ""
                    telefono = str(cliente["Telefono"]) if cliente["Telefono"] is not None else ""
                    direccion = str(cliente["Direccion"]) if cliente["Direccion"] is not None else ""

                    index = list_ctrl.InsertItem(list_ctrl.GetItemCount(), id_cliente)
                    list_ctrl.SetItem(index, 1, codigo)
                    list_ctrl.SetItem(index, 2, nombre)
                    list_ctrl.SetItem(index, 3, apellidos)
                    list_ctrl.SetItem(index, 4, edad)
                    list_ctrl.SetItem(index, 5, correo)
                    list_ctrl.SetItem(index, 6, telefono)
                    list_ctrl.SetItem(index, 7, direccion)
                    
                    if index % 2 == 0:
                        list_ctrl.SetItemBackgroundColour(index, wx.Colour(240, 240, 240))
                    else:
                        list_ctrl.SetItemBackgroundColour(index, wx.WHITE)
                
                ventana_emergente.Show()
            else:
                wx.MessageBox("No hay clientes registrados", "Información", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al consultar clientes: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def leer_empleado(self, event):
        try:
            query = "SELECT idEmpleado, Nombre, Apellido, Puesto, Salario FROM empleado"
            cursor.execute(query)
            resultados = cursor.fetchall()

            if resultados:
                ventana_emergente = wx.Frame(None, title="Listado de Empleados", size=(900, 600))
                panel = wx.Panel(ventana_emergente)
                
                titulo = wx.StaticText(panel, label="Listado de Empleados", pos=(350, 15))
                titulo.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))

                list_ctrl = wx.ListCtrl(panel, pos=(20, 50), size=(850, 500),
                                    style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
                
                columnas = [
                    ("ID", 80),
                    ("Nombre", 200),
                    ("Apellido", 200),
                    ("Puesto", 200),
                    ("Salario", 150)
                ]
                
                for i, (col_name, col_width) in enumerate(columnas):
                    list_ctrl.InsertColumn(i, col_name, width=col_width)

                for empleado in resultados:
                    index = list_ctrl.InsertItem(list_ctrl.GetItemCount(), str(empleado["idEmpleado"]))
                    
                    list_ctrl.SetItem(index, 1, empleado["Nombre"])
                    list_ctrl.SetItem(index, 2, empleado["Apellido"])
                    list_ctrl.SetItem(index, 3, empleado["Puesto"])

                    salario_formateado = f"${float(empleado['Salario']):,.2f}"
                    list_ctrl.SetItem(index, 4, salario_formateado)

                    list_ctrl.SetItemBackgroundColour(index, wx.WHITE)
                
                list_ctrl.SetBackgroundColour(wx.WHITE)
                list_ctrl.SetForegroundColour(wx.BLACK)

                for i in range(list_ctrl.GetItemCount()):
                    list_ctrl.SetItemState(i, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
                
                ventana_emergente.Show()
            else:
                wx.MessageBox("No hay empleados registrados", "Información", wx.OK | wx.ICON_INFORMATION)

        except Error as e:
            wx.MessageBox(f"Error al consultar empleados: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def leer_membresia(self, event):
        try:
            query = "SELECT idCodigo, Fecha_Activacion, Fecha_Vigencia, Tipo FROM membresia"
            cursor.execute(query)
            resultados = cursor.fetchall()

            if resultados:
                ventana_emergente = wx.Frame(None, title="Listado de Membresías", size=(900, 600))
                panel = wx.Panel(ventana_emergente)
                
                titulo = wx.StaticText(panel, label="Listado de Membresías", pos=(350, 15))
                titulo.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))

                list_ctrl = wx.ListCtrl(panel, pos=(20, 50), size=(850, 500),
                                    style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
                
                columnas = [
                    ("Código", 150),
                    ("Fecha Activación", 200),
                    ("Fecha Vigencia", 200),
                    ("Tipo", 250)
                ]
                
                for i, (col_name, col_width) in enumerate(columnas):
                    list_ctrl.InsertColumn(i, col_name, width=col_width)
                
                for membresia in resultados:
                    index = list_ctrl.InsertItem(list_ctrl.GetItemCount(), str(membresia["idCodigo"]))

                    fecha_activacion = str(membresia["Fecha_Activacion"]).split()[0] if membresia["Fecha_Activacion"] else ""
                    fecha_vigencia = str(membresia["Fecha_Vigencia"]).split()[0] if membresia["Fecha_Vigencia"] else ""
                    

                    list_ctrl.SetItem(index, 1, fecha_activacion)
                    list_ctrl.SetItem(index, 2, fecha_vigencia)
                    list_ctrl.SetItem(index, 3, str(membresia["Tipo"]))
                    
                    list_ctrl.SetItemBackgroundColour(index, wx.WHITE)
                
                list_ctrl.SetBackgroundColour(wx.WHITE)
                list_ctrl.SetForegroundColour(wx.BLACK)
                
                for i in range(list_ctrl.GetItemCount()):
                    list_ctrl.SetItemState(i, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
                
                ventana_emergente.Show()
            else:
                wx.MessageBox("No hay membresías registradas", "Información", wx.OK | wx.ICON_INFORMATION)

        except Error as ex:
            wx.MessageBox(f"Error al consultar membresías: {ex}", "Error", wx.OK | wx.ICON_ERROR)

    def regresar_menu(self, event):
        """Regresa al menú principal"""
        if self.parent_frame:
            self.parent_frame.Show()  
        self.Close()  

    def on_close(self, event):
        """Maneja el evento cuando se cierra la ventana"""
        if self.parent_frame:
            self.parent_frame.Show()  
        self.Destroy()

if __name__ == "__main__":
    app = wx.App(False)
    frame = PuntoVenta()
    app.MainLoop()
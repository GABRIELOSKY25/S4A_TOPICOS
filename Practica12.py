# Gabriel Flores Urbina

#https://github.com/GABRIELOSKY25/S4A_TOPICOS

import wx

Menu = wx.App()

def Membresia():
    # Crear ventana de membresia 
    ventana = wx.Frame(None, title='Membresía', size=(500, 370))

    # Crear espacio para trabajar en la ventana membresia 
    panel = wx.Panel(ventana)

    # Título
    titulo = wx.StaticText(panel, label = "Membresías", pos = (180, 30))
    letra_titualo = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    titulo.SetFont(letra_titualo)

    # Campos de membresia 
    idNombre = wx.StaticText(panel, label = "idNombre: ", pos = (30, 80))
    txt_idNombre = wx.TextCtrl(panel, pos = (140, 76), size = (200, -1))
    txt_idNombre.SetBackgroundColour(wx.Colour(254, 241, 147))
    letra_idNombre = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    idNombre.SetFont(letra_idNombre)

    Fecha_Activacion = wx.StaticText(panel, label = "Fecha Activacion: ", pos = (30, 120))
    txt_Fecha_Activacion = wx.TextCtrl(panel, pos = (140, 116), size = (200, -1))
    txt_Fecha_Activacion.SetBackgroundColour(wx.Colour(181, 242, 248))
    letra_Fecha_Activacion = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    Fecha_Activacion.SetFont(letra_Fecha_Activacion)

    Fecha_Vigencia = wx.StaticText(panel, label = "Fecha_Vigencia: ", pos = (30, 160))
    txt_Fecha_Vigencia = wx.TextCtrl(panel, pos = (140, 156), size = (200, -1))
    txt_Fecha_Vigencia.SetBackgroundColour(wx.Colour(181, 242, 248))
    letra_Fecha_Vigencia = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    Fecha_Vigencia.SetFont(letra_Fecha_Vigencia)

    Tipo = wx.StaticText(panel, label = "Tipo: ", pos = (30, 200))
    Opciones = ["Ejecutiva", "Dorada"]
    txt_Opciones = wx.ComboBox(panel, pos = (140, 196), size = (200, -1), choices = Opciones, style=wx.CB_DROPDOWN)
    txt_Opciones.SetBackgroundColour(wx.Colour(181, 242, 248))
    letra_Tipo = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    Tipo.SetFont(letra_Tipo)

    # Botón de membresia
    boton_Eliminar = wx.Button(panel, label = "Eliminar", pos = (70, 260), size = (100, 30))
    boton_Guardar = wx.Button(panel, label = "Guardar", pos = (190, 260), size = (100, 30))
    boton_Actualizar = wx.Button(panel, label = "Actualizar", pos=(310, 260), size = (100, 30))

    ventana.Show()

def Cliente():
     # Crear ventana de Cliente 
    ventana = wx.Frame(None, title='Cliente', size=(500, 525))

    # Crear espacio para trabajar en la ventana Cliente
    panel = wx.Panel(ventana)

    # Título
    titulo = wx.StaticText(panel, label = "Clientes", pos = (195, 30))
    letra_titualo = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    titulo.SetFont(letra_titualo)

    # Campos de Clientes
    idCliente = wx.StaticText(panel, label = "idCliente: ", pos = (60, 80))
    txt_idCliente = wx.TextCtrl(panel, pos = (140, 76), size = (200, -1))
    txt_idCliente.SetBackgroundColour(wx.Colour(254, 241, 147))
    letra_idCliente = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    idCliente.SetFont(letra_idCliente)

    idCodigo = wx.StaticText(panel, label = "idCodigo: ", pos = (60, 120))
    txt_idCodigo = wx.TextCtrl(panel, pos = (140, 116), size = (200, -1))
    txt_idCodigo.SetBackgroundColour(wx.Colour(181, 242, 248))
    letra_idCodigo = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    idCodigo.SetFont(letra_idCodigo)

    Nombre = wx.StaticText(panel, label = "Nombre: ", pos = (60, 160))
    txt_Nombre = wx.TextCtrl(panel, pos = (140, 156), size = (200, -1))
    txt_Nombre.SetBackgroundColour(wx.Colour(181, 242, 248))
    letra_Nombre = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    Nombre.SetFont(letra_Nombre)

    Apellidos = wx.StaticText(panel, label = "Apellidos: ", pos = (60, 200))
    txt_Apellidos = wx.TextCtrl(panel, pos = (140, 196), size = (200, -1))
    txt_Apellidos.SetBackgroundColour(wx.Colour(210, 255, 254))
    letra_Apellidos = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    Apellidos.SetFont(letra_Apellidos)
    
    Edad = wx.StaticText(panel, label = "Edad: ", pos = (60, 240))
    txt_Edad = wx.TextCtrl(panel, pos = (140, 236), size = (200, -1))
    txt_Edad.SetBackgroundColour(wx.Colour(210, 255, 254))
    letra_Edad = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    Edad.SetFont(letra_Edad)

    Correo = wx.StaticText(panel, label = "Correo: ", pos = (60, 280))
    txt_Correo = wx.TextCtrl(panel, pos = (140, 276), size = (200, -1))
    txt_Correo.SetBackgroundColour(wx.Colour(181, 242, 248))
    letra_Correo = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    Correo.SetFont(letra_Correo)

    Telefono = wx.StaticText(panel, label = "Telefono: ", pos = (60, 320))
    txt_Telefono = wx.TextCtrl(panel, pos = (140, 316), size = (200, -1))
    txt_Telefono.SetBackgroundColour(wx.Colour(181, 242, 248))
    letra_Telefono = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    Telefono.SetFont(letra_Telefono)

    Direccion = wx.StaticText(panel, label = "Direccion: ", pos = (60, 360))
    txt_Direccion = wx.TextCtrl(panel, pos = (140, 356), size = (200, -1))
    txt_Direccion.SetBackgroundColour(wx.Colour(181, 242, 248))
    letra_Direccion = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    Direccion.SetFont(letra_Direccion)


    # Botón de clientes
    boton_Eliminar = wx.Button(panel, label = "Eliminar", pos = (70, 420), size = (100, 30))
    boton_Guardar = wx.Button(panel, label = "Guardar", pos = (190, 420), size = (100, 30))
    boton_Actualizar = wx.Button(panel, label = "Actualizar", pos=(310, 420), size = (100, 30))

    ventana.Show()

def Empleado():
     # Crear ventana de Empleados
    ventana = wx.Frame(None, title='Empleado', size=(500, 450))

    # Crear espacio para trabajar en la ventana Empleados
    panel = wx.Panel(ventana)

    # Título
    titulo = wx.StaticText(panel, label = "Empleados", pos = (180, 30))
    letra_titualo = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    titulo.SetFont(letra_titualo)

    # Campos de Empleados
    idEmpleado = wx.StaticText(panel, label = "idEmpleado: ", pos = (60, 80))
    txt_idEmpleado = wx.TextCtrl(panel, pos = (140, 76), size = (200, -1))
    txt_idEmpleado.SetBackgroundColour(wx.Colour(254, 241, 147))
    letra_idEmpleado = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    idEmpleado.SetFont(letra_idEmpleado)

    Nombre = wx.StaticText(panel, label = "Nombre: ", pos = (60, 120))
    txt_Nombre = wx.TextCtrl(panel, pos = (140, 116), size = (200, -1))
    txt_Nombre.SetBackgroundColour(wx.Colour(181, 242, 248))
    letra_Nombre = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    Nombre.SetFont(letra_Nombre)

    Apellidos = wx.StaticText(panel, label = "Apellidos: ", pos = (60, 160))
    txt_Apellidos = wx.TextCtrl(panel, pos = (140, 156), size = (200, -1))
    txt_Apellidos.SetBackgroundColour(wx.Colour(210, 255, 254))
    letra_Apellidos = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    Apellidos.SetFont(letra_Apellidos)
    
    Edad = wx.StaticText(panel, label = "Edad: ", pos = (60, 200))
    txt_Edad = wx.TextCtrl(panel, pos = (140, 196), size = (200, -1))
    txt_Edad.SetBackgroundColour(wx.Colour(210, 255, 254))
    letra_Edad = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    Edad.SetFont(letra_Edad)

    Puesto = wx.StaticText(panel, label = "Puesto: ", pos = (60, 240))
    txt_Puesto = wx.TextCtrl(panel, pos = (140, 236), size = (200, -1))
    txt_Puesto.SetBackgroundColour(wx.Colour(181, 242, 248))
    letra_Puesto = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    Puesto.SetFont(letra_Puesto)

    Salario = wx.StaticText(panel, label = "Salario: ", pos = (60, 280))
    txt_Salario = wx.TextCtrl(panel, pos = (140, 276), size = (200, -1))
    txt_Salario.SetBackgroundColour(wx.Colour(181, 242, 248))
    letra_Salario = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    Salario.SetFont(letra_Salario)

    # Botón de Empleados
    boton_Eliminar = wx.Button(panel, label = "Eliminar", pos = (70, 340), size = (100, 30))
    boton_Guardar = wx.Button(panel, label = "Guardar", pos = (190, 340), size = (100, 30))
    boton_Actualizar = wx.Button(panel, label = "Actualizar", pos=(310, 340), size = (100, 30))

    ventana.Show()

def Categoria():
    # Crear ventana de Categoria
    ventana = wx.Frame(None, title='Categoria', size=(500, 290))

    # Crear espacio para trabajar en la ventana Categorias
    panel = wx.Panel(ventana)

    # Título
    titulo = wx.StaticText(panel, label = "Categoias", pos = (187, 30))
    letra_titualo = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    titulo.SetFont(letra_titualo)

    # Campos de Catgorias
    idCategoria = wx.StaticText(panel, label = "idCategoria: ", pos = (60, 80))
    txt_idCategoria = wx.TextCtrl(panel, pos = (140, 76), size = (200, -1))
    txt_idCategoria.SetBackgroundColour(wx.Colour(254, 241, 147))
    letra_idCategoria = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    idCategoria.SetFont(letra_idCategoria)

    Nombre = wx.StaticText(panel, label = "Nombre: ", pos = (60, 120))
    txt_Nombre = wx.TextCtrl(panel, pos = (140, 116), size = (200, -1))
    txt_Nombre.SetBackgroundColour(wx.Colour(181, 242, 248))
    letra_Nombre = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    Nombre.SetFont(letra_Nombre)

    # Botón de Categorias
    boton_Eliminar = wx.Button(panel, label = "Eliminar", pos = (70, 180), size = (100, 30))
    boton_Guardar = wx.Button(panel, label = "Guardar", pos = (190, 180), size = (100, 30))
    boton_Actualizar = wx.Button(panel, label = "Actualizar", pos=(310, 180), size = (100, 30))

    ventana.Show()

def Historial_Precio():
    # Crear ventana de Historial Precio
    ventana = wx.Frame(None, title='Historial Precio', size=(500, 370))

    # Crear espacio para trabajar en la ventana Historial Precio 
    panel = wx.Panel(ventana)

    # Título
    titulo = wx.StaticText(panel, label = "Historial Precios", pos = (159, 30))
    letra_titualo = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    titulo.SetFont(letra_titualo)

    # Campos de Historial Precios
    idHistorial_Precio = wx.StaticText(panel, label = " idHistorial Precio: ", pos = (30, 80))
    txt_idHistorial_Precio = wx.TextCtrl(panel, pos = (140, 76), size = (200, -1))
    txt_idHistorial_Precio.SetBackgroundColour(wx.Colour(254, 241, 147))
    letra_idHistorial_Precio = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    idHistorial_Precio.SetFont(letra_idHistorial_Precio)

    Precio_Anterior = wx.StaticText(panel, label = "Precio Anterior: ", pos = (30, 120))
    txt_Precio_Anterior = wx.TextCtrl(panel, pos = (140, 116), size = (200, -1))
    txt_Precio_Anterior.SetBackgroundColour(wx.Colour(181, 242, 248))
    letra_Precio_Anterior = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    Precio_Anterior.SetFont(letra_Precio_Anterior)

    Precio_Nuevo = wx.StaticText(panel, label = "Precio Nuevo: ", pos = (30, 160))
    txt_Precio_Nuevo = wx.TextCtrl(panel, pos = (140, 156), size = (200, -1))
    txt_Precio_Nuevo.SetBackgroundColour(wx.Colour(181, 242, 248))
    letra_Precio_Nuevo = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    Precio_Nuevo.SetFont(letra_Precio_Nuevo)

    Fecha_Cambio = wx.StaticText(panel, label = "Fecha Cambio: ", pos = (30, 200))
    txt_Fecha_Cambio = wx.TextCtrl(panel, pos = (140, 196), size = (200, -1))
    txt_Fecha_Cambio.SetBackgroundColour(wx.Colour(210, 255, 254))
    letra_Fecha_Cambio = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    Fecha_Cambio.SetFont(letra_Fecha_Cambio)

    # Botón de Historial Precios
    boton_Eliminar = wx.Button(panel, label = "Eliminar", pos = (70, 260), size = (100, 30))
    boton_Guardar = wx.Button(panel, label = "Guardar", pos = (190, 260), size = (100, 30))
    boton_Actualizar = wx.Button(panel, label = "Actualizar", pos=(310, 260), size = (100, 30))

    ventana.Show()

def Proveedor():
    # Crear ventana de Proveedor
    ventana = wx.Frame(None, title='Proveedor', size=(500, 415))

    # Crear espacio para trabajar en la ventana Proveedores
    panel = wx.Panel(ventana)

    # Título
    titulo = wx.StaticText(panel, label = "Proveedor", pos = (180, 30))
    letra_titualo = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    titulo.SetFont(letra_titualo)

    # Campos de Proveedores
    idProveedor = wx.StaticText(panel, label = "idProveedor: ", pos = (60, 80))
    txt_idProveedor = wx.TextCtrl(panel, pos = (140, 76), size = (200, -1))
    txt_idProveedor.SetBackgroundColour(wx.Colour(254, 241, 147))
    letra_idProveedor = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    idProveedor.SetFont(letra_idProveedor)

    Nombre = wx.StaticText(panel, label = "Nombre: ", pos = (60, 120))
    txt_Nombre = wx.TextCtrl(panel, pos = (140, 116), size = (200, -1))
    txt_Nombre.SetBackgroundColour(wx.Colour(181, 242, 248))
    letra_Nombre = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    Nombre.SetFont(letra_Nombre)

    Apellidos = wx.StaticText(panel, label = "Apellidos: ", pos = (60, 160))
    txt_Apellidos = wx.TextCtrl(panel, pos = (140, 156), size = (200, -1))
    txt_Apellidos.SetBackgroundColour(wx.Colour(210, 255, 254))
    letra_Apellidos = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    Apellidos.SetFont(letra_Apellidos)
    
    Telefono = wx.StaticText(panel, label = "Telefono: ", pos = (60, 200))
    txt_Telefono = wx.TextCtrl(panel, pos = (140, 196), size = (200, -1))
    txt_Telefono.SetBackgroundColour(wx.Colour(210, 255, 254))
    letra_Telefono = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    Telefono.SetFont(letra_Telefono)

    Direccion = wx.StaticText(panel, label = "Direccion: ", pos = (60, 240))
    txt_Direccion = wx.TextCtrl(panel, pos = (140, 236), size = (200, -1))
    txt_Direccion.SetBackgroundColour(wx.Colour(181, 242, 248))
    letra_Direccion = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    Direccion.SetFont(letra_Direccion)

    # Botón de Proveedores
    boton_Eliminar = wx.Button(panel, label = "Eliminar", pos = (70, 300), size = (100, 30))
    boton_Guardar = wx.Button(panel, label = "Guardar", pos = (190, 300), size = (100, 30))
    boton_Actualizar = wx.Button(panel, label = "Actualizar", pos=(310, 300), size = (100, 30))

    ventana.Show()

Membresia()
Cliente()
Empleado()
Categoria()
Historial_Precio()
Proveedor()

Menu.MainLoop()
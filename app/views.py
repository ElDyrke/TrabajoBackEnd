from django.shortcuts import render, redirect
from app.forms import *
from app.models import TipoUsuario, Usuario, Viaje
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password


def inicio(request):
    try:
        if request.session["usuario"]:
            viajes = Viaje.objects.all()
            return render(request, "inicio.html", {"viajes": viajes})
    except:
        try:
            if request.session["administrador"]:
                return redirect('administrador')
        except:
            return redirect('inicio_sesion')
   

def registro_usuario(request):
    if request.method == "GET":
        return render(request, "registro_usuario.html")
    elif request.method == "POST":
        rut = request.POST["rut"]
        username = request.POST["username"]
        nombre = request.POST["nombre"]
        apellido = request.POST["apellido"]
        contrasenna = make_password(request.POST["contrasenna"])
        email = request.POST["email"]
        nuevoRegistro = Usuario(username=username,
                                rut=rut,
                                nombre=nombre,
                                apellido=apellido,
                                contrasenna=contrasenna,
                                email=email,
                                tipo_usuario=TipoUsuario.objects.get(id=1))
        
        if nuevoRegistro:
            nuevoRegistro.save()
            messages.success(request, 'Registro exitoso. Por favor, inicia sesión.')
            return redirect('inicio_sesion')
        else:
            messages.error(request, 'Error en el formulario. Verifica los datos ingresados.')
            return render(request, 'registro_usuario.html')

def autenticar(usuario, rol, pswrd):
    return usuario and usuario.tipo_usuario.nombre == rol and check_password(pswrd, usuario.contrasenna)

def inicio_sesion(request):
    if request.method == "GET":
        return render(request, "inicio_sesion.html")
    
    elif request.method == "POST":
        getUsername = request.POST['username']
        getContrasenna = request.POST['contrasenna']
        #si con filter no se encuentra el username ni contrasena buscada, entonces devuelve None.
        usuario = Usuario.objects.filter(username=getUsername).first()

        # print(f"usuario: {usuario.username} {usuario.tipo_usuario.nombre}")
        # print(f"{check_password(getContrasenna, usuario.contrasenna)}")

        if autenticar(usuario, "Usuario", getContrasenna):

            request.session["usuario"] = getUsername
            print(f"El usuario {getUsername} ha iniciado sesión.")
            return redirect('cliente')
        

        elif autenticar(usuario, "Administrador", getContrasenna):
            request.session["administrador"] = getUsername
            print(f"El administrador {getUsername} ha iniciado sesión.")
            return redirect('administrador')

        else:

            error_message = "Error. Verifique que haya ingresado correctamente los datos"
            print("Error. Verifique que haya ingresado correctamente los datos")
            return render(request, "inicio_sesion.html", {"error_message": error_message})
        
def cerrar_sesion(request):
    return render(request, "cerrar_sesion.html")

def viajes_reservados(request, id):
    # si carrito_cantidad no existe, entonces se inicia en 0
    getViaje = Viaje.objects.get(id=id)

    if getViaje.stock > 0:
        cantidad = request.session.get("carrito_cantidad", 0)
        request.session["carrito_cantidad"] = cantidad + 1
        getViaje.stock = getViaje.stock - 1; 
        getViaje.save()
    #aqui se retorna un render
    return inicio(request)

def cerrar_sesion(request):
    sesion = request.session
    try:
        if sesion["username"]:
            del sesion["username"]
    except:
        if sesion["administrador"]:
            del sesion["administrador"]

    return redirect('inicio')

def cliente(request):
    username = request.session["username"]
    if username:
        return render(request, "cliente.html", {"username": username})
    else:
        redirect('inicio_sesion')

def administrador(request):
    username = request.session["administrador"]
    if username:
        return render(request, "administrador.html", {"username": username})
    else:
        redirect('inicio_sesion')

def formusuarios(request):
    if request.method == "GET":
        form = FormUsuario()
        return render(request, 'agregarUsuarios.html', {"form": form})
    elif request.method == "POST":
        form = FormUsuario(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'agregarUsuarios.html', {"form": form})
        
def formdestinos(request):
    if request.method == "GET":
        form = FormDestino()
        return render(request, 'agregarDestino.html', {"form": form})
    elif request.method == "POST":
        form = FormDestino(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'agregarDestino.html', {"form": form})
def formviajes(request):
    if request.method == "GET":
        form = FormViaje()
        return render(request, 'agregarViaje.html', {"form": form})
    elif request.method == "POST":
        form = FormViaje(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'agregarViaje.html', {"form": form})
    
def formreservas(request):
    if request.method == "GET":
        form = FormReserva()
        return render(request, 'agregarReserva.html', {"form": form})
    elif request.method == "POST":
        form = FormReserva(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'agregarReserva.html', {"form": form})
    
def formcotizaciones(request):
    if request.method == "GET":
        form = FormCotizacion()
        return render(request, 'agregarCotizacion.html', {"form": form})
    elif request.method == "POST":
        form = FormCotizacion(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'agregarCotizacion.html', {"form": form})
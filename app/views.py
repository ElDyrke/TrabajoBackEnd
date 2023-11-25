from django.shortcuts import render, redirect
from app.forms import *
from app.models import TipoUsuario, Usuario, Viaje
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache


def inicio(request):
    sesion = request.session
   
    if "administrador" in sesion:
        return redirect('administrador')
    else:
        viajes = Viaje.objects.all()
        return render(request, "cliente.html", {"viajes": viajes})
   

def registro_usuario(request):
    if request.method == "GET":
        return render(request, "registro_usuario.html")
    elif request.method == "POST":
        rut = request.POST["rut"]
        username = request.POST["username"]
        nombre = request.POST["nombre"]
        apellido = request.POST["apellido"]
        contrasenna = request.POST["contrasenna"]
        contrasenna2 = request.POST["contrasenna2"]
        email = request.POST["email"]
        if contrasenna != contrasenna2: 
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'registro_usuario.html', {"error": 'Las contraseñas no coinciden'})
        nuevoRegistro = Usuario(username=username,
                                rut=rut,
                                nombre=nombre,
                                apellido=apellido,
                                contrasenna=make_password(contrasenna),
                                email=email,
                                tipo_usuario=TipoUsuario.objects.get(id=2))
        
        if nuevoRegistro:
            nuevoRegistro.save()
            messages.success(request, 'Registro exitoso. Por favor, inicia sesión.')
            return redirect('inicio_sesion')
        else:
            messages.error(request, 'Error en el formulario. Verifica los datos ingresados.')
            return render(request, 'registro_usuario.html', {"error": 'Error en el formulario. Verifica los datos ingresados.'})

def autenticar(usuario, rol, pswrd):
    print("El tipo de usuario ingresado es:",usuario.tipo_usuario.nombre)
    return usuario and usuario.tipo_usuario.nombre == rol and check_password(pswrd,usuario.contrasenna)

def inicio_sesion(request):
    if request.method == "GET":
        return render(request, "inicio_sesion.html")
    
    elif request.method == "POST":
        getUsername = request.POST['username']
        getContrasenna = request.POST['contrasenna']
        #si con filter no se encuentra el username ni contrasena buscada, entonces devuelve None.
        usuario = Usuario.objects.filter(username=getUsername).first()

        if usuario is not None:
            if autenticar(usuario, "Cliente", getContrasenna):

                request.session["username"] = getUsername
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
        else:
            error_message = "Error. Verifique que haya ingresado correctamente los datos"
            return render(request, "inicio_sesion.html", {"error_message": error_message})

def listaUsuarios(request):
    print("lista")
    listaUsuarios = Usuario.objects.all()
    return render(request, "listaUsuarios.html", {"usuarios": listaUsuarios})

def listaDestinos(request):
    listaDestinos = Destino.objects.all()
    return render(request, "listaDestinos.html", {"destinos": listaDestinos})

def listaViajes(request):
    listaViajes = Viaje.objects.all()
    return render(request, "listaViajes.html", {"viajes": listaViajes})

def listaCotizaciones(request):
    listaCotizaciones = Cotizacion.objects.all()
    for c in listaCotizaciones:
        c.listav = c.viajes.all()
    return render(request, "listaCotizaciones.html", {"cotizaciones": listaCotizaciones})

def listaReservas(request):
    listaReservas = Reserva.objects.all()
    return render(request, "listaReservas.html", {"reservas": listaReservas})

def editarUsuarios(request,id):
    usuario = Usuario.objects.get(id=id)
    if request.method == 'GET':
        formulario = FormUsuario(instance=usuario)
        return render(request, 'editarUsuarios.html',  {"form":formulario, "id": id})
    elif request.method == 'POST':
        formulario = FormUsuario(request.POST, instance=usuario)
        if formulario.is_valid():
            formulario.save()
        return redirect('listaUsuarios')
    
def editarDestinos(request,id):
    destino = Destino.objects.get(id=id)
    if request.method == 'GET':
        formulario = FormDestino(instance=destino)

        return render(request, 'editarDestinos.html',  {"form":formulario, "id": id})
    elif request.method == 'POST':
        formulario = FormDestino(request.POST, instance=destino)
        if formulario.is_valid():
            formulario.save()
        return redirect('listaDestinos')
    
def editarViajes(request,id):
    viaje = Viaje.objects.get(id=id)
    if request.method == 'GET':
        formulario = FormViaje(instance=viaje)

        return render(request, 'editarViajes.html',  {"form":formulario, "id": id})
    elif request.method == 'POST':
        formulario = FormViaje(request.POST, instance=viaje)
        if formulario.is_valid():
            formulario.save()
        return redirect('listaViajes')


def editarCotizaciones(request,id):
    cotizacion = Cotizacion.objects.get(id=id)
    if request.method == 'GET':
        formulario = FormCotizacion(instance=cotizacion)

        return render(request, 'editarCotizaciones.html',  {"form":formulario, "id": id})
    elif request.method == 'POST':
        formulario = FormCotizacion(request.POST, instance=cotizacion)
        if formulario.is_valid():
            formulario.save()
        return redirect('listaCotizaciones')
    
def editarReservas(request,id):
    reserva = Reserva.objects.get(id=id)
    if request.method == 'GET':
        formulario = FormReserva(instance=reserva)

        return render(request, 'editarReservas.html',  {"form":formulario, "id": id})
    elif request.method == 'POST':
        formulario = FormReserva(request.POST, instance=reserva)
        if formulario.is_valid():
            formulario.save()
        return redirect('listaReservas')
    

def eliminarUsuarios(request, id):
    usuario = Usuario.objects.get(id=id)
    usuario.delete()
    listaUsuarios = Usuario.objects.all()
    return render(request, 'listaUsuarios.html', {"usuarios": listaUsuarios})

def eliminarViajes(request, id):
    viaje = Viaje.objects.get(id=id)
    viaje.delete()
    listaViajes = Viaje.objects.all()
    return render(request, 'listaViajes.html', {"viajes": listaViajes})

def eliminarDestinos(request, id):
    destino = Destino.objects.get(id=id)
    destino.delete()
    listaDestinos = Destino.objects.all()
    return render(request, 'listaDestinos.html', {"destinos": listaDestinos})

def eliminarCotizaciones(request, id):
    cotizacion = Cotizacion.objects.get(id=id)
    cotizacion.delete()
    return redirect('listaCotizaciones')

def eliminarReservas(request, id):
    reserva = Reserva.objects.get(id=id)
    viaje = reserva.viaje
    viaje.stock += 1
    viaje.save()
    reserva.delete()
    listaReservas = Reserva.objects.all()
    return render(request, 'listaReservas.html', {"reservas": listaReservas})

def viajes_reservados(request):
    reservas = Reserva.objects.all()
    sesion = request.session
    reservas_usuario = [r for r in reservas if r.usuario.username == sesion["username"] ]
    return render(request, 'viajes_reservados.html', {"reservas": reservas_usuario})

def cerrar_sesion(request):
    sesion = request.session
    try:
        if "username" in sesion:
            del sesion["username"]
            del sesion["viajes"]
        elif "administrador" in sesion:
            del sesion["administrador"]
        return redirect('inicio_sesion')
    except:
        return redirect('inicio_sesion')



def es_administrador(user):
    return user.is_authenticated and user.tipo_usuario.nombre == 'Administrador'


def cliente(request):
    viajes = Viaje.objects.all()
    print(viajes)
    context = {"viajes": viajes, "username": request.session["username"]}
    return render(request,'cliente.html', context)

def vista_viaje(request, id):
    viaje = Viaje.objects.get(id = id)
    context = {"viaje": viaje}
    return render(request, 'viaje_vista.html', context)

def add_to_cotizacion(request,id):
    viaje = Viaje.objects.get(id = id).id
    
    try:
        if viaje not in request.session["viajes"]:
            lista = request.session["viajes"]
            lista.append(viaje)
            request.session["viajes"] = lista
    except KeyError:
        request.session["viajes"] = [viaje]

    print(request.session["viajes"])

    return redirect('inicio')
    
def usuario_cotizar(request):
    viajes = []
    for id_viaje in request.session["viajes"]:
        viaje = Viaje.objects.get(id = id_viaje)
        viajes.append(viaje)
    
    if request.method == "GET":
        sesion = request.session
        if "username" not in sesion:
            return redirect('inicio_sesion')
        context = {"viajes": viajes}
        
        return render(request, 'usuario_cotizar.html', context)
    
    elif request.method == "POST":
        sesion = request.session
        usuario = Usuario.objects.get(username = sesion["username"])
        fecha_min = request.POST["fecha_min"]
        fecha_max = request.POST["fecha_max"]

        if fecha_min > fecha_max:
            context =  {"viajes": viajes, "error": "La fecha Minima no puede ser Mayor a la Máxima"}
            return render(request, 'usuario_cotizar.html', context)
        
        cotizacion = Cotizacion(usuario=usuario,
                                fecha_minima=fecha_min,
                                fecha_maxima=fecha_max)
        cotizacion.save()
        for v in viajes:
            cotizacion.viajes.add(v)
        print(cotizacion.viajes)
        cotizacion.save()
        del sesion["viajes"]
        return redirect('inicio')


def administrador(request):
    return render(request, "administrador.html", {"username": request.session["administrador"]})


def formusuarios(request):
    if request.method == "GET":
        form = FormUsuario()
        return render(request, 'agregarUsuarios.html', {"form": form})
    elif request.method == "POST":
        form = FormUsuario(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario agregado correctamente.')
            return render(request, 'agregarUsuarios.html', {"form": form, 'usuario':'Usuario agregado correctamente.'})
        else:
            return render(request, 'agregarUsuarios.html', {"form": form})


def formdestinos(request):
    if request.method == "GET":
        form = FormDestino()
        return render(request, 'agregarDestino.html', {"form": form})
    elif request.method == "POST":
        form = FormDestino(request.POST)
        if form.is_valid():
            form.save()
        messages.success(request, 'Destino agregado correctamente.')
        return render(request, 'agregarDestino.html', {"form": form, 'destino':'Destino agregado correctamente.'})


def formviajes(request):
    if request.method == "GET":
        form = FormViaje()
        return render(request, 'agregarViaje.html', {"form": form})
    elif request.method == "POST":
        form = FormViaje(request.POST)
        if form.is_valid():
            form.save()
        messages.success(request, 'Viaje agregado correctamente.')
        return render(request, 'agregarViaje.html', {"form": form, 'viaje':'Viaje agregado correctamente.'})

def formreservas(request):
    if request.method == "GET":
        form = FormReserva()
        return render(request, 'agregarReserva.html', {"form": form})
    elif request.method == "POST":
        form = FormReserva(request.POST)
        
        if form.is_valid():
            viaje = form.cleaned_data["viaje"]
            viaje.stock -= 1
            viaje.save()
            form.save()
        messages.success(request, 'Reserva agregada correctamente.')
        return render(request, 'agregarReserva.html', {"form": form, 'reserva':'Reserva agregada correctamente.'})

def formcotizaciones(request):
    if request.method == "GET":
        form = FormCotizacion()
        return render(request, 'agregarCotizacion.html', {"form": form})
    elif request.method == "POST":
        form = FormCotizacion(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cotizacion agregada correctamente.')
            return render(request, 'agregarCotizacion.html', {"form": form, 'cotizacion':'Cotizacion agregada correctamente.'})
        else:
            return render(request, 'agregarCotizacion.html', {"form": form})



def formUsuarioUsername(request):
    if request.method == "GET":
        form = FormUsuarioUsername()
        return render(request, 'listaUsuarios.html', {"form": form})
    elif request.method == "POST":
        form = FormUsuarioUsername(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'listaUsuarios.html', {"form": form})



# instance sirve para mostrar los datos del usuario ya almacenados
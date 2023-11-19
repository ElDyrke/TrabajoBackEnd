from django.shortcuts import render, redirect
from app.forms import *
from app.models import TipoUsuario, Usuario, Viaje
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache


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
    print("pswrd:", pswrd)
    print("usuario.contrasenna:", usuario.contrasenna)
    print("check_password result:", check_password(pswrd, usuario.contrasenna))

    # No se por que check_password retorna Falso. Revisar
    return usuario and usuario.tipo_usuario and usuario.tipo_usuario.nombre == rol #and check_password(pswrd,usuario.contrasenna)

def inicio_sesion(request):
    if request.method == "GET":
        return render(request, "inicio_sesion.html")
    
    elif request.method == "POST":
        getUsername = request.POST['username']
        getContrasenna = request.POST['contrasenna']
        #si con filter no se encuentra el username ni contrasena buscada, entonces devuelve None.
        usuario = Usuario.objects.filter(username=getUsername, contrasenna=getContrasenna).first()

        # print(f"usuario: {usuario.username} {usuario.tipo_usuario.nombre}")
        # print(f"{check_password(getContrasenna, usuario.contrasenna)}")
        if usuario is not None:
            if autenticar(usuario, "Cliente", getContrasenna):

                request.session["username"] = getUsername
                print(f"El usuario {getUsername} ha iniciado sesión.")
                return render(request, "cliente.html", {'username': getUsername})
            

            elif autenticar(usuario, "Administrador", getContrasenna):
                request.session["administrador"] = getUsername
                print(f"El administrador {getUsername} ha iniciado sesión.")
                return render(request, 'administrador.html', {'username': getUsername})

            else:
                error_message = "Error. Verifique que haya ingresado correctamente los datos"
                print("Error. Verifique que haya ingresado correctamente los datos")
                return render(request, "inicio_sesion.html", {"error_message": error_message})
        else:
            error_message = "Error. Verifique que haya ingresado correctamente los datos"
            return render(request, "inicio_sesion.html", {"error_message": error_message})

def viajes_reservados(request, id):
    # Obtengo la fila de la tabla Viaje, 
    # que contenga el id del viaje seleccionado.
    # get() solo se usa cuando se esta seguro que el dato existe. 
    getViaje = Viaje.objects.get(id=id)

    if getViaje.stock > 0:
        # si carrito_cantidad no existe, entonces se inicia en 0
        cantidad = request.session.get("carrito_cantidad", 0)
        request.session["carrito_cantidad"] = cantidad + 1
        getViaje.stock = getViaje.stock - 1; 
        getViaje.save()
    #aqui se retorna un render
    return inicio(request)


def cerrar_sesion(request):
    sesion = request.session
    try:
        if "username" in sesion:
            del sesion["username"]
        elif "administrador" in sesion:
            del sesion["administrador"]
        return redirect('inicio_sesion')
    except:
        return redirect('inicio_sesion')



def es_administrador(user):
    return user.is_authenticated and user.tipo_usuario.nombre == 'Administrador'


def cliente(request):
    return render(request, "cliente.html", {"username": request.user.username})

def administrador(request):
    return render(request, "administrador.html", {"username": request.user.username})


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


def formUsuarioUsername(request):
    if request.method == "GET":
        form = FormUsuarioUsername()
        return render(request, 'listaUsuarios.html', {"form": form})
    elif request.method == "POST":
        form = FormUsuarioUsername(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'listaUsuarios.html', {"form": form})


'''  
# user_passes_test deberia servir para que solo los administradores puedan acceder a la pagina
# pero aun no puedo hacer que funcione
@user_passes_test(es_administrador, login_url='/inicio_sesion/')    
@never_cache
'''  


# La idea que tenia era mostrar una lista de usuarios para luego editar sus datos
# pero manteniendo sus datos actuales, en caso de que no quiera modificarlos.
# instance sirve para mostrar los datos del usuario ya almacenados
# Aun no puedo hacer que funcione.
# primero deberia mostrar la pagina listaUsuarios.html
# y luego renderizar hacia editarUsuarios.html con el id del cliente.
def editarUsuarios(request,id):
    # Obtener la instancia del usuario que se va a editar
    usuario = Usuario.objects.get(pk=id)

    if request.method == 'POST':
        formulario = FormUsuario(request.POST, instance=usuario)
        formulario.tipo_usuario_id = 1;
        if formulario.is_valid():
            print(formulario)
            formulario.save()
            return render(request, 'editarUsuarios.html', {"form": formulario})
    else:
        # Si la solicitud no es POST, se mostrara el formulario con los datos actuales del usuario
        # instance sirve para mostrar los datos del usuario ya almacenados
        formulario = FormUsuario(instance=usuario)

    return render(request, 'editarUsuarios.html', {'formulario': formulario, 'usuario': usuario})
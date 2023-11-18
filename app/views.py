from django.shortcuts import render, redirect
from app.models import TipoUsuario, Usuario, Viaje
from django.contrib import messages


def inicio(request):
    if request.session.get("usuario"):
        viajes = Viaje.objects.all()
        return render(request, "inicio.html", {"viajes": viajes})
    else:
        return render(request, "inicio_sesion.html")

def registro_usuario(request):
    if request.method == "GET":
        return render(request, "registro_usuario.html")
    elif request.method == "POST":
        rut = request.POST["rut"]
        username = request.POST["username"]
        nombre = request.POST["nombre"]
        apellido = request.POST["apellido"]
        contrasenna = request.POST["contrasenna"]
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
            return redirect('/inicio_sesion')
        else:
            messages.error(request, 'Error en el formulario. Verifica los datos ingresados.')
            return render(request, 'registro_usuario.html')

def inicio_sesion(request):
    if request.method == "GET":
        return render(request, "inicio_sesion.html")
    
    elif request.method == "POST":
        getUsername = request.POST.get('username')
        getContrasenna = request.POST.get('contrasenna')
        #si con filter no se encuentra el username ni contrasena buscada, entonces devuelve None.
        usuario = Usuario.objects.filter(username=getUsername, contrasenna=getContrasenna).first()

        if usuario and usuario.tipo_usuario.id ==1:
            #si tipo_usuario_id == 1 , entonces se inicia como usuario.
            # Para agregar un valor dentro de la SESSION, lo hacemos como si fuera un diccionario
            request.session["usuario"] = getUsername
            print(f"El usuario {getUsername} ha iniciado sesión.")
            return render(request, "cliente.html", {'username':getUsername})
        
        elif usuario and usuario.tipo_usuario.id==2:
            # Para agregar un valor dentro de la SESSION, lo hacemos como si fuera un diccionario
            request.session["administrador"] = getUsername
            print(f"El administrador {getUsername} ha iniciado sesión.")
            return render(request, "administrador.html", {'username':getUsername})

        else:
            # Enviar un mensaje de error si no se proporciona un nombre de usuario
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

def cliente(request):
    return render(request, "cliente.html")

def administrador(request):
    return render(request, "administrador.html")
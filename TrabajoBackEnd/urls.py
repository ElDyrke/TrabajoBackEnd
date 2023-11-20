from django.contrib import admin
from django.urls import path
from app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name="inicio"),
    path('registro_usuario/', views.registro_usuario, name="registro_usuario"),
    path('inicio_sesion/', views.inicio_sesion, name="inicio_sesion"),
    path('cerrar_sesion/', views.cerrar_sesion, name="cerrar_sesion"),
    path('cliente/', views.cliente, name="cliente"),
    path('administrador/', views.administrador, name="administrador"),
    path('agregarUsuarios/', views.formusuarios, name="formusuarios"),
    path('agregardestinos/', views.formdestinos, name="formdestinos"),
    path('agregarviajes/', views.formviajes, name="formviajes"),
    path('agregarreservas/', views.formreservas, name="formreservas"),
    path('agregarcotizaciones/', views.formcotizaciones, name="formcotizaciones"),
    path('cerrar/', views.cerrar_sesion, name="cerrar"),
    path('viajes_reservados/', views.viajes_reservados, name="viajes_reservados"),
    path('editarUsuarios/<int:id>', views.editarUsuarios, name="editarUsuarios"),
    path('eliminarUsuarios/<int:id>', views.eliminarUsuarios, name="eliminarUsuarios"),
    path('listaUsuarios/', views.listaUsuarios, name="listaUsuarios"),
    path('listaDestinos/', views.listaDestinos, name="listaDestinos"),
    path('listaViajes/', views.listaViajes, name="listaViajes"),
    path('listaCotizaciones/', views.listaCotizaciones, name="listaCotizaciones"),
    path('listaReservas/', views.listaReservas, name="listaReservas"),
    path('eliminarReservas/<int:id>', views.eliminarReservas, name="eliminarReservas"),
    path('eliminarCotizaciones/<int:id>', views.eliminarCotizaciones, name="eliminarCotizaciones"),
    path('eliminarViajes/<int:id>', views.eliminarViajes, name="eliminarViajes"),
    path('eliminarUsuarios/<int:id>', views.eliminarUsuarios, name="eliminarUsuarios"),
    path('eliminarDestinos/<int:id>', views.eliminarDestinos, name="eliminarDestinos"),
    path('vista_viaje/<int:id>', views.vista_viaje, name="vista_viaje"),
    path('add_cotizacion/<int:id>', views.add_to_cotizacion, name='add_to_cotizacion'),
    path('usuario_cotizar', views.usuario_cotizar, name="usuario_cotizar")
]

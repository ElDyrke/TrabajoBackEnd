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
    path('viajes_reservados/<int:id>', views.viajes_reservados, name="viajes_reservados"),
    
]

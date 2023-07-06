from django.urls import path
from . import views

urlpatterns = [
    path("",views.Home,name="Index"),
    path("indicadores",views.Indicadores,name="Indicadores"),
    path("calculadora",views.Calculadora,name="Calculadora"),
    path("tabla",views.Tabla,name="Tabla"),
    path("descargar",views.Descargar,name="Descargar"),
    path("graficas",views.Grafica,name="Grafica")
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('agregar/', views.agregar_ciudad, name='agregar_ciudad'),
    path('actualizar/', views.actualizar_clima, name='actualizar_clima'),
    path('graficos/', views.graficos, name='graficos'),
    path('ciudad/<int:ciudad_id>/', views.detalle_ciudad, name='detalle_ciudad'),
    path('sobre/', views.sobre_proyecto, name='sobre_proyecto'),
]

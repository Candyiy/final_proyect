from django.urls import path
from . import views

urlpatterns = [

    path('crear/', views.crear_oferta, name='crear_oferta'),
    path('ofertas/', views.lista_ofertas, name='lista_ofertas'),

]
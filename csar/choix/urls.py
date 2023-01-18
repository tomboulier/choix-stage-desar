from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:interne_uuid>/', views.choix_interne, name='choix_interne')
]
from django.urls import path

from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('addh', views.add_hydro, name='add_hydro'),
    path('adda', views.add_acid, name='add_acid'),
    path('del', views.delete),
]


from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('add', views.add_substance, name='add'),
]
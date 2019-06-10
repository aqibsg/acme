from django.urls import path

from . import views

app_name = 'exporter'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.search, name='search'),
    path('delete/', views.delete, name='delete'),

]
"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from calendario import views

urlpatterns = [
    path('', views.login_view, name='index'),
    path('calendar', views.calendar_view, name='calendar'),
    path('get_events/', views.get_events, name='get_events'),
    path('get_clients/', views.get_clients, name='get_clients'),
    path('add_event/', views.add_event, name='add_event'),
    path('clients/', views.clients_page, name='clients_page'),
    path('get_clients/', views.get_clients, name='get_clients'),
    path('search_clients/', views.search_clients, name='search_clients'),
    path('add_client/', views.add_client, name='add_client'),
    path('delete_client/', views.delete_client, name='delete_client'),
    path('login/', views.login_view, name='login'),
    path('fornecedores/', views.fornecedores_page, name='fornecedores_page'),
    path('get_fornecedores/', views.get_fornecedores),
    path('get_tipos_servico/', views.get_tipos_servico),
    path('add_fornecedor/', views.add_fornecedor),
    path('delete_fornecedor/', views.delete_fornecedor),
]

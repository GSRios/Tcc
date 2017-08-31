from django.conf.urls import url

from Rotas import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajax/go/$',views.teste),    
]

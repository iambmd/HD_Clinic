from django.urls import path

from . import views

app_name = 'clinic'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('news/', views.news, name='news'),
    path('news/<slug:slug>/', views.article_detail, name='article_detail'),
    path('appointment/', views.appointment, name='appointment'),
    path('contact/', views.contact, name='contact'),
    path('location/', views.location, name='location'),
]

from django.urls import path

from . import api_views

app_name = 'clinic_api'

urlpatterns = [
    path('services/', api_views.ServiceListAPIView.as_view(), name='service_list'),
    path('doctors/', api_views.DoctorListAPIView.as_view(), name='doctor_list'),
    path('articles/', api_views.ArticleListAPIView.as_view(), name='article_list'),
    path('articles/<slug:slug>/', api_views.ArticleDetailAPIView.as_view(), name='article_detail'),
    path('appointments/', api_views.AppointmentCreateAPIView.as_view(), name='appointment_create'),
    path('contact/', api_views.ContactCreateAPIView.as_view(), name='contact_create'),
]

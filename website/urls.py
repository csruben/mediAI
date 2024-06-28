from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('diagnose/', views.diagnose, name='diagnose'),
    path('blood-pressure/', views.blood_pressure, name='heart'),
    path('evaluate_bp/', views.evaluate_bp, name='evaluate_bp'),
]

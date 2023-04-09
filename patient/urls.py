from django.urls import path
from .views import  patient_dashboard,patient_profile


urlpatterns = [
    path('patient-dashboard/', patient_dashboard, name='patient_dashboard'),
    path('patient-profile/', patient_profile, name='patient_profile')
]
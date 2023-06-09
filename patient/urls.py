from django.urls import path
from .views import  patient_dashboard,patient_profile,patient_blogs,patient_get_category,patient_post,patient_post_comment,patient_search_view,patient_my_appointments,patient_book_appointment,patient_confirmbook


urlpatterns = [
    path('patient-dashboard/', patient_dashboard, name='patient_dashboard'),
    path('patient-profile/', patient_profile, name='patient_profile'),
    path('patient_blogs/', patient_blogs, name='patient_blogs'),
    path('patient_search/',patient_search_view,name='patient_search'),
     path('patient_post/<str:title>/',patient_post,name='patient_post'),
     path('patient_comment/',patient_post_comment,name='patient_comment'),
     path('patient_category/<str:cat>/',patient_get_category,name='patient_categories'),
     path('patient_my_appointments/',patient_my_appointments,name='patient_my_appointments'),
        path('patient_book_appointment/', patient_book_appointment, name='patient_book_appointment'),
        path('patient_confirm_book/<str:docname>/',patient_confirmbook,name='patient_confirmbook')
]
from django.urls import path
from .views import  doctor_dashboard,doctor_profile,doctor_blogs,post,post_comment,get_category,upload_blog,search_view,myblogs,doctor_drafts,modify



urlpatterns = [
    path('doctor_dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('doctor_profile/', doctor_profile, name='doctor_profile'),
    path('doctor_blogs/', doctor_blogs, name='doctor_blogs'),
    path('doctor_drafts/',doctor_drafts , name='doctor_drafts'),
    path('doctor_upload_assignment/', upload_blog,
         name="upload_blog"),
    path('doctor_myblogs/', myblogs,
         name="myblogs"),
    path('search/',search_view,name='search'),
     path('post/<str:title>/',post,name='post'),
     path('comment/',post_comment,name='comment'),
     path('category/<str:cat>/',get_category,name='categories'),
     path('draft/<str:pid>/',modify,name='modify')
]

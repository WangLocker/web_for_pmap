from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/',admin.site.urls),
    path('personal/',views.personal),
    path('login/',views.login),
    path('personal_logout/',views.personal_logout),
    path('register/',views.register,name='register'),
    path('register/verify/',views.register_verify),
    path('personal/logout/',views.personal_logout),
    path('send-code/',views.send_code),
    path('send-pwd/',views.send_pwd),
    path('personal_edit/',views.personal_edit),
    path('img_edit/',views.image),
    path('login/mobilecode/',views.m_code),
]
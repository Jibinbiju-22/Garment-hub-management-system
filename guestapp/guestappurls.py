from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),

    path('registration', views.registration, name='registration'),
    path('filllocation', views.filllocation, name='filllocation'),
    path('logout', views.logout, name='logout'),
    path('forgotpassword', views.forgotpassword,name='forgotpassword'),

    path('', views.home),
]

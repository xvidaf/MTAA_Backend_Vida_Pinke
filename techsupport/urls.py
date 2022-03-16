from django.urls import path
from techsupport import views


urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
]

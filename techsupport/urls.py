from django.urls import path
from techsupport import views


urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('sendmessage', views.sendmessage, name='sendmessage'),
    path('getticketuser', views.getticketuser, name='getticketuser'),
    path('gettickets', views.gettickets, name='gettickets'),
    path('deleteticket', views.deleteTicket, name='deleteTicket'),
]

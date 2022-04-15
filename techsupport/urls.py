from django.urls import path
from techsupport import views


urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('sendmessage', views.sendmessage, name='sendmessage'),
    path('createticket', views.createticket, name='createticket'),
    path('getticketuser', views.getticketuser, name='getticketuser'),
    path('getticketadmin', views.getticketadmin, name='getticketadmin'),
    path('gettickets', views.gettickets, name='gettickets'),
    path('getticketsbyID', views.getticketsbyID, name='getticketsbyID'),
    path('getmessages', views.getmessages, name='getmessages'),
    path('updateticket', views.updateticket, name='updateticket'),
    path('deleteticket', views.deleteTicket, name='deleteTicket'),
    path('insertmedia', views.insertmedia, name='insertmedia'),
    path('getmedia', views.getmedia, name='getmedia'),
]

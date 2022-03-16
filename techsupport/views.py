from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from techsupport.models import User, ChatMessages, Tickets, Devices, Media
import json
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

@csrf_exempt
def register(request):
    if request.method == "POST":
        last_login = datetime.now()
        j = json.loads(request.body)

        try:
            mail = j['email']
        except:
            mail = False

        try:
            pwd = j['password']
        except:
            pwd = False

        if mail and pwd:
            try:
                u = User(email=mail, password=pwd, usertype="user", lastlogin=last_login)
                u.save()
                return HttpResponse(200)
            except:
                return HttpResponse(400)
        else:
            return HttpResponse(400)

@csrf_exempt
def login(request):
    if request.method == "POST":
        j = json.loads(request.body)
        try:
            mail = j['email']
        except:
            mail = False

        try:
            pwd = j['password']
        except:
            pwd = False

        if mail and pwd:
            try:
                authenticated = User.objects.get(email=mail, password=pwd)
                authenticated.lastlogin = datetime.now()
                authenticated.save()
                return HttpResponse(200)
            except:
                return HttpResponse(400)
        else:
            return HttpResponse(400)

@csrf_exempt
def sendmessage(request):
    if request.method == "POST":
        j = json.loads(request.body)
        try:
            to = j['to']
        except:
            to = False

        try:
            fromm = j['from']
        except:
            fromm = False

        try:
            message = j['message']
        except:
            message = False

        try:
            ticketid = j['ticketid']
        except:
            ticketid = False

        if to and fromm and message and ticketid:
            try:
                message = ChatMessages(ticketid=Tickets.objects.get(pk=ticketid), reciever=User.objects.get(pk=to), sender=User.objects.get(pk=fromm), timestamp= datetime.now(), message=message)
                message.save()
                return HttpResponse(200)
            except:
                return HttpResponse(400)
        else:
            return HttpResponse(400)

def getticketuser(request):
    if request.method == "GET":
        try:
            id = request.GET.get('ticketid', '')
            data = list(Tickets.objects.filter(pk=id).values())
            data[0]['createdBy_id'] = list(User.objects.filter(pk=data[0]['createdBy_id']).values())
            if data[0]['assignedTo_id']:
                data[0]['assignedTo_id'] = list(User.objects.filter(pk=data[0]['assignedTo_id']).values())
            data[0]['deviceType_id'] = list(Devices.objects.filter(pk=data[0]['deviceType_id']).values())
            if data[0]['solutionVideo_id']:
                data[0]['solutionVideo_id'] = list(Media.objects.filter(pk=data[0]['solutionVideo_id']).values())
            if data[0]['image_id']:
                data[0]['image_id'] = list(Media.objects.filter(pk=data[0]['image_id']).values())
            return JsonResponse(data, safe=False)
        except:
            return HttpResponse(400)

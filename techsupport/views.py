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

@csrf_exempt
def createticket(request):
    if request.method == "POST":
        j = json.loads(request.body)

        try:
            name = j['name']
        except:
            name = False

        try:
            device_id = j['device_id']
        except:
            device_id = False

        try:
            createdby_id = j['createdby_id']
        except:
            createdby_id = False

        try:
            issuetype = j['issuetype']
        except:
            issuetype = False

        try:
            description = j['description']
        except:
            description = False

        try:
            image_id = j['image_id']
        except:
            image_id = False

        if name and device_id and createdby_id and issuetype and description and image_id:
            try:
                ticket = Tickets(name=name, deviceType=Devices.objects.get(pk=device_id), createdBy=User.objects.get(pk=createdby_id),
                                       issueType= issuetype, description=description, stage=1, complete=False, image=Media.objects.get(pk=image_id))
                ticket.save()
                return HttpResponse(200)
            except:
                return HttpResponse(400)
        elif name and device_id and createdby_id and issuetype and description:
            try:
                ticket = Tickets(name=name, deviceType=Devices.objects.get(pk=device_id), createdBy=User.objects.get(pk=createdby_id),
                                       issueType= issuetype, description=description, stage=1, complete=False)
                ticket.save()
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

def getticketadmin(request):
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

def gettickets(request):
    if request.method == "GET":
        try:
            data = list(Tickets.objects.all().values())
            for x in data:
                x['createdBy_id'] = list(User.objects.filter(pk=x['createdBy_id']).values())
                if x['assignedTo_id']:
                    x['assignedTo_id'] = list(User.objects.filter(pk=x['assignedTo_id']).values())
                x['deviceType_id'] = list(Devices.objects.filter(pk=x['deviceType_id']).values())
                if x['solutionVideo_id']:
                    x['solutionVideo_id'] = list(Media.objects.filter(pk=x['solutionVideo_id']).values())
                if x['image_id']:
                    x['image_id'] = list(Media.objects.filter(pk=x['image_id']).values())
            return JsonResponse(data, safe=False)
        except:
            return HttpResponse(400)

def getmessages(request):
    if request.method == "GET":
        try:
            data = list(ChatMessages.objects.all().values())
            for x in data:
                if x['sender_id'] is int(request.GET['userid']):
                    x['from'] = User.objects.get(pk=x['sender_id']).email
                    x['to'] = User.objects.get(pk=x['reciever_id']).email
                    x.pop('sender_id', None)
                    x.pop('reciever_id', None)
                    x.pop('id', None)
                    x.pop('ticketid_id', None)
                else:
                    data.remove(x)
            return JsonResponse(data, safe=False)
        except:
            return HttpResponse(400)

@csrf_exempt
def deleteTicket(request):
    if request.method == "DELETE":
        try:
            id = request.GET.get('ticketid', '')
            Tickets.objects.get(pk=id).delete()
            return HttpResponse(204)
        except:
            return HttpResponse(400)
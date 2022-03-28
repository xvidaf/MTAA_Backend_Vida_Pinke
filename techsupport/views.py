from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from techsupport.models import User, ChatMessages, Tickets, Devices, Media
import json
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.db import models as dmodels
from django.http import FileResponse
import secrets

# Function to check for permissions
# authToken is required and should contain the token the user provided
# ticketID is optional and should be used when determining whether the user has access to a requested ticket
# type is optional and is used to check whether the user is of the required usertype
# For example of use check getTicketUser
# You get the token by using the login endpoint
# Expiration not implemented, but should be simple to do if needed
# If treba viac kontrol:
#   povedz mi
def checkPermissions(authToken, ticketID=None, fromID=None, toID=None, type=None, createdBy= None):
    try:
        authToken = authToken.replace("Bearer ", '')
        authenticated= User.objects.get(token= authToken)
        if ticketID:
            if authenticated.usertype == "user":
                Tickets.objects.get(id=ticketID, createdBy=authenticated.id)
            elif authenticated.usertype == "admin":
                Tickets.objects.get(id=ticketID, assignedTo=authenticated.id)
        if type:
            User.objects.get(token=authToken, usertype=type)

        if fromID:
            if int(fromID) == authenticated.id:
                if authenticated.usertype == "user":
                    Tickets.objects.get(id=ticketID, createdBy=authenticated.id, assignedTo=toID)
                elif authenticated.usertype == "admin":
                    Tickets.objects.get(id=ticketID, assignedTo=authenticated.id, createdBy=toID)
            else:
                return False
        if createdBy:
            if authenticated.id != createdBy:
                return False
        return True
    except:
        return False

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
                #We create a token for the user
                loginToken = secrets.token_hex(20)
                authenticated.token = loginToken
                authenticated.save()
                #return HttpResponse(200)
                #We return the token to the requester
                return JsonResponse({"token": loginToken}, safe=False)
            except:
                return HttpResponse(400)
        else:
            return HttpResponse(400)
    else:
        return HttpResponse(400)

@csrf_exempt
def sendmessage(request):
    if request.method == "POST":
        j = json.loads(request.body)
        # We check if the requester has the required permissions
        if checkPermissions(request.META.get('HTTP_AUTHORIZATION'), ticketID=j['ticketid'], fromID=j['from'], toID=j['to']):
            print("Authenticated")
        else:
            return HttpResponse(401)

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
    else:
        return HttpResponse(400)

@csrf_exempt
def createticket(request):
    if request.method == "POST":
        j = json.loads(request.body)
        # We check if the requester has the required permissions
        if checkPermissions(request.META.get('HTTP_AUTHORIZATION'), type="user", createdBy=j['createdby']):
            print("Authenticated")
        else:
            return HttpResponse(401)

        try:
            name = j['name']
        except:
            name = False

        try:
            device_id = j['devicetype']
        except:
            device_id = False

        try:
            createdby_id = j['createdby']
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
    else:
        return HttpResponse(400)

def getticketuser(request):
    if request.method == "GET":
        #We check if the requester has the required permissions
        if checkPermissions(request.META.get('HTTP_AUTHORIZATION'), ticketID=request.GET.get('ticketid', ''), type="user"):
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
        else:
            return HttpResponse(401)
    else:
        return HttpResponse(400)

def getticketadmin(request):
    if request.method == "GET":
        #We check if the requester has the required permissions
        if checkPermissions(request.META.get('HTTP_AUTHORIZATION'), ticketID=request.GET.get('ticketid', ''), type="admin"):
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
        else:
            return HttpResponse(401)
    else:
        return HttpResponse(400)

def gettickets(request):
    if request.method == "GET":
        #We check if the requester has the required permissions
        if checkPermissions(request.META.get('HTTP_AUTHORIZATION')):
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
        else:
            return HttpResponse(401)
    else:
        return HttpResponse(400)

def getmessages(request):
    if request.method == "GET":
        #We check if the requester has the required permissions
        if checkPermissions(request.META.get('HTTP_AUTHORIZATION'), ticketID=request.GET.get('ticketid', '')):
            try:
                data = list(ChatMessages.objects.all().values())
                msgs = []
                for x in data:
                    if x['ticketid_id'] == int(request.GET['ticketid']):
                        x['from'] = User.objects.get(pk=x['sender_id']).email
                        x['to'] = User.objects.get(pk=x['reciever_id']).email
                        x.pop('sender_id', None)
                        x.pop('reciever_id', None)
                        x.pop('id', None)
                        x.pop('ticketid_id', None)
                        msgs.append(x)
                return JsonResponse(msgs, safe=False)
            except:
                return HttpResponse(400)
        else:
            return HttpResponse(401)
    else:
        return HttpResponse(400)

@csrf_exempt
def updateticket(request):
    if request.method == "PUT":
            try:
                j = json.loads(request.body)
                # We check if the requester has the required permissions
                if checkPermissions(request.META.get('HTTP_AUTHORIZATION'), ticketID=j['ticketid'], type="admin"):
                    print("Authenticated")
                else:
                    return HttpResponse(401)
                try:
                    ticketid = j['ticketid']
                except:
                    ticketid = False

                try:
                    stage = j['stage']
                except:
                    stage = False

                try:
                    complete = j['complete']
                except:
                    complete = False

                try:
                    solutiontext = j['solutiontext']
                except:
                    solutiontext = False

                try:
                    solutionvideo = j['solutionvideo']
                except:
                    solutionvideo = False

                ticket = Tickets.objects.get(pk=ticketid)
                ticket.stage = stage
                ticket.complete = complete
                ticket.solutionText = solutiontext
                if solutionvideo:
                    ticket.solutionVideo = Media.objects.get(pk=solutionvideo)
                ticket.save()
                return HttpResponse(204)
            except:
                return HttpResponse(401)
    else:
        return HttpResponse(400)

@csrf_exempt
def deleteTicket(request):
    if request.method == "DELETE":
        #We check if the requester has the required permissions
        if checkPermissions(request.META.get('HTTP_AUTHORIZATION'), ticketID=request.GET.get('ticketid', ''), type="user"):
            try:
                id = request.GET.get('ticketid', '')
                Tickets.objects.get(pk=id).delete()
                return HttpResponse(204)
            except:
                return HttpResponse(400)
        else:
            return HttpResponse(401)
    else:
        return HttpResponse(400)

@csrf_exempt
def insertmedia(request):
    if request.method == "POST":
        try:
            # We check if the requester has the required permissions
            if checkPermissions(request.META.get('HTTP_AUTHORIZATION'), type="admin"):
                print("Authenticated")
            else:
                return HttpResponse(401)

            try:
                name = request.POST['name']
            except:
                name = False

            try:
                file = request.FILES['file']
            except:
                file = False

            try:
                isVideo = request.POST['isVideo']
            except:
                isVideo = False

            if name and file and isVideo:
                media = Media(name=name, path=file, isvideo=isVideo)
                media.save()
                return HttpResponse(200)
            else:
                return HttpResponse(400)

        except:
            return HttpResponse(400)
    else:
        return HttpResponse(400)

def getmedia(request):
    if request.method == "GET":
        #We check if the requester has the required permissions
        if checkPermissions(request.META.get('HTTP_AUTHORIZATION')):
            try:
                id = request.GET.get('mediaid', '')
                data = Media.objects.get(pk=id)
                img = open(str(data.path), 'rb')
                response = FileResponse(img)
                return response
            except:
                return HttpResponse(400)
        else:
            return HttpResponse(401)
    else:
        return HttpResponse(400)

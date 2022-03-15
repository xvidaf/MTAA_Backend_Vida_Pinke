from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from techsupport.models import User
import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def register(request):
    if request.method == "POST":
        last_login = datetime.now()
        j = json.loads(request.body)

        try:
            mail = j['mail']
        except:
            mail = False

        try:
            pwd = j['pass']
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


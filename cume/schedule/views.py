from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Class
from django.contrib import messages
from django.urls import reverse

from selenium import webdriver
from bs4 import BeautifulSoup
import requests, json
import re, operator

import uuid

from django.conf import settings
import os, sys
apiDir = os.path.join(settings.PROJECT_ROOT_DIR, 'api')
sys.path.insert(0, apiDir)
import apiRequests

loggingInSteps = {}

def index(request):
    global loggingInSteps

    if request.method == 'GET':
        clientId = uuid.uuid4()
        loggingInSteps[clientId] = ""
        return render(request, 'schedule/login.html', {'id' : clientId})
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        clientId = request.POST.get('id')

        neededClasses = apiRequests.degreeClasses(username, password, loggingInSteps, clientId)
        print(neededClasses)
        if 'error' not in neededClasses:
            request.session['degreeData'] = neededClasses
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['degreeData'] = neededClasses

                request.session['id'] = clientId

                loggingInSteps.pop(clientId, None)
                return redirect(reverse('schedule'))
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                login(request, user)
                request.session['degreeData'] = neededClasses
                request.session['newUser'] = True

                request.session['id'] = clientId

                loggingInSteps.pop(clientId, None)
                return redirect(reverse('schedule'))
        else:
            messages.add_message(request, messages.INFO, 'Oh no, the username or password is invalid')

            loggingInSteps.pop(clientId, None)
            return redirect(reverse('index'))

@login_required(redirect_field_name='')
def schedule(request):
    userClasses = request.user.class_set.all()
    print(userClasses)
    return render(request, 'schedule/schedule.html', {'classes': userClasses})

@login_required(redirect_field_name='')
def logoutUser(request):
    logout(request)
    return redirect(reverse('index'))

def poll_state(request):
    """ A view to report the progress to the user """
    global loggingInSteps

    data = 'Fail'
    if request.is_ajax() and request.method == 'POST':
        data = loggingInSteps[request.POST.get('id')]
    else:
        data = 'This is not an ajax request'

    result = {'data': data}
    return JsonResponse(result)

@login_required(redirect_field_name='')
def class_add(request):
    status = 'Fail'
    if request.is_ajax() and request.method == 'POST':
        request.user.class_set.create(name=request.POST.get('name'), times=request.POST.get('times'), instructor=request.POST.get('instructor'), rating=request.POST.get('rating'), room=request.POST.get('room'), dates=request.POST.get('dates'))
        status = 'Success'

    result = {'status': status}
    return JsonResponse(result)

@login_required(redirect_field_name='')
def class_delete(request):
    status = 'Fail'
    if request.is_ajax() and request.method == 'POST':
        classToRemove = request.user.class_set.get(name=request.POST.get('name'))
        classToRemove.delete()
        status = 'Success'

    result = {'status': status}
    return JsonResponse(result)

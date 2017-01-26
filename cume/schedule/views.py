
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

from django.conf import settings
import os, sys
sys.path.append(settings.PROJECT_ROOT_DIR)
from api.tasks import degreeClasses

def index(request):
    if request.method == 'GET':
        return render(request, 'schedule/login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        neededClasses = degreeClasses.delay(username, password)
        if 'error' not in neededClasses:
            request.session['degreeData'] = neededClasses
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['degreeData'] = neededClasses
                return redirect(reverse('schedule'))
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                login(request, user)
                request.session['degreeData'] = neededClasses
                request.session['newUser'] = True
                return redirect(reverse('schedule'))
        else:
            messages.add_message(request, messages.INFO, neededClasses['error'])
            return redirect(reverse('index'))

@login_required(redirect_field_name='')
def schedule(request):
    userClasses = request.user.class_set.all()
    return render(request, 'schedule/schedule.html', {'classes': userClasses})

@login_required(redirect_field_name='')
def logoutUser(request):
    logout(request)
    return redirect(reverse('index'))

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

def poll_state(request):
    """ A view to report the progress to the user """
    data = 'Fail'
    if request.is_ajax():
        if 'task_id' in request.POST.keys() and request.POST['task_id']:
            task_id = request.POST['task_id']
            task = AsyncResult(task_id)
            data = task.result or task.state
        else:
            data = 'No task_id in the request'
    else:
        data = 'This is not an ajax request'

    json_data = json.dumps(data)
    return JsonResponse(json_data, content_type='application/json')

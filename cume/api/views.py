from django.http import JsonResponse
from .apiRequests import classSearch, degreeClasses

from django.conf import settings
import os, sys
sys.path.append(settings.PROJECT_ROOT_DIR)

def search(request):
    #required
    school = request.GET.get('college', '')
    term = request.GET.get('term', '')
    dept = request.GET.get('dept', '')

    #optional
    courseNbr = request.GET.get('courseNbr', '')
    contains = request.GET.get('contains', '')
    session = request.GET.get('session', '')

    classNbr = request.GET.get('classNbr', '')
    courseCareer = request.GET.get('courseCareer', '')
    reqdes = request.GET.get('reqdes', '')
    instructor = request.GET.get('instructor', '')
    instructorContains = request.GET.get('instrContains', '')
    
    result = classSearch(school, term, dept, courseNbr, contains, session, classNbr, courseCareer, reqdes, instructor, instructorContains)

    return JsonResponse(result)

def degree(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        result = degreeClasses(username, password)

        return JsonResponse(result)

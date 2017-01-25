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
    classNbr = request.GET.get('classNbr', '')
    contains = request.GET.get('contains', '')
    session = request.GET.get('session', '')

    result = classSearch(school, term, dept, classNbr, contains, session)

    return JsonResponse(result)

def degree(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        result = degreeClasses(username, password)

        return JsonResponse(result)

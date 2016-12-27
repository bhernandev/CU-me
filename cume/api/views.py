from django.http import JsonResponse
from . import apiRequests

searchSteps = {}

def search(request):
    global searchSteps
    clientId = request.GET.get('id', '')
    searchSteps[clientId] = ""

    #required
    school = request.GET.get('college', '')
    term = request.GET.get('term', '')
    dept = request.GET.get('dept', '')

    #optional
    classNbr = request.GET.get('classNbr', '')
    contains = request.GET.get('contains', '')
    session = request.GET.get('session', '')

    result = apiRequests.classSearch(school, term, dept, classNbr, contains, session, searchSteps, clientId)

    return JsonResponse(result)

def degree(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        result = apiRequests.degreeClasses(username, password)

        return JsonResponse(result)

def poll_state(request):
    """ A view to report the progress to the user """
    global searchSteps

    data = 'Fail'
    if request.is_ajax() and request.method == 'POST':
        data = searchSteps[request.POST.get('id')]
    else:
        data = 'This is not an ajax request'

    result = {'data': data}
    return JsonResponse(result)

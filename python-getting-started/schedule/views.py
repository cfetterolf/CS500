import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import Http404
from django.http import HttpResponse
from schedule.models import TimeBlock
from schedule.db import getUsers, get_group_info, getTimeBlocks, get_alg_leader_groups, add_user, add_leaders, set_gid, get_groups, login_account, signup_account, add_group, delete_group, reset_gid
from schedule.algorithm import run
from django.conf import settings


# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', {})

class SchedulePageView(TemplateView):
    def get(self, request, **kwargs):
        group_info = {
            'users': getUsers(settings.GID),
            'time_blocks': getTimeBlocks(settings.GID),
            'leader_groups': get_alg_leader_groups(settings.GID),
            'gid': settings.GID,
            'group_name': get_group_info(settings.GID)['name'],
            'group_term': get_group_info(settings.GID)['term']
        }
        return render(request, 'schedule.html', {'group_info': group_info, 'alg_results': run()})

class LoginPageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'login.html', context=None)

class GroupsPageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'groups.html', context=None)

class NewGroupPageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'new_group.html', context=None)


def checkLogin(request):
    if (settings.LOGGED_IN == True):
        return render(request, 'index.html', {})
    else:
        return render(request, 'login.html', {})

def getGroupInfo(request):
    if request.method == 'GET':
        group_info = {
            'users': getUsers(settings.GID),
            'time_blocks': getTimeBlocks(settings.GID),
            'leader_groups': get_alg_leader_groups(settings.GID),
            'gid': settings.GID,
            'group_name': get_group_info(settings.GID)['name'],
            'group_term': get_group_info(settings.GID)['term']
        }
        return JsonResponse(group_info)
    else:
        raise Http404

def getGroups(request):
    if request.method == 'GET':
        groups = get_groups()
        return JsonResponse(groups)
    else:
        raise Http404

def addGroup(request):
    if request.method == 'POST':
        response = add_group(json.loads(request.body))
        return JsonResponse(response)
    else:
        raise Http404

def deleteGroup(request):
    if request.method == 'GET':
        gid = int(request.GET.get('gid', -1))
        if (gid == -1):
            return JsonResponse({'error': 'Group Not Found'})
        else:
            return JsonResponse(delete_group(gid))
    else:
        raise Http404

def addUser(request):
    if request.method == 'POST':
        response = add_user(json.loads(request.body), settings.GID)
        return JsonResponse(response)
    else:
        raise Http404

def addLeaders(request):
    if request.method == 'POST':
        response = add_leaders(json.loads(request.body))
        return JsonResponse(response)
    else:
        raise Http404

def run_algorithm(request):
    if request.method == 'GET':
        return JsonResponse(run())
    else:
        raise Http404

def setGid(request):
    if request.method == 'POST':
        response = set_gid(json.loads(request.body))
        return JsonResponse(response)
    elif request.method == 'GET':
        response = reset_gid()
        return JsonResponse(response)
    else:
        raise Http404

def login(request):
    if request.method == 'POST':
        response = login_account(json.loads(request.body))
        return JsonResponse(response)
    else:
        raise Http404

def signup(request):
    if request.method == 'POST':
        response = signup_account(json.loads(request.body))
        return JsonResponse(response)
    else:
        raise Http404

def logout(request):
    settings.GID = None
    settings.USERNAME = ''
    settings.PASSWORD = ''
    settings.LOGGED_IN = False
    return render(request, 'login.html', {})

# class LoginPageView(TemplateView):
#     def get(self, request, **kwargs):
#         return render(request, 'login.html', context=None)

# def index(request):
#     r = requests.get('http://httpbin.org/status/418')
#     print(r.text)
#     return HttpResponse('<pre>' + r.text + '</pre>')
#
#
# def db(request):
#
#     greeting = Greeting()
#     greeting.save()
#
#     greetings = Greeting.objects.all()
#
#     return render(request, 'db.html', {'greetings': greetings})

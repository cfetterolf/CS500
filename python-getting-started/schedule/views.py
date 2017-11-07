import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import Http404
from django.http import HttpResponse
from schedule.models import TimeBlock
from schedule.db import getUsers, getTimeBlocks, get_alg_leader_groups
from schedule.algorithm import run


# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', {})

class SchedulePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'schedule.html', context=None)

def getGroupInfo(request):
    if request.method == 'GET':
        group_info = {'users': getUsers(), 'time_blocks': getTimeBlocks(), 'leader_groups': get_alg_leader_groups()}
        return JsonResponse(group_info)
    else:
        raise Http404

def run_algorithm(request):
    if request.method == 'GET':
        return JsonResponse(run())
    else:
        raise Http404


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

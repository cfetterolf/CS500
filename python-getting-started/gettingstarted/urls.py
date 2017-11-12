from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()
from schedule import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='index'),
    url(r'^schedule/$', views.SchedulePageView.as_view(), name='schedule'),
    url(r'^ajax/db/$', views.getGroupInfo, name='getGroupInfo'),
    url(r'^ajax/db/user/$', views.addUser, name='addUser'),
    url(r'^ajax/alg/$', views.run_algorithm, name='run_algorithm'),
]

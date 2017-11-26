from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()
from schedule import views

urlpatterns = [
    url(r'^$', views.checkLogin, name='start'),
    url(r'^users/$', views.HomePageView.as_view(), name='index'),
    url(r'^schedule/$', views.SchedulePageView.as_view(), name='schedule'),
    url(r'^login/$', views.LoginPageView.as_view(), name='login'),
    url(r'^groups/$', views.GroupsPageView.as_view(), name='manage_groups'),
    url(r'^groups/new$', views.NewGroupPageView.as_view(), name='new_group'),
    url(r'^groups/del/$', views.deleteGroup, name='del_group'),
    url(r'^ajax/db/$', views.getGroupInfo, name='getGroupInfo'),
    url(r'^ajax/db/groups/$', views.getGroups, name='getGroups'),
    url(r'^ajax/db/groups/new$', views.addGroup, name='addGroup'),
    url(r'^ajax/db/user/$', views.addUser, name='addUser'),
    url(r'^ajax/db/leaders/$', views.addLeaders, name='addLeaders'),
    url(r'^ajax/alg/$', views.run_algorithm, name='run_algorithm'),
    url(r'^ajax/gid/$', views.setGid, name='setGid'),
    url(r'^ajax/login/$', views.login, name='login'),
    url(r'^ajax/signup/$', views.signup, name='signup'),
    url(r'^logout/$', views.logout, name='logout'),
]

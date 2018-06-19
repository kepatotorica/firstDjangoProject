from django.urls import path, re_path
from . import views

urlpatterns = [
    #/profile/
    re_path(r'^$', views.index, name='index'),
    #/profile/profileID
    re_path(r'^(?P<user_id>[0-9]+)/$', views.view_id, name='view_id'),
    #/music/album
    re_path('users',views.view_users, name='view_users')
]
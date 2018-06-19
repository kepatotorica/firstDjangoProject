from django.urls import path, re_path
from . import views

app_name = 'music'

urlpatterns = [
    #/music/
    re_path(r'^$', views.index, name='index'),
    #/music/albumID
    re_path(r'^(?P<album_id>[0-9]+)/$', views.view_id, name='view_id'),
]
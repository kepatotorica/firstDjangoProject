from django.urls import path, re_path
from . import views

urlpatterns = [
    #/music/
    re_path(r'^$', views.index, name='index'),
    #/music/albumID
    re_path(r'^(?P<album_id>[0-9]+)/$', views.view_id, name='view_id'),
    #/music/album
    #re_path('albums',views.view_albums, name='view_albums')
]
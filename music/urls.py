from django.urls import path, re_path
from . import views

app_name = 'music'

urlpatterns = [
    #/music/
    re_path(r'^$', views.IndexView.as_view(), name='index'),

    re_path(r'^register/$', views.UserFormView.as_view(), name='register'),
    re_path(r'^login/$', views.UserLoginView.as_view(), name='login'),
    # re_path(r'^logout/', views.logout(), name='logout'),


    #/music/albumID
    re_path(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='details'),
    re_path(r'album/add/$', views.AlbumCreate.as_view(), name='album-add'),
    re_path(r'album/(?P<pk>[0-9]+)/$', views.AlbumUpdate.as_view(), name='album-update'),
    re_path(r'album/(?P<pk>[0-9]+)/delete/$', views.AlbumDelete.as_view(), name='album-delete'),
    re_path(r'album/add/song/$', views.SongCreate.as_view(), name='song-add'),
]
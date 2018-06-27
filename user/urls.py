from django.urls import path, re_path
from . import views

app_name = 'user'

urlpatterns = [
    #/music/
    re_path(r'^$', views.IndexView.as_view(), name='index'),

    re_path(r'^register/$', views.UserFormView.as_view(), name='register'),
    re_path(r'^login/$', views.UserLoginView.as_view(), name='login'),
    re_path(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    # re_path(r'^logout/', views.logout(), name='logout'),


    #/music/albumID
    re_path(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='details'),
    re_path(r'^user/add/$', views.UserCreate.as_view(), name='user-add'),
    re_path(r'^user/(?P<pk>[0-9]+)/$', views.UserUpdate.as_view(), name='user-update'),
    re_path(r'^user/(?P<pk>[0-9]+)/delete/$', views.UserDelete.as_view(), name='user-delete'),
    re_path(r'^user/add/song/$', views.SongCreate.as_view(), name='song-add'),
]
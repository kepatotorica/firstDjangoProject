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
    re_path(r'^user/add/$', views.PicCreate.as_view(), name='user-post'),
    re_path(r'^user/(?P<pk>[0-9]+)/$', views.ProfileUpdate.as_view(), name='user-update'),
    re_path(r'^user/priv/(?P<pk>[0-9]+)/$', views.PrivProfileUpdate.as_view(), name='priv-user-update'),
    re_path(r'^user/(?P<pk>[0-9]+)/delete/$', views.userDelete.as_view(), name='user-delete'),
    re_path(r'^user/add/friend/$', views.PicCreate.as_view(), name='pic-add'),
    re_path(r'^connect/(?P<operations>.*)/(?P<pk>[0-9]+)/$', views.change_friends, name='change_friends'),
    re_path(r'^friends/$', views.FriendView.as_view(), name='friends'),
    re_path(r'^processRec/$', views.processRec, name='processRec'),
]
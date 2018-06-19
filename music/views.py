from django.shortcuts import render
from django.http import HttpResponse
from .models import Album
# Create your views here.

def index(request):
    all_albums = Album.objects.all()
    html = ''
    for album in all_albums:
        url = '/music/'+ str(album.id) + '/'
        html += '<a href="' + url + '">' + album.album_title + '</a><br>'
    return HttpResponse(html)

def view_id(request, album_id):
    return HttpResponse("<h2>Album id: " + str(album_id) + "</h2>")

def view_albums(request):
    return HttpResponse("nothing yet")

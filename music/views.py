from django.shortcuts import render
from django.http import HttpResponse
from .models import Album
from django.template import loader
# Create your views here.

def index(request):
    all_albums = Album.objects.all()
    template = loader.get_template('music/index.html')
    context = {
        'all_albums': all_albums,
    }
    return HttpResponse(template.render(context, request))

def view_id(request, album_id):
    return HttpResponse("<h2>Album id: " + str(album_id) + "</h2>")

def view_albums(request):
    return HttpResponse("nothing yet")

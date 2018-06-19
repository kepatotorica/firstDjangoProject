from django.http import Http404
from .models import Album, Song
from django.shortcuts import render

def index(request):
    all_albums = Album.objects.all()
    context = {'all_albums': all_albums,}
    return render(request, 'music/index.html',context)

def view_id(request, album_id):
    try:
        all_songs = Song.objects.all()
        album = Album.objects.get(id=album_id)
    except Album.DoesNotExist:
        raise Http404('oops that album doesn\'t exists')
    context = {
        'album': album,
        'all_songs': all_songs,
    }
    return render(request, 'music/details.html',context)
   #"<a href=\"../\">back to albums<a/>")
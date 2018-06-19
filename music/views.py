from .models import Album, Song
from django.shortcuts import render, get_object_or_404

def index(request):
    all_albums = Album.objects.all()
    context = {'all_albums': all_albums,}
    return render(request, 'music/index.html',context)

def view_id(request, album_id):

    album = get_object_or_404(Album, pk=album_id)
    context = {'album': album,}
    return render(request, 'music/details.html',context)
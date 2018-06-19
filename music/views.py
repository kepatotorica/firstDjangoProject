from django.shortcuts import render, get_object_or_404
from .models import Album, Song

def index(request):
    all_albums = Album.objects.all()
    context = {'all_albums': all_albums,}
    return render(request, 'music/index.html',context)

def view_id(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    context = {'album': album}
    return render(request, 'music/details.html', context)

def favorite(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        selected_song = album.song_set.get(pk=request.POST['song'])
    except (KeyError, Song.DoesNotExist):
        return render(request, 'music/details.html', {
            'album': album,
            'error_message': "this isn't a valid song",
        })
    else:
        if selected_song.is_favorite == False:
            selected_song.is_favorite = True
        else:
            selected_song.is_favorite = False
        selected_song.save()
        return render(request, 'music/details.html', {'album': album})

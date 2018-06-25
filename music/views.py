from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Album, Song

class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_albums'

    def get_queryset(self):
        return Album.objects.all()

class DetailView(generic.DetailView):
    model = Album #the template we are using
    template_name = 'music/details.html'

class AlbumCreate(CreateView):
    model = Album
    fields = ['artist', 'album_title','genre', 'album_logo']

class AlbumUpdate(UpdateView):
     model = Album
     fields = ['artist', 'album_title', 'genre', 'album_logo']

class AlbumDelete(DeleteView):
         model = Album
         success_url = reverse_lazy('music:index')

class SongCreate(CreateView):
    model = Song
    fields = ['album', 'file_type', 'song_title', 'is_favorite']
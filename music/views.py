from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Album, Song
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm, LoginForm

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

class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

    #display a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    #proces form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            #cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password) #this is the only way to change a password because of hashing
            user.save()

            #returns the User obejects if credintials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('music:index')


        return render(request, self.template_name,{'form': form})


class UserLoginView(View):
    form_class = LoginForm
    template_name = 'music/login_form.html'

    #display a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    #proces form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            # user = form.save(commit=False)

            #cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # user.set_password(password) #this is the only way to change a password because of hashing

            #returns the User obejects if credintials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('music:index')


        return render(request, self.template_name,{'form': form})
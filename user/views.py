from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import User as users, Song
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm, LoginForm

class IndexView(generic.ListView):
    template_name = 'user/index.html'
    context_object_name = 'all_users'

    def get_queryset(self):
        return users.objects.all()

class DetailView(generic.DetailView):
    model = users #the template we are using
    template_name = 'user/details.html'

class UserCreate(CreateView):
    model = users
    fields = ['name', 'user_title', 'user_logo']

class UserUpdate(UpdateView):
     model = users
     fields = ['name', 'user_title', 'user_logo']

class UserDelete(DeleteView):
         model = users
         success_url = reverse_lazy('user:index')

class SongCreate(CreateView):
    model = Song
    fields = ['user', 'file_type', 'song_title', 'is_favorite']

class UserFormView(View):
    form_class = UserForm
    template_name = 'user/registration_form.html'

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
                    return redirect('user:index')


        return render(request, self.template_name,{'form': form})


class UserLoginView(View):
    form_class = LoginForm
    template_name = 'user/login_form.html'

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
                    return redirect('user:index')


        return render(request, self.template_name,{'form': form})

class LogoutView(View):

     def get(self, request):
        logout(request)
        return redirect('user:index')

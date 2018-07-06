from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Prof, Pic
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm, LoginForm, UserUpdateForm
from django.contrib.auth.models import User


class IndexView(generic.ListView):
    template_name = 'user/index.html'
    context_object_name = 'all_users'
    print('we are printing in index')
    def get_queryset(self):
        print('we are printing in index query')
        return User.objects.all()

class DetailView(generic.DetailView):
    model = Prof #the template we are using IS THIS RIGHT OR SHOULD IT BE Prof OR User.prof
    print('we are printing')
    template_name = 'user/details.html'

class FriendCreate(CreateView):
    model = Prof
    fields = ['handle', 'bio', 'profile_picture']

class ProfileUpdate(UpdateView):
     model = Prof
     fields = ['handle', 'bio', 'profile_picture']


class PrivProfileUpdate(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'user/user_form.html'

    def form_valid(self, form):
        user = form.save(commit=True)
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        return redirect('user:index')

class FriendDelete(DeleteView):
         model = Prof
         success_url = reverse_lazy('user:index')

class PicCreate(CreateView):
    model = Pic
    fields = ['friend', 'file_type', 'pic_name', 'is_favorite']

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

            #returns the Prof obejects if credintials are correct
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

            #returns the Prof obejects if credintials are correct
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

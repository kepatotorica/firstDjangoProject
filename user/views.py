from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Prof, Pic, Friend
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, TemplateView
from .forms import UserForm, LoginForm, UserUpdateForm
from django.contrib.auth.models import User
from django import forms
from user import models


class IndexView(generic.ListView):
    template_name = 'user/index.html'
    context_object_name = 'all_users'

    def get_queryset(self):
        return User.objects.all()


class DetailView(generic.DetailView):
    model = Prof  # the template we are using IS THIS RIGHT OR SHOULD IT BE Prof OR User.prof
    template_name = 'user/details.html'

    def get(self, request, pk, *args, **kwargs):
        try:
            self.object = self.get_object()
        except:
            return redirect('user:index')
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class PicCreate(CreateView):
    model = Pic  # TODO force the upload to go to the logged in user
    fields = ['prof', 'pic_desc', 'pic_name', 'pic_publicity', 'picture']


class ProfileUpdate(UpdateView):
    model = Prof
    fields = ['privacy_level', 'bio', 'profile_picture']

    def get(self, request, pk, *args, **kwargs):
        try:
            prof = Prof.objects.get(id=self.kwargs['pk'])
            print(prof)
            return redirect('user:index')
        except:
            return redirect('user:index')

    def get_form(self, form_class=None):
        form = super(ProfileUpdate, self).get_form(form_class)
        prof = Prof.objects.get(id=self.kwargs['pk'])
        # read in the profile from the query key
        form.fields['bio'].required = False
        form.fields['bio'].initial = 'hey'
        return form


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


class userDelete(DeleteView):
    model = Prof
    success_url = reverse_lazy('user:index')


class UserFormView(View):
    form_class = UserForm
    template_name = 'user/registration_form.html'

    # display a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # proces form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)  # this is the only way to change a password because of hashing
            user.save()

            # returns the Prof obejects if credintials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.session['user_id'] = user.pk
                    return redirect('user:index')

        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    form_class = LoginForm
    template_name = 'user/login_form.html'

    # display a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # proces form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            # user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # user.set_password(password) #this is the only way to change a password because of hashing

            # returns the Prof obejects if credintials are correct
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.session['user_id'] = user.pk
                    request.session['logged_in_user_id'] = user.id
                    return redirect('user:index')

        return render(request, self.template_name, {'form': form})


class LogoutView(View):

    def get(self, request):
        logout(request)
        request.session.clear()
        return redirect('user:index')


def change_friends(request, operations, pk):
    new_friend = User.objects.get(pk=pk)
    # Friend.makeFriend(request.Prof, new_friend)
    # Friend.makeFriend(request.log_prof, new_friend)
    print("======data passed in======")
    print(operations)
    print(pk)
    print(new_friend)
    if operations == 'add':
        Friend.makeFriend(request.user, new_friend)
    elif operations == 'remove':
        Friend.removeFriend(request.user, new_friend)
    return redirect('user:index')


# class friendsView(generic.DetailView):
#     model = Friend #the template we are using IS THIS RIGHT OR SHOULD IT BE Prof OR User.prof
#     template_name = 'user/friends.html'
#
#     def get(self, request, pk, *args, **kwargs):
#         try:
#             self.object = self.get_object()
#             print("\n==================")
#             print(self.object)
#             # prof = Prof.objects.get(id=self.kwargs['pk'])
#             print("==================\n")
#         except:
#             return redirect('user:index')
#         context = self.get_context_data(object=self.object)
#         return self.render_to_response(context)

class FriendView(TemplateView):
    template_name = "user/friends.html"


    def get(self, request, *args, **kwargs):
        try:
            self.object = Friend.objects.get_or_create(current_user=request.user)
        except:
            return redirect('user:index')
        context = self.get_context_data(object=self.object)
        context['friendList'] = self.object
        return self.render_to_response(context)


    #
    # def get_context_data(self, **kwargs):
    #     friends = Friend.objects.get_or_create(current_user=User.objects.get(pk=1))
    #     # print(self.request)
    #     context = super().get_context_data(**kwargs)
    #
    #     context['latest_articles'] = Friend.objects.all()
    #     return context

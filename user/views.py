from django.http import JsonResponse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Prof, Pic, Friend
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, TemplateView
from .forms import UserForm, LoginForm, UserUpdateForm, ProfUpdateForm, PicForm
from django.contrib.auth.models import User
from django import forms
from user import models

# numpy, pandas, sklearn
import numpy as np
import pandas as pd
# importing train_test_split
from sklearn.model_selection import train_test_split
# import KNeighborsClassifier
from sklearn.neighbors import KNeighborsClassifier
# import confusion_matrix
from sklearn.metrics import confusion_matrix
# import GridSearchCV
from sklearn.model_selection import GridSearchCV
# import classification_reportD
from sklearn.metrics import classification_report
# import classification_report
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score


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

        if not request.user.is_authenticated:
            return self.render_to_response(context)
        context['friendList'] = Friend.objects.get_or_create(current_user=request.user)
        context['friends'] = False
        print(context['friendList'])
        loggedIn = Prof.objects.get(id=self.kwargs['pk'])
        # print(request.user)
        # print(loggedIn.user)
        user = loggedIn.user
        if user.friend_set.filter(current_user=request.user).exists():
            context['friends'] = True
        print(context['friends'])
        return self.render_to_response(context)


# class PicCreate(CreateView):
#     form_class = PicForm
#     model = Pic
#
#     def get_form_kwargs(self):
#         kwargs = super(PicCreate, self).get_form_kwargs()
#         # kwargs.update({'pk': self.kwargs.get('pk')})
#         return kwargs

class PicCreate(CreateView):
    model = Pic  # TODO force the upload to go to the logged in user
    form_class = PicForm
    template_name = 'user/pic_form.html'


    def get(self, request, *args, **kwargs):
        form = PicForm()
        try:
            prof = Prof.objects.get(id=request.session['user_id'])
            if prof.privacy_level:
                priv = '0'
            else:
                priv = prof.privacy_level
            form = PicForm(initial={
                'prof': prof,
                'pic_publicity': priv,
                })
            print(request.log_prof)
            return render(request, self.template_name, context={'form': form})
        except:
           return render(request, self.template_name, context={'form': form})
    # fields = ['prof', 'pic_desc', 'pic_name', 'pic_publicity', 'picture']


class ProfileUpdate(UpdateView):
    model = Prof
    form_class = ProfUpdateForm
    template_name = 'user/prof_form.html'

    # we may be able to do something about recommendation with a post
    # def post(self, request, pk, *args, **kwargs):
    #     try:
    #         prof = Prof.objects.get(id=self.kwargs['pk'])
    #         form = ProfUpdateForm(initial={
    #             'privacy_level': prof.privacy_level,
    #             'bio': prof.bio,
    #             'profile_picture': prof.profile_picture,
    #             })
    #         return render(request, self.template_name, context={'form': form})
    #     except:
    #        return render(request, self.template_name, context={'form': form})

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
                    return redirect('user:user-update', str(user.id))

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
                    return redirect('user:details', str(user.id))

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
    print(request.user)
    if operations == 'add':
        Friend.makeFriend(request.user, new_friend)
        # Friend.makeFriend(new_friend, request.user)
    elif operations == 'remove':
        Friend.removeFriend(request.user, new_friend)
        # Friend.removeFriend(new_friend, request.user)
    return redirect('user:details', new_friend.id)



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

def processRec(request):
    user_preference = request.GET.get('user_preference', None)
    sentiment = request.GET.get('sentiment', None)
    sensitivity = request.GET.get('sensitivity', None)
    relationship = request.GET.get('relationship', None)
    fieldData = request.GET.get('fieldData', None)
    print(request.GET)

    print("user pref: " + user_preference)
    print("sentiment: " + sentiment)
    print("sensitivity: " + sensitivity)
    print("relationship: " + relationship)
    print("fieldData: " + fieldData)

    ######## start of recommender system

    # Load the dataset
    # /../../processRec/
    # df = pd.read_csv('/../../more_processed_policy_selections.csv/')
    df = pd.read_csv('/Users/devankarsann/Desktop/helpingKepa2/firstDjangoProject/user/more_processed_policy_selections.csv')

    X = df.drop('Policy',axis=1).values
    y = df['Policy'].values

    # X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.4,random_state=42, stratify=y)

    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.01, random_state=42)

    # Setup arrays to store training and test accuracies
    neighbors = np.arange(1,9)
    train_accuracy = np.empty(len(neighbors))
    test_accuracy = np.empty(len(neighbors))

    for i,k in enumerate(neighbors):
        # Setup a knn classifier with k neighbors
        knn = KNeighborsClassifier(n_neighbors=k)

        # Fit the model
        knn.fit(X_train, y_train)

        # Compute accuracy on the training set
        train_accuracy[i] = knn.score(X_train, y_train)

        # Compute accuracy on the test set
        test_accuracy[i] = knn.score(X_test, y_test)


    # Setup a knn classifier with k neighbors
    knn = KNeighborsClassifier(n_neighbors=7)

    # Fit the model
    knn.fit(X_train,y_train)

    # Get accuracy. Note: In case of classification algorithms score method represents accuracy.
    knn.score(X_test,y_test)

    # let us get the predictions using the classifier we had fit above
    # y_pred = knn.predict(X_test)
    # print(y_pred)
    # print(y_pred[0])

    # recommender system
    # 1 is everyone
    # 2 is friends
    # 3 is nobody

    # website
    # 0 is me
    # 1 is friends
    # 2 is everyone

    if relationship == 0:
        relationship = 3
    elif relationship == 1:
        relationship = 2
    else:
        relationship = 1

    test_input = [[sensitivity, sentiment, relationship]]
    test_input_pred = knn.predict(test_input)
    # print(test_input_pred)
    print('recommendation generated: ' + test_input_pred[0])

    '''
    PRIVACY_LEVELS = (
        ('0', 'Just Me'), = c
        ('1', 'Friends'), = b
        ('2', 'Everyone'), = a
    )
    '''

    ######## end of recommender system

    # finalRec = user_preference;
    finalRec = test_input_pred[0]

    if finalRec == 'a':
        finalRec = 2
    elif finalRec == 'b':
        finalRec = 1
    else: # 'c'
        finalRec = 0

    data = {
        'rec': finalRec
    }
    return JsonResponse(data)


#     what is the problem we want to solve
#
# the technical aspeccts of the website, and the backround rec
#
# where we will go from here, the plan to finish it up
# 	-aka automatically parsing meaning from a picture
#
# layout an evaluation plan
# 	-aka diffrernt recomendation plans
# 	-how will we evaluate the tool
# 	-what would be the logistical challanges for the study
# 	-what will we measure
# 	-what hypothisis do we have
# 	-this is based on if it is completed
# 	-how will the tool enable research
#

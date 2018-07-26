from django.contrib.auth.models import User
from django import forms
from .models import Prof

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Prof
#         fields = ('privacy_level', 'bio', 'profile_picture')


class ProfForm(forms.ModelForm):

    class Meta:
        model = Prof
        fields = ['privacy_level', 'bio', 'profile_picture']

        # def __init__(self, *args, **kwargs):
        #     print('aye')
        #     self.request = kwargs.pop('request', None)
        #
        #     products = kwargs['instance'].products.all()
        #
        #     self.bio = "please"
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    fields = ['username', 'password']


class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']


# class picUpload
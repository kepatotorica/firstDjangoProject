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




class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    fields = ['username', 'password']



class ProfUpdateForm(forms.ModelForm):
    bio = forms.CharField(label="Tell me about yourself", widget=forms.TextInput(attrs={"value":"asdf"}))
    class Meta:
        model = Prof
        fields = ['privacy_level', 'bio', 'profile_picture']

class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']


# class picUpload
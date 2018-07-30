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
    print("hey")
    class Meta:
        model = Prof
        fields = ['privacy_level', 'bio', 'profile_picture']

class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']


# class BazForm(models.ModelForm):
#     model = Baz
#     fields = ['bar', ...]
#
#     def __init__(self, *args, **kwargs):
#         foo_id = kwargs.pop('foo_id')
#         super(BazForm, self).__init__(*args, **kwargs)
#         self.fields['bar'].queryset = Bar.objects.filter(foo_id=foo_id)

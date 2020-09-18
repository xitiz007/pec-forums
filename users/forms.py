from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Faculty
from django.db.models import ForeignKey, CASCADE

class AuthenticationForm(forms.Form):
    email = forms.EmailField(widget= forms.TextInput(attrs={
        'class': 'form-control','type':'text','name': 'email'
    }),
    label= 'Email')
    password = forms.CharField(widget= forms.PasswordInput(attrs={
        'class': 'form-control','type':'password','name': 'password'
    }),
    label= 'Password')

    class Meta:
        fields= ['email', 'password']

class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(required= True)
    last_name = forms.CharField(required= True)
    email = forms.EmailField(required= True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

class ChooseFaculty(forms.Form):
    choices = [(instance, instance) for instance in Faculty.objects.all() ]
    faculty = forms.ChoiceField(choices= choices, required= True, label='Select your faculty')

class ChangeUserProfileModel(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'faculty']
        labels = {
            'profile_picture' : 'Profile picture',
            'faculty' : 'My Faculty'
        }

class ChangeUserModel(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required= True)
    last_name = forms.CharField(max_length=150, required= True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name']
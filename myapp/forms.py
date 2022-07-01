import email
from faulthandler import disable
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django import forms


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'align':'center','placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'align':'center','placeholder': 'Confirm Password'}),
    )
    class Meta:
        model = User 
        fields = ['name','email']
        widgets = { 
            "name":forms.TextInput(attrs={'class':'form-control','placeholder': 'Name'}),
            "email":forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter Email'}),
        }

class LoginForm(forms.Form):
    email =forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password= forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))



class PasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'align':'center'}),
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'align':'center'}),    
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'align':'center'}),    
    )




class ProfileForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), disabled=True)
    class Meta:
        model = User
        fields = ['name','email','phone','gender','address','profile','bio']
        widgets = { 
            "name":forms.TextInput(attrs={'class':'form-control'}),
            "phone":forms.TextInput(attrs={'class':'form-control'}),
            "gender":forms.Select(attrs={'class':'form-control'}),
            "role":forms.Select(attrs={'class':'form-control'}),
            "address":forms.TextInput(attrs={'class':'form-control'}),
            "bio":forms.TextInput(attrs={'class':'form-control'}),
        }


class CreatepostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['image','caption']
        widgets={
            'image':forms.FileInput(attrs={'class':'form-control'}),
            'caption':forms.Textarea(attrs={'class':'form-control'}),
        }

class EditpostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['caption']
        widgets={
            'caption':forms.TextInput(attrs={'class':'form-control'}),
        }
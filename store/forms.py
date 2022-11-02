from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from .models import User
from django.forms import ModelForm
from django import forms
from django.contrib.auth import password_validation

class UserCreationForm(UserCreationForm):
    class Meta:
       model=User
       fields=['username','email','password1','password2']



class PasswordChangeCustomForm(PasswordChangeForm):
        
    old_password = forms.CharField(required=True, label='Old Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'})),
                      

    new_password1 = forms.CharField(required=True, label='New Password',
                      widget=forms.PasswordInput(attrs={
                        'class': 'form-control'}),
                        help_text=password_validation.password_validators_help_text_html()),
                     
    new_password2 = forms.CharField(required=True, label='Confirm Password',
                      widget=forms.PasswordInput(attrs={
                        'class': 'form-control'})),
                      
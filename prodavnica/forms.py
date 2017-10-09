from django import forms
from django.contrib.auth.models import User
from django import forms
from . import models

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=['username','email','password']


class SearchForm(forms.Form):
    naziv_artikla = forms.CharField(required=False)

class UploadFileForm(forms.Form):
    file = forms.ImageField()

class RegisterForm(forms.Form):
    username = forms.CharField(min_length=5,max_length=30,widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(min_length=5,max_length=30,widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(min_length=5,max_length=30,widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(min_length=5,max_length=30,widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(min_length=5,max_length=30,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    repeat_password = forms.CharField(min_length=5,max_length=30,widget = forms.PasswordInput(attrs={'class':'form-control'}))
    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data.get('username')).count() > 0:
            raise forms.ValidationError("Username je zauzet")
        return self.cleaned_data.get('username')

    def clean_repeat_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('repeat_password')

        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2
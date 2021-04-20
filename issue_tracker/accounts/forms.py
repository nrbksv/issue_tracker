from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm, Textarea, widgets, TextInput, EmailInput, ImageField, URLInput

from accounts.models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=100, required=True, widget=widgets.EmailInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'email', 'first_name', 'last_name']

        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
            }),
            'first_name': TextInput(attrs={
                'class': 'form-control',
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        if not first_name and not last_name:
            self.add_error('first_name', 'Одно из этих двух полей должно быть заполнено')
            self.add_error('last_name', 'Одно из этих двух полей должно быть заполнено')
        return cleaned_data


class UserChangeForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']

        widgets = {
            'first_name': TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control'
            }),
            'email': EmailInput(attrs={
                'class': 'form-control'
            }),
        }


class ProfileChangeForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

        widgets = {
            'git_hub': URLInput(attrs={
                'class': 'form-control'
            }),
            'about': Textarea(attrs={
                'class': 'form-control'
            }),
        }

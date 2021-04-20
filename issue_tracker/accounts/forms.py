from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm, Textarea, widgets, TextInput, EmailInput, URLInput

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


class PasswordChangeForm(ModelForm):
    old_password = forms.CharField(label='Старый пароль', strip=False, widget=forms.PasswordInput)
    password = forms.CharField(label='Новый пароль', strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Подтвердите пароль', strip=False, widget=forms.PasswordInput)

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают')
        return password_confirm

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.instance.check_password(old_password):
            raise forms.ValidationError('Старый пароль неправильный')
        return old_password

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ['old_password', 'password', 'password_confirm']

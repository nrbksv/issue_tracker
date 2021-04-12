from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import widgets, TextInput


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

from django.forms import ModelForm, TextInput, Select, Textarea, CheckboxSelectMultiple, widgets, DateInput, modelformset_factory
from django import forms

from tracker.models import Issue, Project


class ProjectIssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['status', 'types', 'summary', 'description']

        widgets = {
            'status': Select(attrs={
                'class': 'form-control'
            }),
            'types': CheckboxSelectMultiple(attrs={
                'class': 'list-unstyled'
            }),
            'summary': TextInput(attrs={
                'class': 'form-control'
            }),
            'description': Textarea(attrs={
                'class': 'form-control'
            })
        }


class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['project', 'status', 'types', 'summary', 'description']

        widgets = {
            'project': Select(attrs={
                'class': 'form-control'
            }),
            'status': Select(attrs={
                'class': 'form-control'
            }),
            'types': CheckboxSelectMultiple(attrs={
                'class': 'list-unstyled'
            }),
            'summary': TextInput(attrs={
                'class': 'form-control'
            }),
            'description': Textarea(attrs={
                'class': 'form-control'
            })
        }


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['project', 'project_description', 'date_start', 'date_finish']

        widgets = {
            'project': TextInput(attrs={
                'class': 'form-control'
            }),
            'project_description': Textarea(attrs={
                'class': 'form-control'
            }),
            'date_start': DateInput(attrs={
                'class': 'form-control'
            }),
            'date_finish': DateInput(attrs={
                'class': 'form-control'
            })
        }


class SearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=widgets.TextInput(
            attrs={
                'style': 'width: 100%;',
                'placeholder': 'Поиск'
            }
        )
    )

from django.forms import ModelForm, TextInput, Select, Textarea, CheckboxSelectMultiple

from tracker.models import Issue


class IssueForm(ModelForm):
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

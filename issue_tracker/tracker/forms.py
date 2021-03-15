from django.forms import widgets
from django import forms


from tracker.models import Issue, Status, Type


class IssueForm(forms.Form):
    model = Issue
    status = forms.ModelChoiceField(queryset=Status.objects.all(), empty_label=None, required=True, widget=widgets.Select(attrs={'class': 'form-control'}), label='Статус')
    type_issue = forms.ModelMultipleChoiceField(queryset=Type.objects.all(), required=True, widget=widgets.CheckboxSelectMultiple(attrs={'class': 'list-unstyled'}), label='Тип')
    summary = forms.CharField(max_length=300, required=True, widget=widgets.TextInput(attrs={'class': 'form-control'}), label='Заголовок')
    description = forms.CharField(max_length=3000, widget=widgets.Textarea(attrs={'class': 'form-control'}), required=False, label='Описание')
from django.forms import widgets
from django import forms


from tracker.models import Issue, Status, Type


class IssueForm(forms.Form):
    model = Issue
    status = forms.ModelChoiceField(queryset=Status.objects.all(), required=True, label='Статус')
    type_issue = forms.ModelChoiceField(queryset=Type.objects.all(), required=True, label='Тип')
    summary = forms.CharField(max_length=300, required=True, label='Заголовок')
    description = forms.CharField(max_length=3000, widget=widgets.Textarea, required=False, label='Описание')
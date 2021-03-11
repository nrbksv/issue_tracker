from django.shortcuts import render
from django.views.generic import TemplateView

from tracker.models import Issue, Status, Type


class IssueListView(TemplateView):
    template_name = 'issues_list.html'

    def get_context_data(self, **kwargs):
        kwargs['issues'] = Issue.objects.all()
        return super().get_context_data(**kwargs)


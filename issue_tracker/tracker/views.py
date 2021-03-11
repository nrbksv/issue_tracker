from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from tracker.models import Issue, Status, Type


class IssueListView(TemplateView):
    template_name = 'issues_list.html'

    def get_context_data(self, **kwargs):
        kwargs['issues'] = Issue.objects.all()
        return super().get_context_data(**kwargs)


class IssueDetail(TemplateView):
    template_name = 'issue_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['issue'] = get_object_or_404(Issue, id=kwargs.get('pk'))
        return super().get_context_data(**kwargs)



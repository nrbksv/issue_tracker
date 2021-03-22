from datetime import datetime, timedelta

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import TemplateView, View, FormView
from django.db.models import Q, F, Count

from tracker.models import Issue
from tracker.forms import IssueForm


class IssueListView(TemplateView):
    template_name = 'issues_list.html'

    def get_context_data(self, **kwargs):
        kwargs['issues'] = Issue.objects.all()
        return super().get_context_data(**kwargs)


class IssueFilteredListView(TemplateView):
    template_name = 'issues_list.html'

    def get_context_data(self, **kwargs):
        f = kwargs.get('filter')
        if f == 'all':
            f = Issue.objects.all()
        elif f == 'filter_1':
            f = Issue.objects.filter(updated_at__gt=datetime.now()-timedelta(days=30), status__status__iexact='Сделано')
        elif f == 'filter_2':
            f = Issue.objects.filter(types__type_issue__in=['Ошибка', 'Улучшение'], status__status__in=['Сделано', 'Новый']).distinct()
        elif f == 'filter_3':
            f = Issue.objects.filter(Q(Q(types__type_issue__iexact='Ошибка') | Q(summary__icontains='bug')) & ~Q(status__status__iexact='Сделано')).distinct()
        elif f == 'filter_4':
            f = Issue.objects.filter(summary__iexact=F('description'))
        kwargs['issues'] = f
        return super().get_context_data(**kwargs)


class IssueDetail(TemplateView):
    template_name = 'issue_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['issue'] = get_object_or_404(Issue, id=kwargs.get('pk'))
        return super().get_context_data(**kwargs)


class NewIssue(FormView):
    template_name = 'new_issue.html'
    form_class = IssueForm

    def form_valid(self, form):
        self.issue = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('issue-detail', kwargs={'pk': self.issue.pk})


class IssueUpdate(FormView):
    template_name = 'issue_update.html'
    form_class = IssueForm

    def dispatch(self, request, *args, **kwargs):
        self.issue = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issue'] = self.issue
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.issue
        return kwargs

    def form_valid(self, form):
        self.issue = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('issue-detail', kwargs={'pk': self.issue.id})

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Issue, id=pk)


class IssueDelete(View):
    def post(self, request, pk):
        issue = get_object_or_404(Issue, id=pk)
        issue.delete()
        return redirect('issues-list')

from django.shortcuts import get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, FormView, UpdateView, DeleteView
from django.db.models import Q


from tracker.models import Issue
from tracker.forms import IssueForm
from tracker.base_views import SearchView


class IssueListView(SearchView):
    template_name = 'issues/list.html'
    model = Issue
    context_object_name = 'issues'
    paginate_by = 10

    def get_query(self):
        query = Q(summary__icontains=self.search_value) | Q(description__icontains=self.search_value)
        return query


class IssueDetail(TemplateView):
    template_name = 'issues/detail.html'

    def get_context_data(self, **kwargs):
        kwargs['issue'] = get_object_or_404(Issue, id=kwargs.get('pk'))
        return super().get_context_data(**kwargs)


class NewIssue(FormView):
    template_name = 'issues/create.html'
    form_class = IssueForm

    def form_valid(self, form):
        self.issue = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('issue-detail', kwargs={'pk': self.issue.pk})


class IssueUpdate(UpdateView):
    model = Issue
    template_name = 'issues/update.html'
    form_class = IssueForm
    context_object_name = 'issue'

    def get_success_url(self):
        return reverse('issue-detail', kwargs={'pk': self.kwargs.get('pk')})


class IssueDelete(DeleteView):
    template_name = 'partial/modal.html'
    model = Issue
    context_object_name = 'issue'
    success_url = reverse_lazy('issues-list')

from django.shortcuts import get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
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


class IssueDetail(DetailView):
    template_name = 'issues/detail.html'
    model = Issue

    def get_queryset(self):
        return super().get_queryset().filter(project__is_deleted=False)


class NewIssue(CreateView):
    template_name = 'issues/create.html'
    model = Issue
    form_class = IssueForm

    def get_success_url(self):
        return reverse('issue-detail', kwargs={'pk': self.object.pk})


class IssueUpdate(UpdateView):
    model = Issue
    template_name = 'issues/update.html'
    form_class = IssueForm
    context_object_name = 'issue'

    def get_success_url(self):
        return reverse('issue-detail', kwargs={'pk': self.kwargs.get('pk')})


class IssueDelete(DeleteView):
    model = Issue
    context_object_name = 'issue'
    success_url = reverse_lazy('issues-list')

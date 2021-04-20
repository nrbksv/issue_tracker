from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q


from tracker.models import Issue
from tracker.forms import IssueForm
from tracker.base_views import SearchView


class IssueListView(PermissionRequiredMixin, SearchView):
    template_name = 'issues/list.html'
    model = Issue
    context_object_name = 'issues'
    paginate_by = 10
    permission_required = 'tracker.view_issue'

    def get_query(self):
        query = Q(summary__icontains=self.search_value) | Q(description__icontains=self.search_value)
        return query


class IssueDetail(PermissionRequiredMixin, DetailView):
    template_name = 'issues/detail.html'
    model = Issue
    permission_required = 'tracker.view_issue'

    def has_permission(self):
        issue = get_object_or_404(Issue, pk=self.kwargs.get('pk'))
        return self.request.user in issue.project.users.all() and super().has_permission()

    def get_queryset(self):
        return super().get_queryset().filter(project__is_deleted=False)


class NewIssue(PermissionRequiredMixin, CreateView):
    template_name = 'issues/create.html'
    model = Issue
    form_class = IssueForm
    permission_required = 'tracker.add_issue'

    def form_valid(self, form):
        issue = form.save(commit=False)
        if self.request.user in issue.project.users.all():
            return super().form_valid(form)
        form.add_error('project', f'Вас в спике пользователей проекта: <<{form.cleaned_data.get("project")}>> нет.')
        return self.form_invalid(form)

    def get_success_url(self):
        return reverse('tracker:issue-detail', kwargs={'pk': self.object.pk})


class IssueUpdate(PermissionRequiredMixin, UpdateView):
    model = Issue
    template_name = 'issues/update.html'
    form_class = IssueForm
    context_object_name = 'issue'
    permission_required = 'tracker.change_issue'

    def has_permission(self):
        issue = get_object_or_404(Issue, pk=self.kwargs.get('pk'))
        return self.request.user in issue.project.users.all() and super().has_permission()

    def get_success_url(self):
        return reverse('tracker:issue-detail', kwargs={'pk': self.kwargs.get('pk')})


class IssueDelete(PermissionRequiredMixin, DeleteView):
    model = Issue
    context_object_name = 'issue'
    success_url = reverse_lazy('tracker:issues-list')
    permission_required = 'tracker.delete_issue'

    def has_permission(self):
        issue = get_object_or_404(Issue, pk=self.kwargs.get('pk'))
        return self.request.user in issue.project.users.all() and super().has_permission()
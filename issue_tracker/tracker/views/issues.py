from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import TemplateView, View, FormView
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


class IssueUpdate(FormView):
    template_name = 'issues/update.html'
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

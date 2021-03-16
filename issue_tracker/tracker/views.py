from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import TemplateView, View, FormView

from tracker.models import Issue
from tracker.forms import IssueForm


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


class NewIssue(FormView):
    template_name = 'new_issue.html'
    form_class = IssueForm

    def form_valid(self, form):
        self.issue = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('issue-detail', kwargs={'pk': self.issue.pk})


class IssueUpdate(View):
    def get(self, request, pk):
        issue = get_object_or_404(Issue, id=pk)
        form = IssueForm(initial={
            'status': issue.status,
            'type_issue': issue.types.all(),
            'summary': issue.summary,
            'description': issue.description
        })
        return render(request, 'issue_update.html', {'form': form, 'issue': issue})

    def post(self, request, pk):
        issue = get_object_or_404(Issue, id=pk)
        form = IssueForm(data=request.POST)
        if form.is_valid():
            types = form.cleaned_data.pop('type_issue')
            issue.status = form.cleaned_data.get('status')
            issue.summary = form.cleaned_data.get('summary')
            issue.description = form.cleaned_data.get('description')
            issue.save()
            issue.types.set(types)
            return redirect('issue-detail', pk=issue.id)
        return render(request, 'issue_update.html', {'form': form})


class IssueDelete(View):
    def post(self, request, pk):
        issue = get_object_or_404(Issue, id=pk)
        issue.delete()
        return redirect('issues-list')

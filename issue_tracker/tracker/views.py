from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View

from tracker.models import Issue, Status, Type
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


class NewIssue(View):

    def get(self, request):
        form = IssueForm()
        return render(request, 'new_issue.html', {'form': form})

    def post(self, request):
        form = IssueForm(data=request.POST)
        if form.is_valid():
            types = form.cleaned_data.pop('type_issue')
            issue = Issue.objects.create(
                status=form.cleaned_data.get('status'),
                summary=form.cleaned_data.get('summary'),
                description=form.cleaned_data.get('description')
            )
            issue.types.set(types)
            return redirect('issue-detail', pk=issue.id)
        return render(request, 'new_issue.html', {'form': form})


class IssueUpdate(View):
    def get(self, request, pk):
        issue = get_object_or_404(Issue, id=pk)
        form = IssueForm(initial={
            'status': issue.status,
            'type_issue': issue.type_issue,
            'summary': issue.summary,
            'description': issue.description
        })
        return render(request, 'issue_update.html', {'form': form, 'issue': issue})

    def post(self, request, pk):
        issue = get_object_or_404(Issue, id=pk)
        form = IssueForm(data=request.POST)
        if form.is_valid():
            issue.status=form.cleaned_data.get('status')
            issue.type_issue=form.cleaned_data.get('type_issue')
            issue.summary=form.cleaned_data.get('summary')
            issue.description=form.cleaned_data.get('description')
            issue.save()
            return redirect('issue-detail', pk=issue.id)
        return render(request, 'issue_update.html', {'form': form})


class IssueDelete(View):
    def post(self, request, pk):
        issue = get_object_or_404(Issue, id=pk)
        issue.delete()
        return redirect('issues-list')
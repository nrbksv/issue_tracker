from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import get_object_or_404, reverse
from django.core.paginator import Paginator, Page

from tracker.models import Project
from tracker.forms import ProjectForm, ProjectIssueForm


class ProjectListView(ListView):
    template_name = 'projects/list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.all()


class ProjectDetailView(DetailView):
    template_name = 'projects/detail.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        paginator = Paginator(project.issues.all(), 5)
        page = self.request.GET.get('page')
        if page is None:
            page = 1
        context['issues'] = paginator.get_page(page)
        context['is_paginated'] = True
        context['page_obj'] = Page(project.issues.all(), int(page), paginator)
        return context


class ProjectCreateView(CreateView):
    template_name = 'projects/create.html'
    model = Project
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('project-detail', kwargs={'pk': self.object.pk})


class ProjectIssueCreate(CreateView):
    template_name = 'projects/create_issue.html'
    model = Project
    form_class = ProjectIssueForm

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        form.instance.project = project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('project-detail', kwargs={'pk': self.kwargs.get('pk')})


class ProjectUpdateView(UpdateView):
    template_name = 'projects/update.html'
    model = Project
    form_class = ProjectForm
    context_object_name = 'project'

    def get_success_url(self):
        return reverse('project-detail', kwargs={'pk': self.kwargs.get('pk')})


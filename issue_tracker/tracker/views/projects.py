from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.shortcuts import get_object_or_404, reverse, redirect
from django.core.paginator import Paginator, Page

from tracker.models import Project
from tracker.forms import ProjectForm, ProjectIssueForm, ProjectUserForm
from tracker.base_views import SoftDeleteView


class ProjectListView(ListView):
    template_name = 'projects/list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(is_deleted=False)


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
        context['form'] = ProjectUserForm()
        context['issues'] = paginator.get_page(page)
        context['is_paginated'] = True
        context['page_obj'] = Page(project.issues.all(), int(page), paginator)
        return context

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class ProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = 'projects/create.html'
    model = Project
    form_class = ProjectForm

    def form_valid(self, form):
        project = form.save()
        project.users.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tracker:project-detail', kwargs={'pk': self.object.pk})


class ProjectIssueCreate(LoginRequiredMixin, CreateView):
    template_name = 'projects/create_issue.html'
    model = Project
    form_class = ProjectIssueForm

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        form.instance.project = project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tracker:project-detail', kwargs={'pk': self.kwargs.get('pk')})


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'projects/update.html'
    model = Project
    form_class = ProjectForm
    context_object_name = 'project'

    def get_success_url(self):
        return reverse('tracker:project-detail', kwargs={'pk': self.kwargs.get('pk')})


class ProjectDeleteView(LoginRequiredMixin, SoftDeleteView):
    model = Project
    context_object_name = 'project'
    success_url = 'tracker:projects-list'


class ProjectUserAdd(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        for user_id in self.request.POST.getlist('users'):
            user = get_object_or_404(User, pk=user_id)
            project.users.add(user)
            project.save()

        return redirect('tracker:project-detail', pk=project.id)


class ProjectUserRemove(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        for user_id in self.request.POST.getlist('remove_list'):
            user = get_object_or_404(User, pk=user_id)
            if user != self.request.user:
                project.users.remove(user)
                project.save()

        return redirect('tracker:project-detail', pk=project.id)

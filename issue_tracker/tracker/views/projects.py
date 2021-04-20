from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import get_object_or_404, reverse
from django.core.paginator import Paginator

from tracker.models import Project
from tracker.forms import ProjectForm, ProjectIssueForm, ProjectUserForm
from tracker.base_views import SoftDeleteView


class ProjectListView(ListView):
    template_name = 'projects/list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(is_deleted=False)


class ProjectDetailView(PermissionRequiredMixin, DetailView):
    template_name = 'projects/detail.html'
    model = Project
    permission_required = 'tracker.view_project'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        issues = self.object.issues.all()
        paginator = Paginator(issues, self.paginate_by)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        context['form'] = ProjectUserForm(initial={'users': self.object.users.all()})
        context['page_obj'] = page
        context['issues'] = page.object_list
        context['is_paginated'] = page.has_other_pages()
        return context

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class ProjectCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'projects/create.html'
    model = Project
    form_class = ProjectForm
    permission_required = 'tracker.add_project'

    def form_valid(self, form):
        project = form.save()
        project.users.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tracker:project-detail', kwargs={'pk': self.object.pk})


class ProjectIssueCreate(PermissionRequiredMixin, CreateView):
    template_name = 'projects/create_issue.html'
    model = Project
    form_class = ProjectIssueForm
    permission_required = 'tracker.add_issue'

    def has_permission(self):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        if not self.request.user.groups.filter(name='Project manager'):
            return self.request.user in project.users.all() and super().has_permission()
        return super().has_permission()

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        form.instance.project = project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tracker:project-detail', kwargs={'pk': self.kwargs.get('pk')})


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'projects/update.html'
    model = Project
    form_class = ProjectForm
    context_object_name = 'project'
    permission_required = 'tracker.change_project'

    def has_permission(self):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        if not self.request.user.groups.filter(name='Project manager'):
            return self.request.user in project.users.all() and super().has_permission()
        return super().has_permission()

    def get_success_url(self):
        return reverse('tracker:project-detail', kwargs={'pk': self.kwargs.get('pk')})


class ProjectDeleteView(PermissionRequiredMixin, SoftDeleteView):
    model = Project
    context_object_name = 'project'
    success_url = 'tracker:projects-list'
    permission_required = 'tracker.delete_project'


class ProjectUsersUpdate(PermissionRequiredMixin, UpdateView):
    template_name = None
    form_class = ProjectUserForm
    model = Project
    permission_required = 'tracker.project_user_update'

    def has_permission(self):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        return self.request.user in project.users.all() and super().has_permission()

    def get_success_url(self):
        return reverse('tracker:project-detail', kwargs={'pk': self.kwargs.get('pk')})



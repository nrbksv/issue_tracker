from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404, reverse

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


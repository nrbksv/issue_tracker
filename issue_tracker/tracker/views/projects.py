from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404, reverse

from tracker.models import Project
from tracker.forms import ProjectForm


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
        return reverse('project-detail', kwargs={'pk': self.object.pk })


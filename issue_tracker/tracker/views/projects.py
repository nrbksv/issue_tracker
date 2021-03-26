from django.views.generic import ListView, DetailView

from tracker.models import Project


class ProjectListView(ListView):
    template_name = 'projects/list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.all()


class ProjectDetailView(DetailView):
    template_name = 'projects/detail.html'
    model = Project

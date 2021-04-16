from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.models import User
from accounts.forms import RegisterForm
from accounts.models import Profile


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    model = User
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = 'tracker:projects-list'
        return next_url


class UserDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        projects = self.object.projects.all()
        paginator = Paginator(projects, self.paginate_by)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        kwargs['page_obj'] = page
        kwargs['projects'] = page.object_list
        kwargs['is_paginated'] = page.has_other_pages()
        return super().get_context_data(**kwargs)


class UserListView(PermissionRequiredMixin, ListView):
    template_name = 'users.html'
    context_object_name = 'user_obj'
    paginate_by = 10
    permission_required = 'accounts.view_profile'

    def get_queryset(self):
        return get_user_model().objects.all()
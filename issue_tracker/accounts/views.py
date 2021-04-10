from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib.auth.models import User
from accounts.forms import RegisterForm


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    model = User
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = 'tracker:projects-list'
        return next_url


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect


def login_view(request, *args, **kwargs):
    context = {}
    next_url = request.GET.get('next')
    if next_url is None:
        next_url = '/projects/'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(f'{next_url}')
        context['has_error'] = True
    return render(request, 'login.html', context=context)


def logout_view(request, *args, **kwargs):
    logout(request)
    return redirect('projects-list')

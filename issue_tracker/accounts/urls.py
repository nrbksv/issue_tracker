from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import RegisterView, UserDetailView, UserListView, UserChangeView, PasswordChangeView


app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', RegisterView.as_view(), name='register'),
    path('user/<int:pk>/profile', UserDetailView.as_view(), name='user-profile'),
    path('users/all', UserListView.as_view(), name='user-list'),
    path('user/update', UserChangeView.as_view(), name='user-update'),
    path('change-password/', PasswordChangeView.as_view(), name='change-password'),
]

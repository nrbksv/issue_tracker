"""issue_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tracker.views import (
        IssueListView,
        IssueDetail,
        NewIssue,
        IssueUpdate,
        IssueDelete,
        ProjectListView,
        ProjectDetailView,
        ProjectCreateView,
        ProjectIssueCreate,
        ProjectUpdateView,
        ProjectDeleteView
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ProjectListView.as_view(), name='projects-list'),
    path('project/<int:pk>', ProjectDetailView.as_view(), name='project-detail'),
    path('project/add', ProjectCreateView.as_view(), name='project-create'),
    path('project/<int:pk>/update', ProjectUpdateView.as_view(), name='project-update'),
    path('project/<int:pk>/delete', ProjectDeleteView.as_view(), name='project-delete'),
    path('project/<int:pk>/issue/add', ProjectIssueCreate.as_view(), name='project-issue'),
    path('issues/all', IssueListView.as_view(), name='issues-list'),
    path('issue/<int:pk>', IssueDetail.as_view(), name='issue-detail'),
    path('issue/add', NewIssue.as_view(), name='new-issue'),
    path('issue/<int:pk>/update', IssueUpdate.as_view(), name='issue-update'),
    path('issue/<int:pk>/delete', IssueDelete.as_view(), name='issue-delete'),
]

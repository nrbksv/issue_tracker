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
        ProjectDeleteView,
        ProjectUserAdd,
        ProjectUserRemove
    )

app_name = 'tracker'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ProjectListView.as_view(), name='projects-list'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('add/', ProjectCreateView.as_view(), name='project-create'),
    path('<int:pk>/update/', ProjectUpdateView.as_view(), name='project-update'),
    path('<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
    path('<int:pk>/issue/add/', ProjectIssueCreate.as_view(), name='project-issue'),
    path('<int:pk>/user/add/', ProjectUserAdd.as_view(), name='project-user-add'),
    path('<int:pk>/user/remove/', ProjectUserRemove.as_view(), name='project-user-remove'),
    path('issues/all', IssueListView.as_view(), name='issues-list'),
    path('issue/<int:pk>', IssueDetail.as_view(), name='issue-detail'),
    path('issue/add', NewIssue.as_view(), name='new-issue'),
    path('issue/<int:pk>/update', IssueUpdate.as_view(), name='issue-update'),
    path('issue/<int:pk>/delete', IssueDelete.as_view(), name='issue-delete'),
]

from django.contrib import admin

from tracker.models import Issue, Status, Type


class IssueAdmin(admin.ModelAdmin):
    list_display = ['status', 'summary', 'created_at', 'updated_at']
    list_filter = ['created_at', 'status', 'types']
    search_fields = ['summary']
    fields = ['id', 'status', 'types', 'summary', 'description', 'created_at', 'updated_at']
    readonly_fields = ['id', 'created_at', 'updated_at']


admin.site.register(Issue, IssueAdmin)


class StatusAdmin(admin.ModelAdmin):
    list_display = ['status']
    fields = ['status']


admin.site.register(Status, StatusAdmin)


class TypeAdmin(admin.ModelAdmin):
    list_display = ['type_issue']
    fields = ['type_issue']


admin.site.register(Type, TypeAdmin)
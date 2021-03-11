from django.db import models


class Issue(models.Model):
    summary = models.CharField(max_length=300, null=False, blank=False, verbose_name='Заголовок')
    description = models.TextField(max_length=3000, null=True, blank=True)
    status = models.ForeignKey('tracker.Status', on_delete=models.PROTECT, verbose_name='Статус')
    type_issue = models.ForeignKey('tracker.Type', on_delete=models.PROTECT, verbose_name='Тип')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'issues'
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return f'{self.status}{self.type_issue}{self.summary}{self.description}'


class Type(models.Model):
    type_issue = models.CharField(max_length=30, null=False, blank=False, verbose_name='Тип')

    class Meta:
        db_table = 'types'
        verbose_name = 'Тип задачи'
        verbose_name_plural = 'Типы задач'

    def __str__(self):
        return f'{self.type_issue}'


class Status(models.Model):
    status = models.CharField(max_length=30, blank=False, null=False, verbose_name='Статус')

    class Meta:
        db_table = 'statuses'
        verbose_name = 'Статус задачи'
        verbose_name_plural = 'Статусы задач'

    def __str__(self):
        return f'{self.status}'
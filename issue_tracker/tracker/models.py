from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator


class Issue(models.Model):
    summary = models.CharField(
        max_length=300,
        null=False,
        blank=False,
        validators=[MaxLengthValidator(300), MinLengthValidator(6)],
        verbose_name='Заголовок'
    )
    description = models.TextField(
        max_length=3000,
        validators=[MaxLengthValidator(3000), MinLengthValidator(6)],
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    status = models.ForeignKey(
        'tracker.Status',
        on_delete=models.PROTECT,
        related_name='issues',
        verbose_name='Статус'
    )
    types = models.ManyToManyField('tracker.Type', related_name='issues', verbose_name='Типы задач')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(
        'tracker.Project',
        on_delete=models.CASCADE,
        related_name='issues',
        verbose_name='Проект'
    )

    class Meta:
        db_table = 'issues'
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return f'{self.status}{self.types}{self.summary}{self.description}{self.project}'


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


class Project(models.Model):
    users = models.ManyToManyField(get_user_model(), related_name='projects', verbose_name='Пользователь')
    project = models.CharField(max_length=50, blank=False, null=False, verbose_name='Проект')
    project_description = models.TextField(max_length=1000, blank=False, null=False, verbose_name='Описание')
    date_start = models.DateField(verbose_name='Дата начала')
    date_finish = models.DateField(blank=True, null=True, verbose_name='Дата окончания')
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'projects'
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

        permissions = [
            ('project_user_update', 'Can update users in project'),
        ]

    def __str__(self):
        return f'{self.project}'
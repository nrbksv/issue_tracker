from django.contrib.auth import get_user_model
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь')
    avatar = models.ImageField(blank=True, null=True, upload_to='avatars', verbose_name='Аватар')
    git_hub = models.URLField(blank=True, null=True, verbose_name='Профиль в "GitHub"')
    about = models.TextField(max_length=1000, blank=True, null=True, verbose_name='О себе')

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'profiles'
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

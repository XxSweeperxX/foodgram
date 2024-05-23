from django.db import models
from .settings import *

class ShortLink(models.Model):
    short_url = models.CharField(
        'Короткая ссылка',
        db_index=True,
        max_length=100,
        null=True,
        blank=True
    )
    full_url = models.CharField(
        'Полная ссылка',
        max_length=500,
    )

    def __str__(self):
        return f'{self.pk} - {self.short_url}'

    class Meta:
        db_table = 'shortlink'
        verbose_name = 'короткая ссылка'
        verbose_name_plural = 'Короткие ссылки'

    @property
    def short_path(self):
        return f'{HOST_ADDRESS}/{SHORTLINK_URL_BASE}{self.short_url}'

    def

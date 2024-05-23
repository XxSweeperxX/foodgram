from django.db import models
from django.conf import settings

from shortener.utils import generate_rnd_string


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
        return (f'{settings.HOST_ADDRESS}/'
                f'{settings.SHORTLINK_URL_BASE}{self.short_url}')

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
    ):
        if not self.short_url:
            self.generate_new_short_url(commit=False)

    def generate_new_short_url(self, commit):
        while True:
            url = generate_rnd_string()
            if not ShortLink.objects.filter(short_url=url).exists():
                break
        self.short_url = url
        if commit:
            self.save()



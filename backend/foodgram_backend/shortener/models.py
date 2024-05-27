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
        return f'{self.full_url} - {self.short_url}'

    class Meta:
        verbose_name = 'короткая ссылка'
        verbose_name_plural = 'Короткие ссылки'

    @property
    def short_path(self):
        return (
            f'{settings.SHORTENER_DOMAIN_ADDRESS}/'
            f'{settings.SHORTENER_URL_BASE}{self.short_url}'
        )

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
    ):
        if not self.short_url:
            self.generate_new_short_url()
            super().save()

    def generate_new_short_url(self):
        while True:
            new_short_url = generate_rnd_string()
            if not ShortLink.objects.filter(short_url=new_short_url).exists():
                break
        self.short_url = new_short_url

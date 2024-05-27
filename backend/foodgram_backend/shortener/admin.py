from django.contrib import admin

from shortener.models import ShortLink


@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_url',
        'short_url',
    )

from django.contrib import admin
from users.models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'username',
        'email',
        'is_superuser',
    )
    search_fields = ('username', 'email',)
    list_filter = ('first_name', 'email',)


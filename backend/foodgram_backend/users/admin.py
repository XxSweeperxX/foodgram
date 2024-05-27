from django.contrib import admin
from django.contrib.auth.models import Group

from users.models import (
    User
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'email',
        'username'

    )
    search_fields = (
        'first_name',
        'email',
        'username'
    )


admin.site.unregister(Group)

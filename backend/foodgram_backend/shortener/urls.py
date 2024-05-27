from django.urls import re_path
from django.conf import settings

from .views import map_link


urlpatterns = [
    re_path(
        '^{}(?P<path>[a-zA-Z0-9 _-]+)$'.format(settings.SHORTENER_URL_BASE),
        map_link, name='map_link'),
]

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from .models import ShortLink


def map_link(request, **kwargs):
    path = kwargs.get('path')
    short_link = get_object_or_404(
        ShortLink,
        short_url=path
    )
    return HttpResponseRedirect(short_link.full_url)

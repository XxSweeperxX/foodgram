from django.http import HttpResponseRedirect, Http404

from .models import ShortLink


def map_link(request, **kwargs):
    path = kwargs['path']
    s = ShortLink.objects.filter(url=path).first()
    if s:
        return HttpResponseRedirect(s.full_url)
    raise Http404

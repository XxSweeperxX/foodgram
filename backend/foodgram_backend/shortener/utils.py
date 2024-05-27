import string
import random

from django.conf import settings


def generate_rnd_string(num=settings.SHORTENER_PATH_LENGTH):
    return ''.join(random.SystemRandom().choice(
        string.ascii_uppercase + string.ascii_lowercase + string.digits
    ) for _ in range(num))

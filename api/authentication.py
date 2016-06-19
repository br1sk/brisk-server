import uuid

from django.http import HttpResponse
from functools import wraps
from models import Authorization


def token_auth(func):
    @wraps(func)
    def _decorator(request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' in request.META:
            token = request.META['HTTP_AUTHORIZATION'].strip()
            try:
                request.authorization = Authorization.objects.get(token=token)
            except Authorization.DoesNotExist:
                return HttpResponse("Unauthorized", status=401)

        return func(request, *args, **kwargs)

    return _decorator


def authenticate(cookie):
    token = uuid.uuid4().hex
    return Authorization.objects.create(token=token, cookie=cookie)

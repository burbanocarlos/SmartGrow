from django.http import HttpResponseRedirect
from django.conf import settings
from functools import wraps
from django.contrib.auth.decorators import user_passes_test
from channels.db import database_sync_to_async
from django.urls import reverse


def async_user_passes_test(test_func):
    def decorator(view_func):
        @wraps(view_func)
        async def _wrapped_view(request, *args, **kwargs):
            test_result = await database_sync_to_async(test_func)(request.user)
            if not test_result:
                return HttpResponseRedirect(reverse('smart_grow:login'))  # Use 'login' instead of settings.LOGIN_URL
            return await view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def async_login_required():
    return async_user_passes_test(lambda u: u.is_authenticated)

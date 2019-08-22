"""
This is just a pure wrapper / alias module around django_api_decorators to
still be able to import it with the original, unintended name of decorators.
See https://github.com/agilgur5/django-serializable-model/issues/2, which had
the same issue and its changes were cherry-picked here.
In the first major/breaking release, v1.0.0, this file should be deleted and
the module removed from `setup.py`.
"""

from django_api_decorators import *  # noqa F403, F401

import json
from functools import wraps

import django
from django.http import HttpResponse, HttpResponseNotAllowed


def method_exclusive(method):
    """
    Checks if request.method is equal to method, if not, returns a
    405 not allowed response
    """
    def decorator(func):
        @wraps(func)
        def func_wrapper(request, *args, **kwargs):
            if request.method != method:
                return HttpResponseNotAllowed([method])
            return func(request, *args, **kwargs)
        return func_wrapper
    return decorator


def require_auth(func):
    """
    Checks if the request was made by an authenticated user, and if not,
    returns a 401 unauthorized response
    """
    @wraps(func)
    def func_wrapper(request, *args, **kwargs):
        # backward compatibility for Django < 1.10
        if django.VERSION < (1, 10):
            is_authenticated = request.user.is_authenticated()
        else:
            is_authenticated = request.user.is_authenticated

        if not is_authenticated:
            return HttpResponse(status=401)
        return func(request, *args, **kwargs)
    return func_wrapper


def clean_form(form_class):
    """
    Cleans the data in the POST or GET params using the form_class specified.
    Responds with a 400 bad request if the form is invalid with the errors
    specified in the form as JSON.
    Adds the cleaned data as a kwarg (cd) to the decorated function.
    """
    def decorator(func):
        @wraps(func)
        def func_wrapper(request, *args, **kwargs):
            form = form_class(
                (request.POST if request.method == 'POST' else request.GET),
                request.FILES
            )
            if not form.is_valid():
                return HttpResponse(json.dumps(form.errors), status=400)
            kwargs['cd'] = form.cleaned_data
            return func(request, *args, **kwargs)
        return func_wrapper
    return decorator


def clean_forms(form_class, attribute, required=True):
    """
    Cleans the data in the POST or GET params using the form_class specified.
    Responds with a 400 bad request if any of the forms are invalid with the
    errors specified in the form as JSON.
    Adds the cleaned data as a kwarg (cd_list) to the decorated function.
    """
    def decorator(func):
        @wraps(func)
        def func_wrapper(request, *args, **kwargs):
            request_dict = (request.POST
                            if request.method == 'POST' else request.GET)
            data_list = request_dict.getlist(attribute + '[]')
            kwargs['cd_list'] = []

            if not data_list:
                # error out if not existent
                if required:
                    obj = {}
                    obj[attribute] = 'This field is required'
                    return HttpResponse(json.dumps(obj), status=400)
                # early return if not required
                return func(request, *args, **kwargs)

            # iterate through and validate each form submitted
            for data in data_list:
                # must JSON.loads as Django QueryDicts can't handle nesting
                form = form_class(json.loads(data))
                if not form.is_valid():
                    return HttpResponse(json.dumps(form.errors), status=400)
                kwargs['cd_list'].append(form.cleaned_data)

            return func(request, *args, **kwargs)
        return func_wrapper
    return decorator

# django-api-decorators

<!-- releases / versioning -->
[![PyPI version](https://img.shields.io/pypi/v/django-api-decorators.svg)](https://pypi.org/project/django-api-decorators/)
[![releases](https://img.shields.io/github/tag-pre/agilgur5/django-api-decorators.svg)](https://github.com/agilgur5/django-api-decorators/releases)
[![commits](https://img.shields.io/github/commits-since/agilgur5/django-api-decorators/latest.svg)](https://github.com/agilgur5/django-api-decorators/commits/master)
<br><!-- downloads -->
[![dm](https://img.shields.io/pypi/dm/django-api-decorators.svg)](https://pypi.org/project/django-api-decorators/)
[![dw](https://img.shields.io/pypi/dw/django-api-decorators.svg)](https://pypi.org/project/django-api-decorators/)

Tiny decorator functions to make it easier to build an API using Django in ~100 LoC (shorter than this README!)

## Table of Contents

I. [Installation](#installation) <br />
II. [Usage](#usage) <br />
III. [How it Works](#how-it-works) <br />
IV. [Related Libraries](#related-libraries) <br />
V. [Backstory](#backstory)

## Installation

```shell
pip install django-api-decorators
```

It is expected that you already have Django installed

### Compatibility

_This was originally used in an older Django 1.5 codebase with Python 2.7._

Should work with Django 1.x-2.x and with Python 2.7-3.x

- Likely works with Django 0.95-0.99 as well, didn't check any earlier versions' release notes
- `2to3` shows that there is nothing to change, so should be compatible with Python 3.x
- Have not confirmed if this works with earlier versions of Python.

Please submit a PR or file an issue if you have a compatibility problem or have confirmed compatibility on versions.

<br>

## Usage

`@method_exclusive`, per docstring: `Checks if request.method is equal to method, if not, returns a 405 not allowed response`. Example:

```python
from django_api_decorators import method_exlusive

@method_exclusive('GET')
def get_latest_public_posts(request):
    ...

```

<br>

`@require_auth`, per docstring: `Checks if the request was made by an authenticated user, and if not, returns a 401 unauthorized response`. Example:

```python
from django_api_decorators import method_exclusive, require_auth

@method_exclusive('GET')
@require_auth
def get_favorites(request):
    favs = request.user.favorites.all()
    ...

```

One can add more authorization checks on the User, such as for specific user types,
by building on top of the `@require_auth` decorator. For instance:

```python
from functools import wraps

from django.http import HttpResponse
from django_api_decorators import require_auth

def tenant_exclusive(func):
    """
    Checks if the authenticated user is a tenant, and if not, returns a
    401 unauthorized response
    """
    @wraps(func)
    @require_auth
    def func_wrapper(request, *args, **kwargs):
        if not request.user.is_tenant():
            return HttpResponse(status=401)
        return func(request, *args, **kwargs)
    return func_wrapper
```

<br>

`@clean_form`, per docstring: `Cleans the data in the POST or GET params using the form_class specified. Responds with a 400 bad request if the form is invalid with the errors specified in the form as JSON. Adds the cleaned data as a kwarg (cd) to the decorated function`. Example:

```python
from django.shortcuts import get_object_or_404
from django_api_decorators import method_exclusive, clean_form, require_auth

from posts.models import Post
from posts.forms import AddFavForm

@method_exclusive('POST')
@clean_form(AddFavForm)
@require_auth
def add_fav(request, cd):
    post = get_object_or_404(Post, pk=cd['post_id'])
    request.user.favorites.add(post)
    ...

```

<br>

`@clean_forms`, per docstring: `Cleans the data in the POST or GET params using the form_class specified. Responds with a 400 bad request if any of the forms are invalid with the errors specified in the form as JSON. Adds the cleaned data as a kwarg (cd_list) to the decorated function`. Example:

```python
from django_api_decorators import method_exclusive, clean_forms, require_auth

from posts.models import Post
from posts.forms import CreatePostForm

@method_exclusive('POST')
@clean_forms(CreatePostForm, 'posts')
@require_auth
def bulk_create_posts(request, cd_list):
    post_list = []
    for data in cd_list:
        post_list.append(Post(
            user=request.user,
            cotent=data['content']
        ))
    Post.objects.bulk_create(post_list)

    ...

```

<br>

## How it works

All of the decorators currently just perform a check against the `request` object, have an early return if the request is invalid, and otherwise let the next function execute. Some of them add a keyword argument when calling the next function so that the interpreted data can be used within it (like with the cleaned dictionaries of forms, which are added as a `kwarg` of the keyword `cd`).

I'd encourage you to read the source code, since it's shorter than this README :)

## Related Libraries

- [django-serializable-model](https://github.com/agilgur5/django-serializable-model)
  - `Django classes to make your models, managers, and querysets serializable, with built-in support for related objects in ~100 LoC`

<br>

## Backstory

This library was built while I was working on [Yorango](https://github.com/Yorango)'s ad-hoc API and transitioning from an MPA to an SPA. Instead of repeating lots of authentication, authorization, and validation code for every request, I wanted to DRY it up more using decorators or middleware. Decorators would allow us to have early returns with proper HTTP Status Codes for invalid requests. Request code became easier to reason about as a result, guaranteeing it would only execute after authz/authn/etc, and much less prone to accidental bugs, e.g. security issues due to forgetting an authorization check. `@method_exclusive`, `@require_auth`, and a few more project-specific decorators were born out of some of those needs.

Validation was a bit more difficult, as we had many existing [Django `Form`s](https://docs.djangoproject.com/en/2.0/ref/forms/api/#django.forms.Form) in the MPA, wanted to re-use the classes and validation code we already had in our API instead of re-writing, and wanted to keep things in the same idiomatic style. [Django REST Framework has the concept of "Validators"](http://www.django-rest-framework.org/api-guide/validators/), but it is explicitly different from Django's standard `Form` interface and requires you to buy-in to other parts of DRF to use, like Serializers. `@clean_form` was born to address those needs. Later `@clean_forms` was made to address the case of multiple of the same form in one API request (e.g. for bulk creation), somewhat similar to how a [Django `FormSet`](https://docs.djangoproject.com/en/2.0/topics/forms/formsets/) might work, but much simpler and requiring a lot less coupling of front and back end code.

These were all used in production with great results, some API methods having just 1 decorator and others having 3 or more decorators, such as:

```python
@method_exclusive('POST')
@clean_form(CreateBillsForm)
@clean_forms(BillForm, 'bills')
@landlord_saas_exclusive
@authorize_action(Listing, 'listing_id')
def create_bills(request, cd, cd_list, listing):
    ...

    # bulk_create the new list of Bills
    bill_list = []
    for data in cd_list:
        bill_list.append(Bill(
            listing=listing,
            price=data['price'],
            due_date=data['due_date'],
        ))
    Bill.objects.bulk_create(bill_list)

    ...
```

Had been meaning to extract and open source this as well as other various useful utility libraries I had made at Yorango and finally got the chance!

# django-api-decorators

[![PyPI version](https://badge.fury.io/py/django-api-decorators.svg)](https://badge.fury.io/py/django-api-decorators)

Tiny decorator functions to make it easier to build an API using Django in ~100 LoC.


## Table of Contents

I. [Installation](#installation) <br />
II. [How it Works](#how-it-works) <br />


## Installation

```shell
pip install django-api-decorators
```

It is expected that you already have Django installed

### Compatibility

_This was originally used in an older Django 1.5 codebase with Python 2.7._

- `2to3` shows that there is nothing to change, so should be compatible with Python 3.x
- Have not confirmed if this works with earlier versions of Python.


Please submit a PR or file an issue if you have a compatibility problem or have confirmed compatibility on versions.

<br>


## How it works

All of the decorators currently just perform a check against the `request` object, have an early return if the request is invalid, and otherwise let the next function execute. Some of them add a keyword argument when calling the next function so that the interpreted data can be used within it (like with the cleaned dictionaries of forms, which are added as a `kwarg` of the keyword `cd`).

I'd encourage you to read the source code, since it's pretty short :)

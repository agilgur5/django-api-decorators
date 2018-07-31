# Always prefer setuptools over distutils
from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-api-decorators',
    version='0.0.1',
    description=('Tiny decorator functions to make it easier to build an ' +
                 'API using Django in ~100 LoC'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/agilgur5/django-api-decorators',
    author='Anton Gilgur',
    license='Apache-2.0',
    classifiers=[
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: Apache Software License',

        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'Framework :: Django :: 1.5',
    ],
    keywords=('django api rest ad-hoc decorators json dict'),
    py_modules=['decorators'],
    python_requires='>=2.7, <4',
    project_urls={  # Optional
        'Source': 'https://github.com/agilgur5/django-api-decorators/',
        'Tracker': 'https://github.com/agilgur5/django-api-decorators/issues', # noqa
    },
)

Nose Django Querycount Plugin
========================

Counts queries for each test and shows result in the end in table. XML otput
and other fancy stuff will be added later.

Installation
------------
From the source repository:

    $ pip install git+git://github.com/dgladkov/nose-django-querycount.git

From PyPI:

    $ pip install nose-django-querycount

Usage
------------

Currently only nose is supported, but native Django runner support is planned.
Run like following:

    $ nosetests --with-querycount

Alternatively, if you use [django-nose][], add it to your Django settings
like so:

    NOSE_ARGS = ['--with-querycount']
    NOSE_PLUGINS = [
        'nosequerycount.plugin.DjangoQueryCountPlugin',
    ]

Options
------------

    $ nosetests --with-querycount --querycount-threshold=15

Provides query count threshold for each test. If test run exceeds 15 queries,
query count number will be red. Works only for terminal output and only if
your terminal application supports coloring.

Warning
------------

**This plugin sets DEBUG=True for tests, it can break your existing tests!**

Django test runner sets DEBUG to False when when running test, but Django
saves query log only when DEBUG mode is enabled.


[django-nose]: https://github.com/jbalogh/django-nose

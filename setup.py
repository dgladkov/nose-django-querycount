from setuptools import setup

setup(
    name='nose-django-querycount',
    version='0.1',
    packages=['nosequerycount'],
    author="Dmitry Gladkov",
    author_email='dmitry.gladkov@gmail.com',
    entry_points={
        'nose.plugins.0.10': [
            'querycount = nosequerycount.plugin:DjangoQueryCountPlugin',
        ],
    },
)

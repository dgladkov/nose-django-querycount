try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup
import nose


setup(
    name='nose-django-querycount',
    version='0.2',
    author="Dmitry Gladkov",
    author_email='dmitry.gladkov@gmail.com',
    url='https://github.com/dgladkov/nose-django-querycount',
    description = 'Nose plugin for counting queries in Django tests',
    packages=['nosequerycount'],
    zip_safe=False,
    install_requires=[
        'django',
        'nose',
    ],
    test_suite = "nose.collector",
    include_package_data=True,
    entry_points={
        'nose.plugins.0.10': [
            'querycount = nosequerycount.plugin:DjangoQueryCountPlugin',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development'
    ],
    keywords='test unittest nosetests nose plugin django queries querycount',
)

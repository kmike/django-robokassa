#!/usr/bin/env python
#coding: utf-8
from distutils.core import setup

import sys
reload(sys).setdefaultencoding("UTF-8")

setup(
    name='django-robokassa',
    version='0.9.1',
    author='Mikhail Korobov',
    author_email='kmike84@gmail.com',

    packages=['robokassa', 'robokassa.migrations'],

    url='http://bitbucket.org/kmike/django-robokassa/',
    download_url = 'http://bitbucket.org/kmike/django-robokassa/get/tip.zip',
    license = 'MIT license',
    description = u'Приложение для интеграции платежной системы ROBOKASSA в проекты на Django.'.encode('utf8'),
    long_description = open('README.rst').read().decode('utf8'),

    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Natural Language :: Russian',
    ),
)
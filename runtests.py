#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.management import call_command

settings.configure(
    INSTALLED_APPS=('robokassa', 'south'),
    DATABASE_ENGINE = 'sqlite3',
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3'
        }
    },

    ROBOKASSA_LOGIN = 'test_login',
    ROBOKASSA_PASSWORD1 = 'test_password',
    ROBOKASSA_PASSWORD2 = 'test_password2',
    ROBOKASSA_EXTRA_PARAMS = ['param1', 'param2'],
)

if __name__ == "__main__":
    call_command('test', 'robokassa')

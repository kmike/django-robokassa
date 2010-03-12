#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.management import call_command

settings.configure(
    INSTALLED_APPS=('robokassa',),
    DATABASE_ENGINE = 'sqlite3',

    ROBOKASSA_LOGIN = 'test_login',
    ROBOKASSA_PASSWORD1 = 'test_password',
)

if __name__ == "__main__":
    call_command('test', 'robokassa')

#coding: utf-8

from django.conf import settings

# обязательные параметры - реквизиты магазина
LOGIN = settings.ROBOKASSA_LOGIN
PASSWORD1 = settings.ROBOKASSA_PASSWORD1
PASSWORD2 = getattr(settings, 'ROBOKASSA_PASSWORD2', None)



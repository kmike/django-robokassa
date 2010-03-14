#coding: utf-8

from django.conf import settings

# обязательные параметры - реквизиты магазина
LOGIN = settings.ROBOKASSA_LOGIN
PASSWORD1 = settings.ROBOKASSA_PASSWORD1
PASSWORD2 = getattr(settings, 'ROBOKASSA_PASSWORD2', None)

# использовать ли метод POST при приеме результатов
USE_POST = getattr(settings, 'ROBOKASSA_USE_POST', True)

# требовать предварительного уведомления на ResultURL
STRICT_CHECK = getattr(settings, 'ROBOKASSA_STRICT_CHECK', True)


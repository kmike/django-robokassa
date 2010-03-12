================
django-robokassa
================

django-robokassa - это приложение для интеграции платежной системы ROBOKASSA в
проекты на Django.

До использования следует ознакомиться с официальной документацией
ROBOKASSA (http://robokassa.ru/Doc/Ru/Interface.aspx). Приложение реализует
протокол взаимодействия, описанный в этом документе.

Установка
=========

Как обычно::

    $ pip install django-robokassa

или ::

    $ easy_install django-robokassa

или ::

    $ hg clone http://bitbucket.org/kmike/django-robokassa/
    $ cd django-robokassa
    $ python setup.py install


Потом следует добавить 'robokassa' в INSTALLED_APPS и выполнить ::

    $ python manage.py syncdb

Если используется South, то вместо syncdb нужно сделать ::

    $ python manage.py migrate


Настройка
=========

В settings.py нужно указать следующие настройки:

* ROBOKASSA_LOGIN - логин
* ROBOKASSA_PASSWORD - пароль

Необязательный параметар: ASSIST_TEST_MODE - включен ли тестовый режим.
По умолчанию False (т.е. включен боевой режим).

Использование
=============

TODO: написать

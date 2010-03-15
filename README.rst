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
* ROBOKASSA_PASSWORD - пароль №1

Необязательные параметры:

* ROBOKASSA_PASSWORD2 - пароль №2 (используется, если нужна автоматическая
  обработка результатов)

* ROBOKASSA_USE_POST - используется ли метод POST при приеме результатов от
  ROBOKASSA. По умолчанию - True. Считается, что для Result URL, Success URL и
  Fail URL выбран один и тот же метод.

* ROBOKASSA_STRICT_CHECK - использовать ли строгую проверку (требовать
  предварительного уведомления на ResultURL). По умолчанию - True.


Использование
=============

TODO: написать

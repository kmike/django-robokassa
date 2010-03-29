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

или, если используется South, ::

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

* ROBOKASSA_TEST_MODE - включен ли тестовый режим. По умолчанию False
  (т.е. включен боевой режим).


Использование
=============

urls.py
-------

Для настройки Result URL, Success URL и Fail URL можно подключить
модуль robokassa.urls::

    urlpatterns = patterns('',
        #...
        url(r'^robokassa/', include('robokassa.urls')),
        #...
    )

Адреса, которые нужно указывать в панели robokassa, в этом случае будут иметь вид

* Result URL: http://yoursite.ru/robokassa/result/
* Success URL: http://yoursite.ru/robokassa/success/
* Fail URL: http://yoursite.ru/robokassa/fail/


Шаблоны
-------

* ``robokassa/success.html`` - показывается в случае успешной оплаты. В
  контексте есть переменная form типа `SuccessRedirectForm`, а также InvId
  и OrderSum с параметрами заказа.

* ``robokassa/fail.html`` - показывается в случае неуспешной оплаты. В
  контексте есть переменная form типа `SuccessRedirectForm`, а также InvId
  и OrderSum с параметрами заказа.

* ``robokassa/error.html`` - показывается при ошибочном запросе к странице
  "успех" или "неудача" (например, ошибка в контрольной сумме). В контексте
  есть переменная form класса `FailRedirectForm` или `SuccessRedirectForm`.



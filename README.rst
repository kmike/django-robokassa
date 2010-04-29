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
* ROBOKASSA_PASSWORD1 - пароль №1

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

* ROBOKASSA_EXTRA_PARAMS - список (list) названий дополнительных параметров,
  которые будут передаваться вместе с запросами. "Shp" к ним приписывать не
  нужно.


Использование
=============

Форма для приема платежей
-------------------------
Для того, чтобы упростить конструирование html-форм для отправки пользователей в
Robokassa, в django-robokassa есть форма RobokassaForm. Она нужна
для упрощения вывода информации в шаблонах, вычисления контрольной суммы и
формирования параметров GET-запросов.

Пример::

    # views.py

    from django.shortcuts import get_object_or_404
    from django.views.generic.simple import direct_to_template
    from django.contrib.auth.decorators import login_required

    from robokassa.forms import RobokassaForm

    @login_required
    def pay_with_robokassa(request, order_id)
        order = get_object_or_404(Order, pk = order_id)

        form = RobokassaForm(initial={
                   'OutSum': order.total,
                   'InvId': order.id,
                   'Desc': order.name,
                   'Email': request.user.email,
                   # 'IncCurrLabel': '',
                   # 'Culture': 'ru'
               })

        return direct_to_template(request, 'pay_with_robokassa.html', {'form': form})

В initial все параметры необязательны. Детальную справку по параметрам
лучше посмотреть в документации к Robokassa. Можно передавать в initial
значения дополнительных параметров, описанных в ROBOKASSA_EXTRA_PARAMS.

Соответствующий шаблон::

    {% extends 'base.html' %}

    {% block content %}
        <form action="{{ form.target }}" method="POST">
            <p>{{ form.as_p }}</p>
            <p><input type="submit" value="Купить"></p>
        </form>
    {% endblock %}

Форма выведется в виде набора скрытых input-тегов.

У формы есть атрибут target, содержащий URL, по которому форму следует
отправлять. В тестовом режиме это будет тестовый URL, в боевом - боевой.

Вместо отправки формы можно сформировать GET-запрос. У формы есть
метод get_redirect_url, который возвращает нужный адрес со всеми параметрами.
Редирект на этот адрес равносилен отправке формы методом GET.

django-robokassa не включает в себя модели "Покупка", т.к. эта модель будет
отличаться от сайта к сайту. Обработку смены статусов покупок следует
осуществлять в обработчиках сигналов.


Получение результатов платежей
------------------------------
В Robokassa есть несколько методов определения результата платежа:

1. При переходе на страницы Success и Fail гарантируется, что платеж
   соответственно прошел и не прошел

2. При успешном или неудачном платеже Robokassa отправляет POST или GET запрос
   на Result URL.

3. Можно запрашивать статус платежа через XML-сервис.

В django-robokassa на данный момент поддерживаются методы 1 и 2 и их совмещение
(дополнительная проверка, что при переходе на Success URL уже было уведомление
на Result URL при использовании опции ROBOKASSA_STRICT_CHECK = True).
Обработчики подключаются через urls.py, рендерят соответствующие
шаблоны и шлют сигналы в зависимости от успешности платежа.


Сигналы
-------
Обработку смены статусов покупок следует осуществлять в обработчиках сигналов.

* robokassa.signals.result_received - шлется при получении уведомления от
  Robokassa. Получение этого сигнала означает, что оплата была успешной.
  В качестве sender передается экземпляр модели SuccessNotification, у
  которой есть атрибуты InvId и OutSum.

* robokassa.signals.success_page_visited - шлется при переходе пользователя
  на страницу успешной оплаты. Этот сигнал следует использовать вместо
  result_received, если не используется строгая проверка
  (ROBOKASSA_STRICT_CHECK=False)

* robokassa.signals.fail_page_visited - шлется при переходе пользователя
  на страницу ошибки оплаты. Получение этого сигнала означает, что оплата
  не была произведена. В обработчике следует осуществлять разблокирвку товара
  на складе и т.д.

Все сигналы получают параметры InvId (номер заказа), OutSum (сумма оплаты) и
extra (словарь с дополнительными параметрами, описанными в
ROBOKASSA_EXTRA_PARAMS).

Пример::

    from robokassa.signals import result_received
    from my_app.models import Order

    def payment_received(sender, **kwargs):
        order = Order.objects.get(id=kwargs['InvId'])
        order.status = 'paid'
        order.paid_sum = kwargs['OutSum']
        order.extra_param = kwargs['extra']['my_param']
        order.save()

    result_received.connect(payment_received)



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

* Result URL: ``http://yoursite.ru/robokassa/result/``
* Success URL: ``http://yoursite.ru/robokassa/success/``
* Fail URL: ``http://yoursite.ru/robokassa/fail/``


Шаблоны
-------

* ``robokassa/success.html`` - показывается в случае успешной оплаты. В
  контексте есть переменная form типа ``SuccessRedirectForm``, InvId
  и OutSum с параметрами заказа, а также все дополнительные параметры, описанные
  в ROBOKASSA_EXTRA_PARAMS.

* ``robokassa/fail.html`` - показывается в случае неуспешной оплаты. В
  контексте есть переменная form типа ``FailRedirectForm``, InvId
  и OutSum с параметрами заказа, а также все дополнительные параметры, описанные
  в ROBOKASSA_EXTRA_PARAMS.

* ``robokassa/error.html`` - показывается при ошибочном запросе к странице
  "успех" или "неудача" (например, при ошибке в контрольной сумме). В контексте
  есть переменная form класса ``FailRedirectForm`` или ``SuccessRedirectForm``.

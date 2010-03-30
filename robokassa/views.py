#coding: utf-8

from django.http import HttpResponse
from django.views.generic.simple import direct_to_template

from robokassa.conf import USE_POST
from robokassa.forms import ResultURLForm, SuccessRedirectForm, FailRedirectForm
from robokassa.models import SuccessNotification
from robokassa.signals import result_received, success_page_visited, fail_page_visited

def receive_result(request):
    """ обработчик для ResultURL. """
    data = request.POST if USE_POST else request.GET
    form = ResultURLForm(data)
    if form.is_valid():
        id, sum = form.cleaned_data['InvId'], form.cleaned_data['OrderSum']

        # сохраняем данные об успешном уведомлении в базе, чтобы
        # можно было выполнить дополнительную проверку на странице успешного
        # заказа
        notification = SuccessNotification.objects.create(InvId = id, OrdSum = sum)

        # дополнительные действия с заказом (например, смену его статуса) можно
        # осуществить в обработчике сигнала robokassa.signals.result_received
        result_received.send(sender = notification, InvId = id, OrdSum = sum)


        return HttpResponse('OK'+id)
    return HttpResponse('error: bad signature')


def success(request, template_name='robokassa/success.html', extra_context=None,
            error_template_name = 'robokassa/error.html'):
    """ обработчик для SuccessURL """

    data = request.POST if USE_POST else request.GET
    form = SuccessRedirectForm(data)
    if form.is_valid():
        id, sum = form.cleaned_data['InvId'], form.cleaned_data['OrderSum']

        # в случае, когда не используется строгая проверка, действия с заказом
        # можно осуществлять в обработчике сигнала robokassa.signals.success_page_visited
        success_page_visited.send(sender = form, InvId = id, OrdSum = sum)

        context = {'InvId': id, 'OrderSum': sum, 'form': form}
        context.update(extra_context or {})
        return direct_to_template(request, template_name, extra_context=context)

    return direct_to_template(request, error_template_name, extra_context={'form': form})


def fail(request, template_name='robokassa/fail.html', extra_context=None,
         error_template_name = 'robokassa/error.html'):
    """ обработчик для FailURL """

    data = request.POST if USE_POST else request.GET
    form = FailRedirectForm(data)
    if form.is_valid():
        id, sum = form.cleaned_data['InvId'], form.cleaned_data['OrderSum']

        # дополнительные действия с заказом (например, смену его статуса для
        # разблокировки товара на складе) можно осуществить в обработчике
        # сигнала robokassa.signals.fail_page_visited
        fail_page_visited.send(sender = form, InvId = id, OrdSum = sum)

        context = {'InvId': id, 'OrderSum': sum, 'form': form}
        context.update(extra_context or {})
        return direct_to_template(request, template_name, extra_context=context)

    return direct_to_template(request, error_template_name, extra_context={'form': form})


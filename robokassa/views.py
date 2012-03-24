#coding: utf-8

from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt

from robokassa.conf import USE_POST
from robokassa.forms import ResultURLForm, SuccessRedirectForm, FailRedirectForm
from robokassa.models import SuccessNotification
from robokassa.signals import result_received, success_page_visited, fail_page_visited

@csrf_exempt
def receive_result(request):
    """ обработчик для ResultURL. """
    data = request.POST if USE_POST else request.GET
    form = ResultURLForm(data)
    if form.is_valid():
        id, sum = form.cleaned_data['InvId'], form.cleaned_data['OutSum']

        # сохраняем данные об успешном уведомлении в базе, чтобы
        # можно было выполнить дополнительную проверку на странице успешного
        # заказа
        notification = SuccessNotification.objects.create(InvId = id, OutSum = sum)

        # дополнительные действия с заказом (например, смену его статуса) можно
        # осуществить в обработчике сигнала robokassa.signals.result_received
        result_received.send(sender = notification, InvId = id, OutSum = sum,
                             extra = form.extra_params())

        return HttpResponse('OK%s' % id)
    return HttpResponse('error: bad signature')


@csrf_exempt
def success(request, template_name='robokassa/success.html', extra_context=None,
            error_template_name = 'robokassa/error.html'):
    """ обработчик для SuccessURL """

    data = request.POST if USE_POST else request.GET
    form = SuccessRedirectForm(data)
    if form.is_valid():
        id, sum = form.cleaned_data['InvId'], form.cleaned_data['OutSum']

        # в случае, когда не используется строгая проверка, действия с заказом
        # можно осуществлять в обработчике сигнала robokassa.signals.success_page_visited
        success_page_visited.send(sender = form, InvId = id, OutSum = sum,
                                  extra = form.extra_params())

        context = {'InvId': id, 'OutSum': sum, 'form': form}
        context.update(form.extra_params())
        context.update(extra_context or {})
        return TemplateResponse(request, template_name, context)

    return TemplateResponse(request, error_template_name, {'form': form})


@csrf_exempt
def fail(request, template_name='robokassa/fail.html', extra_context=None,
         error_template_name = 'robokassa/error.html'):
    """ обработчик для FailURL """

    data = request.POST if USE_POST else request.GET
    form = FailRedirectForm(data)
    if form.is_valid():
        id, sum = form.cleaned_data['InvId'], form.cleaned_data['OutSum']

        # дополнительные действия с заказом (например, смену его статуса для
        # разблокировки товара на складе) можно осуществить в обработчике
        # сигнала robokassa.signals.fail_page_visited
        fail_page_visited.send(sender = form, InvId = id, OutSum = sum,
                               extra = form.extra_params())

        context = {'InvId': id, 'OutSum': sum, 'form': form}
        context.update(form.extra_params())
        context.update(extra_context or {})
        return TemplateResponse(request, template_name, context)

    return TemplateResponse(request, error_template_name, {'form': form})


#coding: utf-8

from hashlib import md5
from urllib import urlencode
from django import forms

from robokassa.conf import LOGIN, PASSWORD1, PASSWORD2
from robokassa.conf import STRICT_CHECK, FORM_TARGET
from robokassa.models import SuccessNotification

class RobokassaForm(forms.Form):

    # login магазина в обменном пункте
    MrchLogin = forms.CharField(max_length=20, initial = LOGIN)

    # требуемая к получению сумма
    OutSum = forms.DecimalField(min_value=0, max_digits=20, decimal_places=2, required=False)

    # номер счета в магазине (должен быть уникальным для магазина)
    InvId = forms.IntegerField(min_value=0, required=False)

    # описание покупки
    Desc = forms.CharField(max_length=100, required=False)

    # контрольная сумма MD5
    SignatureValue = forms.CharField(max_length=32)

    # предлагаемая валюта платежа
    IncCurrLabel = forms.CharField(max_length = 10, required=False)

    # e-mail пользователя
    Email = forms.CharField(max_length=100, required=False)

    # язык общения с клиентом (en или ru)
    Culture = forms.CharField(max_length=2, required=False)

    # Параметр с URL'ом, на который форма должны быть отправлена.
    # Может пригодиться для использования в шаблоне.
    target = FORM_TARGET

    def get_redirect_url(self):
        """ Получить URL с GET-параметрами, соответствующими значениям полей в
        форме. Редирект на адрес, возвращаемый этим методом, эквивалентен
        ручной отправке формы методом GET.
        """
        def _initial(name, field):
            val = self.initial.get(name, field.initial)
            if not val:
                return val
            return unicode(val).encode('1251')

        fields = [(name, _initial(name, field))
                  for name, field in self.fields.items()
                  if _initial(name, field)
                 ]
        params = urlencode(fields)
        return self.target+'?'+params

    def __init__(self, *args, **kwargs):
        super(RobokassaForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget = forms.HiddenInput()
        self.fields['SignatureValue'].initial = self._get_signature()

    def _get_signature_string(self):
        def _val(name):
            value = self.initial[name] if name in self.initial else self.fields[name].initial
            if value is None:
                return ''
            return unicode(value)
        return ':'.join([_val('MrchLogin'), _val('OutSum'), _val('InvId'), PASSWORD1])

    def _get_signature(self):
        return md5(self._get_signature_string()).hexdigest().upper()


class ResultURLForm(forms.Form):
    '''Форма для приема результатов и проверки контрольной суммы '''
    OutSum = forms.CharField(max_length=15)
    InvId = forms.IntegerField(min_value=0)
    SignatureValue = forms.CharField(max_length=32)

    def clean(self):
        if self.cleaned_data['SignatureValue'].upper() != self._get_signature():
            raise forms.ValidationError(u'Ошибка в контрольной сумме')
        return self.cleaned_data

    def _get_signature_string(self):
        _val = lambda name: unicode(self.cleaned_data[name])
        return ':'.join([_val('OutSum'), _val('InvId'), PASSWORD2])

    def _get_signature(self):
        return md5(self._get_signature_string()).hexdigest().upper()


class _RedirectPageForm(ResultURLForm):
    '''Форма для проверки контрольной суммы на страницах Success и Fail'''

    Culture = forms.CharField(max_length=3)

    def _get_signature_string(self):
        _val = lambda name: unicode(self.cleaned_data[name])
        return ':'.join([_val('OutSum'), _val('InvId'), PASSWORD1])


class FailRedirectForm(_RedirectPageForm):
    pass

class SuccessRedirectForm(_RedirectPageForm):
    """ Форма для обработки страницы Success с дополнительной защитой. Она
    проверяет, что ROBOKASSA предварительно уведомила систему о платеже,
    отправив запрос на ResultURL. """

    def clean(self):
        data = super(SuccessRedirectForm, self).clean()
        if STRICT_CHECK:
            try:
                notification = SuccessNotification.objects.get(InvId=data['InvId'])
            except SuccessNotification.DoesNotExist:
                raise forms.ValidationError(u'От ROBOKASSA не было предварительного уведомления')
        return data

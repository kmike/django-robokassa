#coding: utf-8

from hashlib import md5
from urllib import urlencode
from django import forms
from robokassa.conf import LOGIN, PASSWORD1

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
    target = u'https://merchant.roboxchange.com/Index.aspx'

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

    def _get_signature(self):
        _val = lambda name: self.fields[name].initial
        params = ':'.join(filter(None, [_val('MrchLogin'), _val('OutSum'), _val('InvId'), PASSWORD1]))
        return md5(params).hexdigest().upper()


#coding: utf-8
from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from robokassa.forms import RobokassaForm, ResultURLForm
from robokassa.conf import PASSWORD1, LOGIN

class RobokassaFormTest(TestCase):

    def setUp(self):
        self.form = RobokassaForm(initial = {
                       'OutSum': 100.00,
                       'InvId': 58,
                       'Desc' : u'Холодильник "Бирюса"',
                       'Email' : 'vasia@example.com'
                    })

    def testSignature(self):
        self.assertEqual(self.form._get_signature_string(), '%s:100.0:58:%s' % (LOGIN, PASSWORD1))
        self.assertEqual(len(self.form.fields['SignatureValue'].initial), 32)
        self.assertEqual(self.form.fields['SignatureValue'].initial, '59506E1E5BBE937B31386DD981788C9B')

    def testSignatureMissingParams(self):
        form = RobokassaForm(initial = {'InvId': 5})
        self.assertEqual(form._get_signature_string(), '%s::5:%s' % (LOGIN, PASSWORD1))
        self.assertEqual(form.fields['SignatureValue'].initial, 'DCEDD9C5F84C1E6CB73AB52CA9FAA8B3')

    def testRedirectUrl(self):
        url = "https://merchant.roboxchange.com/Index.aspx?MrchLogin=test_login&OutSum=100.0&InvId=58&Desc=%D5%EE%EB%EE%E4%E8%EB%FC%ED%E8%EA+%22%C1%E8%F0%FE%F1%E0%22&SignatureValue=59506E1E5BBE937B31386DD981788C9B&Email=vasia%40example.com"
        self.assertEqual(self.form.get_redirect_url(), url)


class ResultURLTest(DjangoTestCase):

    def setUp(self):
        self.valid_data = {
                'OutSum': '100',
                'InvId': '58',
                'SignatureValue': '6E75B4F55BEFE22C8DB12778D8EF32C3',
             }
        self.invalid_data = {
                'OutSum': '101',
                'InvId': '58',
                'SignatureValue': '6E75B4F55BEFE22C8DB12778D8EF32C3',
             }

    def testForm(self):
        self.assertTrue(ResultURLForm(self.valid_data).is_valid())
        self.assertFalse(ResultURLForm(self.invalid_data).is_valid())

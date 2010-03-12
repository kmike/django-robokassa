#coding: utf-8

from unittest import TestCase

from robokassa.forms import RobokassaForm

class RobokassaFormTest(TestCase):

    def setUp(self):
        self.form = RobokassaForm(initial = {
                   'OutSum': 100.00,
                   'InvId': 58,
                   'Desc' : u'Холодильник "Бирюса"',
                   'Email' : 'vasia@example.com'
               })

    def testSignature(self):
        self.assertEqual(len(self.form.fields['SignatureValue'].initial), 32)
        self.assertEqual(self.form.fields['SignatureValue'].initial, 'FBA6DB00B521BB848CD44D0F01D7BFC8')

    def testRedirectUrl(self):
        url = "https://merchant.roboxchange.com/Index.aspx?MrchLogin=test_login&OutSum=100.0&InvId=58&Desc=%D5%EE%EB%EE%E4%E8%EB%FC%ED%E8%EA+%22%C1%E8%F0%FE%F1%E0%22&SignatureValue=FBA6DB00B521BB848CD44D0F01D7BFC8&Email=vasia%40example.com"
        self.assertEqual(self.form.get_redirect_url(), url)
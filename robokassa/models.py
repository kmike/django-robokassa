#coding: utf-8

from datetime import datetime
from django.db import models

class SuccessNotification(models.Model):
    InvId = models.IntegerField(u'Номер заказа', db_index=True)
    OutSum = models.CharField(u'Сумма', max_length=15)

    created_at = models.DateTimeField(u'Дата и время получения уведомления', default = datetime.now)

    def __unicode__(self):
        return u'#%d: %s (%s)' % (self.InvId, self.OutSum, self.created_at)

    class Meta:
        verbose_name = u'Уведомление об успешном платеже'
        verbose_name_plural = u'Уведомления об успешных платежах (ROBOKASSA)'

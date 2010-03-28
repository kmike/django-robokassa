#coding: utf-8

from south.db import db
from django.db import models
from robokassa.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'SuccessNotification'
        db.create_table('robokassa_successnotification', (
            ('id', orm['robokassa.SuccessNotification:id']),
            ('InvId', orm['robokassa.SuccessNotification:InvId']),
            ('OutSum', orm['robokassa.SuccessNotification:OutSum']),
            ('created_at', orm['robokassa.SuccessNotification:created_at']),
        ))
        db.send_create_signal('robokassa', ['SuccessNotification'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'SuccessNotification'
        db.delete_table('robokassa_successnotification')
        
    
    
    models = {
        'robokassa.successnotification': {
            'InvId': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'OutSum': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }
    
    complete_apps = ['robokassa']

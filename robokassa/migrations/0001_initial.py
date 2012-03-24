# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SuccessNotification'
        db.create_table('robokassa_successnotification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('InvId', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('OutSum', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('robokassa', ['SuccessNotification'])

    def backwards(self, orm):
        # Deleting model 'SuccessNotification'
        db.delete_table('robokassa_successnotification')

    models = {
        'robokassa.successnotification': {
            'InvId': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'Meta': {'object_name': 'SuccessNotification'},
            'OutSum': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['robokassa']
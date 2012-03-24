# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'SuccessNotification.created_at'
        db.alter_column('robokassa_successnotification', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))
    def backwards(self, orm):

        # Changing field 'SuccessNotification.created_at'
        db.alter_column('robokassa_successnotification', 'created_at', self.gf('django.db.models.fields.DateTimeField')())
    models = {
        'robokassa.successnotification': {
            'InvId': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'Meta': {'object_name': 'SuccessNotification'},
            'OutSum': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['robokassa']
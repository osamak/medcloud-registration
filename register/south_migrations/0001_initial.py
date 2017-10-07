# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Registration'
        db.create_table(u'register_registration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=200)),
            ('batch', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('section', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('unisersity_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_successful', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'register', ['Registration'])


    def backwards(self, orm):
        # Deleting model 'Registration'
        db.delete_table(u'register_registration')


    models = {
        u'register.registration': {
            'Meta': {'object_name': 'Registration'},
            'batch': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_successful': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'unisersity_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['register']
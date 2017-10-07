# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Registration.forgotten_password'
        db.add_column(u'register_registration', 'forgotten_password',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Registration.submission_date'
        db.add_column(u'register_registration', 'submission_date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Registration.edit_date'
        db.add_column(u'register_registration', 'edit_date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Registration.forgotten_password'
        db.delete_column(u'register_registration', 'forgotten_password')

        # Deleting field 'Registration.submission_date'
        db.delete_column(u'register_registration', 'submission_date')

        # Deleting field 'Registration.edit_date'
        db.delete_column(u'register_registration', 'edit_date')


    models = {
        u'register.registration': {
            'Meta': {'object_name': 'Registration'},
            'batch': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'edit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '200'}),
            'forgotten_password': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_successful': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'unisersity_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['register']
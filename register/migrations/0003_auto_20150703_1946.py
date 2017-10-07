# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def create_batches(apps, schema_editor):
    Registration = apps.get_model('register', 'Registration')
    Batch = apps.get_model('register', 'Batch')
    for number in range(9, 13):
        Batch.objects.create(
            college='M',
            number=number)
    for number in range(1, 6):
        Batch.objects.create(
            college='P',
            number=number)
        Batch.objects.create(
            college='D',
            number=number)
    for number in range(13, 17):
        Batch.objects.create(
            college='N',
            number=number)

    m12 = Batch.objects.get(college='M', number=12)
    m11 = Batch.objects.get(college='M', number=11)
    m10 = Batch.objects.get(college='M', number=10)
    m9 = Batch.objects.get(college='M', number=9)

    Registration.objects.filter(batch='B12').update(group=m12)
    Registration.objects.filter(batch='B11').update(group=m11)
    Registration.objects.filter(batch='B10').update(group=m10)
    Registration.objects.filter(batch='B9').update(group=m9)

def remove_batches(apps, schema_editor):
    Batch = apps.get_model('Batch', 'register')
    Batch.objects.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_auto_20150703_1946'),
    ]

    operations = [
       migrations.RunPython(
            create_batches,
            reverse_code=remove_batches),
    ]

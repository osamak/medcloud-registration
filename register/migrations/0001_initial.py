# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=200, verbose_name='\u0627\u0644\u0628\u0631\u064a\u062f \u0627\u0644\u062c\u0627\u0645\u0639\u064a')),
                ('batch', models.CharField(max_length=3, verbose_name='\u0627\u0644\u062f\u0641\u0639\u0629')),
                ('section', models.CharField(max_length=2, verbose_name='\u0627\u0644\u0642\u0633\u0645')),
                ('unisersity_id', models.PositiveIntegerField(verbose_name='\u0627\u0644\u0631\u0642\u0645 \u0627\u0644\u062c\u0627\u0645\u0639\u064a')),
                ('password', models.CharField(max_length=6)),
                ('date', models.DateTimeField(auto_now=True, verbose_name=b'date')),
                ('is_successful', models.BooleanField(default=False)),
                ('forgotten_password', models.BooleanField(default=False)),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644', null=True)),
                ('edit_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644', null=True)),
            ],
        ),
    ]

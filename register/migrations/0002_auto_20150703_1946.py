# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.PositiveSmallIntegerField(verbose_name='\u0631\u0642\u0645 \u0627\u0644\u062f\u0641\u0639\u0629')),
                ('college', models.CharField(max_length=1, verbose_name='\u0627\u0644\u0643\u0644\u064a\u0629', choices=[(b'M', '\u0643\u0644\u064a\u0629 \u0627\u0644\u0637\u0628'), (b'D', '\u0643\u0644\u064a\u0629 \u0627\u0644\u0623\u0633\u0646\u0627\u0646'), (b'P', '\u0643\u0644\u064a\u0629 \u0627\u0644\u0635\u064a\u062f\u0644\u0629'), (b'N', '\u0643\u0644\u064a\u0629 \u0627\u0644\u062a\u0645\u0631\u064a\u0636')])),
            ],
        ),
        migrations.AddField(
            model_name='registration',
            name='group',
            field=models.ForeignKey(verbose_name='\u0627\u0644\u062f\u0641\u0639\u0629', to='register.Batch', null=True),
        ),
    ]

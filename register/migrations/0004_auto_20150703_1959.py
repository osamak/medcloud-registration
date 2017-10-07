# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_auto_20150703_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u062f\u0641\u0639\u0629', to='register.Batch', null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-23 09:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20160103_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='user',
            field=models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

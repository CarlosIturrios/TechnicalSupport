# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-08 03:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ordermanager', '0011_auto_20180607_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]

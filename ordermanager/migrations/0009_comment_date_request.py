# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-07 03:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordermanager', '0008_auto_20180606_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='date_request',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]

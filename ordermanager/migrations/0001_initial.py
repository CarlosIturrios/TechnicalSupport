# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-05 02:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('responsible', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='equipment_user_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_type', models.CharField(choices=[('1', 'Maintenance of computer equipment'), ('2', 'Software configuration'), ('3', 'Software installation'), ('4', 'Computer consulting'), ('3', 'Audio'), ('4', 'Events in general')], default='1', max_length=1)),
                ('status', models.CharField(choices=[('1', 'Pennding'), ('2', 'on process'), ('3', 'Canceled'), ('4', 'Done')], default='1', max_length=1)),
                ('comments', models.CharField(blank=True, max_length=200, null=True)),
                ('date_request', models.DateTimeField(auto_now_add=True)),
                ('date_onprocess', models.DateTimeField(blank=True, null=True)),
                ('date_done', models.DateTimeField(blank=True, null=True)),
                ('date_cancel', models.DateTimeField(blank=True, null=True)),
                ('equipment_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='equipment_set', to='ordermanager.Equipment')),
                ('technical', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='request_technical_set', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='request_user_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

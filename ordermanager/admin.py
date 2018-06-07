# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Request)
admin.site.register(models.Equipment)
admin.site.register(models.Poll)
admin.site.register(models.Activity)
admin.site.register(models.Comment)
admin.site.register(models.Department)
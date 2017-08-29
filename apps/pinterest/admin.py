# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Pin, Board, Topic

# Register your models here.
admin.site.register(Pin)
admin.site.register(Board)
admin.site.register(Topic)
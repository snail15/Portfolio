# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
    return render(request, 'portfoliosite/index.html')
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import urllib

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse #email sender
from django.template import Context #email sender
from django.template.loader import render_to_string, get_template #email sender
from django.core.mail import EmailMessage, EmailMultiAlternatives #email sender
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.conf import settings

from datetime import datetime
from .models import Request

# Create your views here.
@login_required()
def principal(request):
	requests = Request.objects.filter(user=request.user)
	return render(request, 'principal.html', {'requests':requests})


def createOrder(request):
	return render(request, 'createOrder.html')


def dashboard(request):
	return render(request, 'dashboard.html')


def orderPending(request):
	return render(request, 'orderPending.html')


def orderSupport(request):
	return render(request, 'orderSupport.html')


def poll(request):
	return render(request, 'poll.html')
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
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.db.models import Q

from datetime import datetime
from .models import Request, Poll, Activity, Comment, Equipment

# Create your views here.
@login_required()
def principal(request):
	requests = Request.objects.filter(~Q(status='3'), ~Q(status='4'), user=request.user)
	allrequests = Request.objects.filter(~Q(status='3'), ~Q(status='4'))[:5]
	myrequests = Request.objects.filter(user=request.user).order_by('status')
	comments = Comment.objects.all().order_by('id').reverse()
	activities = Activity.objects.all().order_by('id').reverse()
	return render(request, 'principal.html', {'requests':requests, 'allrequests':allrequests, 'myrequests':myrequests, 'comments':comments, 'activities':activities})
 

@login_required()
def createOrder(request, int):
	maintype = int
	equipments = Equipment.objects.all()
	if request.method == "POST":		
		comments = request.POST.get('comments', None)		
		req = Request()
		req.user = request.user
		req.request_type = maintype
		if maintype == '1' or maintype == '6':
			slequipment = request.POST.get('slequipment', None)
			req.equipment_id = Equipment(id=slequipment)
		req.status = '1'
		req.comments = comments
		req.date_onprocess = datetime.now()
		req.save()
		return redirect('ordermanager:principal')
	return render(request, 'createOrder.html', {'maintype':maintype, 'equipments':equipments})


@login_required()
@permission_required('ordermanager.add_poll')
def dashboard(request):
	return render(request, 'dashboard.html')


@login_required()
@permission_required('ordermanager.add_request')
def orderPending(request):
	principal_requests = Request.objects.filter(user__profile__department='1')
	admin_requests = Request.objects.filter(~Q(user__profile__department='1')).order_by('user__groups')
	return render(request, 'orderPending.html', {'principal_requests':principal_requests, 'admin_requests':admin_requests})


@login_required()
@permission_required('ordermanager.add_request')
def orderSupport(request, pk):
	principal_request = get_object_or_404(Request, pk=pk)
	
	return render(request, 'orderSupport.html', {'principal_request':principal_request})


@login_required()
def poll(request):
	return render(request, 'poll.html')


@login_required()
def comment(request):
	if request.method == "POST":		
		comments = request.POST.get('comments', None)		
		comen = Comment()
		comen.user = request.user
		comen.comment = comments
		comen.save()
		return redirect('ordermanager:principal')
	return render(request, 'comment.html')
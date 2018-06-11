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
from django.contrib import messages
from django.conf import settings
from django.db.models import Q

from datetime import datetime
from .models import Request, Poll, Activity, Comment, Equipment

# Create your views here.
@login_required()
def principal(request):
	requests = Request.objects.filter(~Q(status='3'), ~Q(status='4'), user=request.user)
	allrequests = Request.objects.filter(~Q(status='3'), ~Q(status='4')).order_by('status').reverse()[:5]
	myrequests = Request.objects.filter(user=request.user).order_by('status')
	comments = Comment.objects.all().order_by('id').reverse()
	activities = Activity.objects.all().order_by('id').reverse()
	polls = Poll.objects.filter(request_id__user = request.user, status='1')
	return render(request, 'principal.html', {'requests':requests, 'allrequests':allrequests, 'myrequests':myrequests, 'comments':comments, 'activities':activities, 'polls':polls})
 

@login_required()
def createOrder(request, int):
	requests = Request.objects.filter(~Q(status='3'), ~Q(status='4'), user=request.user)
	maintype = int
	equipments = Equipment.objects.filter(responsible=request.user)
	reques = Request.objects.filter(user=request.user)
	for reque in reques:
		thepoll = Poll.objects.get(request_id = reque.id)
		if thepoll.status == '1':
			messages.error(request, 'You have to do the poll before to create a new request!')
			return redirect('ordermanager:poll', thepoll.pk)
	
	if request.method == "POST":		
		comments = request.POST.get('comments', None)		
		req = Request()
		req.user = request.user
		req.request_type = maintype
		if maintype == '1' or maintype == '6':
			slequipment = request.POST.get('slequipment', None)
			if slequipment == '3':
				print('hola')
			else:
				req.equipment_id = Equipment(id=slequipment)
		req.status = '1'
		req.comments = comments
		req.date_onprocess = datetime.now()
		req.save()
		poll = Poll()
		poll.request_id = req
		poll.status = 1
		poll.save()		
		messages.warning(request, 'Do not forget do the poll when the technical finishes the service!')
		messages.success(request, 'Your order was created successfully!')
		return redirect('ordermanager:principal')
	return render(request, 'createOrder.html', {'requests':requests, 'maintype':maintype, 'equipments':equipments})


@login_required()
@permission_required('ordermanager.add_poll')
def dashboard(request):
	requests = Request.objects.filter(~Q(status='3'), ~Q(status='4'), user=request.user)
	return render(request, 'dashboard.html', {'requests':requests})


@login_required()
@permission_required('ordermanager.add_request')
def orderPending(request):
	requests = Request.objects.filter(~Q(status='3'), ~Q(status='4'), user=request.user)
	principal_requests = Request.objects.filter(user__profile__department='1')
	admin_requests = Request.objects.filter(~Q(status='2'), ~Q(status='3'), ~Q(status='4'), ~Q(user__profile__department='1')).order_by('user__groups')
	return render(request, 'orderPending.html', {'requests':requests, 'principal_requests':principal_requests, 'admin_requests':admin_requests})


@login_required()
@permission_required('ordermanager.add_request')
def orderSupport(request, pk):
	requests = Request.objects.filter(~Q(status='3'), ~Q(status='4'), user=request.user)
	principal_request = get_object_or_404(Request, pk=pk)
	if request.method == "GET":
		principal_request.status = '2'
		principal_request.date_onprocess = datetime.now()
		principal_request.save()
	elif request.method == "POST":
		observations = request.POST.get('observations', None)
		principal_request.status = '4'
		principal_request.observations = observations
		principal_request.date_done = datetime.now()
		messages.success(request, 'The order is done!')
		principal_request.save()
		return redirect('ordermanager:orderPending')
	return render(request, 'orderSupport.html', {'requests':requests, 'principal_request':principal_request})


@login_required()
def poll(request, pk):
	poll = get_object_or_404(Poll, pk=pk)
	requests = Request.objects.filter(~Q(status='3'), ~Q(status='4'), user=request.user)
	if request.method == "POST":
		answer = request.POST.get('answer', None)
		answerTwo = request.POST.get('answerTwo', None)
		answerThree = request.POST.get('answerThree', None)
		answerFour = request.POST.get('answerFour', None)
		answerFive = request.POST.get('answerFive', None)		
		poll.answer = answer
		poll.answerTwo = answerTwo
		poll.answerThree = answerThree
		poll.answerFour = answerFour
		poll.answerFive = answerFive
		poll.status = '2'
		poll.save()	
		return redirect('ordermanager:principal')
	return render(request, 'poll.html', {'requests':requests, 'poll':poll})


@login_required()
def comment(request):
	if request.method == "POST":		
		comments = request.POST.get('comments', None)		
		comen = Comment()
		comen.user = request.user
		comen.comment = comments
		comen.save()
		messages.success(request, 'Your comment was created successfully!')
		return redirect('ordermanager:principal')
	return render(request, 'comment.html')


@login_required()
def orderCancel(request, pk):
	principal_request = get_object_or_404(Request, pk=pk)
	if request.method == "POST":
		principal_request.status = '3'
		messages.error(request, 'The order was Canceled successfully!')
		return redirect('ordermanager:orderPending')
	return render(request, 'orderCancel.html', {'principal_request':principal_request})


@login_required()
@permission_required('ordermanager.add_request')
def reports(request):
	principal_requests = Request.objects.all()
	return render(request, 'reports.html', {'principal_requests':principal_requests})
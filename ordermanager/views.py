# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import urllib

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse  # email sender
from django.template import Context  # email sender
from django.template.loader import render_to_string, get_template  # email sender
from django.core.mail import EmailMessage, EmailMultiAlternatives  # email sender
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.conf import settings
from django.db.models import Q

from datetime import datetime
from .models import Request, Poll, Activity, Comment, Equipment, Preventive_Maintenance, Equipment_Maintenance


# Create your views here.
@login_required()
def principal(request):
    requests = Request.objects.filter(~Q(status='3'), ~Q(status='4'), user=request.user)
    allrequests = Request.objects.filter(~Q(status='3'), ~Q(status='4')).order_by('status').reverse()[:5]
    myrequests = Request.objects.filter(user=request.user).order_by('status')
    comments = Comment.objects.all().order_by('id').reverse()[:5]
    activities = Activity.objects.all().order_by('id').reverse()
    polls = Poll.objects.filter(request_id__user=request.user, status='1', request_id__status='4')
    numrequest = Request.objects.filter(~Q(status='3'), ~Q(status='4')).order_by('status').reverse().count()
    userrequest = Request.objects.filter(user=request.user, status='1').first()
    if userrequest:
        print(userrequest)
        userrequest = int(userrequest.pk)
        requestlast = Request.objects.filter(~Q(status='3'), ~Q(status='4')).reverse().first()
        print(requestlast)
        requestlast = int(requestlast.pk)
        if userrequest - requestlast == 0:
            numrequest = int(numrequest) - 1
        else:
            numrequest = (int(numrequest) - (requestlast - userrequest)) - 1
    return render(request, 'principal.html', {
        'requests': requests,
        'allrequests': allrequests,
        'myrequests': myrequests,
        'comments': comments,
        'activities': activities,
        'polls': polls,
        'userrequest': userrequest,
        'numrequest': numrequest})


@login_required()
def createOrder(request, int):
    requests = Request.objects.filter(~Q(status='3'), ~Q(status='4'), user=request.user)
    maintype = int
    equipments = Equipment.objects.filter(responsible=request.user)
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
        req.save()
        poll = Poll()
        poll.request_id = req
        poll.status = 1
        poll.save()
        messages.warning(request, 'Do not forget do the poll when the technical finishes the service!')
        messages.success(request, 'Your order was created successfully!')
        return redirect('ordermanager:principal')
    return render(request, 'createOrder.html', {'requests': requests, 'maintype': maintype, 'equipments': equipments})


@login_required()
@permission_required('ordermanager.add_poll')
def dashboard(request):
    requests = Request.objects.filter(~Q(status='3'), ~Q(status='4'), user=request.user)
    cancelRequest = Request.objects.filter(status='3').count()
    penndingRequest = Request.objects.filter(status='1').count()
    onProcessRequest = Request.objects.filter(status='2').count()
    doneRequest = Request.objects.filter(status='4').count()
    allrequsts = float(Request.objects.all().count())
    cancel = Request.objects.filter(status='3').count()
    pennding = Request.objects.filter(status='1').count()
    onProcess = Request.objects.filter(status='2').count()
    if allrequsts == 0:
        done = 0
        onProcess = 0
        pennding = 0
        cancel = 0
        messages.error(request, 'There is not any request!')
    else:
        done = Request.objects.filter(status='4').count()
        done = float((done * 100) / allrequsts)
        done = float(("%0.2f" % done))
        onProcess = float((onProcess * 100) / allrequsts)
        onProcess = float(("%0.2f" % onProcess))
        pennding = float((pennding * 100) / allrequsts)
        pennding = float(("%0.2f" % pennding))
        cancel = float((cancel * 100) / allrequsts)
        cancel = float(("%0.2f" % cancel))
        if request.method == "POST":
            date = request.POST.get('date', None)
            dateTwo = request.POST.get('dateTwo', None)
            cancelRequest = Request.objects.filter(date_request__range=[date, dateTwo], status='3').count()
            penndingRequest = Request.objects.filter(date_request__range=[date, dateTwo], status='1').count()
            onProcessRequest = Request.objects.filter(date_request__range=[date, dateTwo], status='2').count()
            doneRequest = Request.objects.filter(date_request__range=[date, dateTwo], status='4').count()
            allrequsts = float(Request.objects.filter(date_request__range=[date, dateTwo]).count())
            if allrequsts != 0:
                cancel = Request.objects.filter(date_request__range=[date, dateTwo], status='3').count()
                pennding = Request.objects.filter(date_request__range=[date, dateTwo], status='1').count()
                onProcess = Request.objects.filter(date_request__range=[date, dateTwo], status='2').count()
                done = Request.objects.filter(date_request__range=[date, dateTwo], status='4').count()
                done = float((done * 100) / allrequsts)
                done = float(("%0.2f" % done))
                onProcess = float((onProcess * 100) / allrequsts)
                onProcess = float(("%0.2f" % onProcess))
                pennding = float((pennding * 100) / allrequsts)
                pennding = float(("%0.2f" % pennding))
                cancel = float((cancel * 100) / allrequsts)
                cancel = float(("%0.2f" % cancel))
            else:
                done = 0
                onProcess = 0
                pennding = 0
                cancel = 0
                messages.error(request, 'There is not any request!')
    return render(request, 'dashboard.html', {
        'requests': requests,
        'cancelRequest': cancelRequest,
        'penndingRequest': penndingRequest,
        'onProcessRequest': onProcessRequest,
        'doneRequest': doneRequest,
        'allrequsts': allrequsts,
        'cancel': cancel,
        'pennding': pennding,
        'onProcess': onProcess,
        'done': done})


@login_required()
@permission_required('ordermanager.add_poll')
def request_type_dashboard(request):
    requests = Request.objects.filter(~Q(status='3'), ~Q(status='4'), user=request.user)
    maintenanceComputer = Request.objects.filter(request_type='1').count()
    softwareConfiguration = Request.objects.filter(request_type='2').count()
    softwareInstallation = Request.objects.filter(request_type='3').count()
    computerConsulting = Request.objects.filter(request_type='4').count()
    audioCount = Request.objects.filter(request_type='5').count()
    eventsGeneral = Request.objects.filter(request_type='6').count()
    allrequsts = float(Request.objects.all().count())
    if allrequsts == 0:
        maintenance = 0
        configuration = 0
        installation = 0
        consulting = 0
        audio = 0
        events = 0
        messages.error(request, 'There is not any request!')
    else:
        maintenance = Request.objects.filter(request_type='1').count()
        maintenance = float((maintenance * 100) / allrequsts)
        maintenance = float(("%0.2f" % maintenance))
        configuration = Request.objects.filter(request_type='2').count()
        configuration = float((configuration * 100) / allrequsts)
        configuration = float(("%0.2f" % configuration))
        installation = Request.objects.filter(request_type='3').count()
        installation = float((installation * 100) / allrequsts)
        installation = float(("%0.2f" % installation))
        consulting = Request.objects.filter(request_type='4').count()
        consulting = float((consulting * 100) / allrequsts)
        consulting = float(("%0.2f" % consulting))
        audio = Request.objects.filter(request_type='5').count()
        audio = float((audio * 100) / allrequsts)
        audio = float(("%0.2f" % audio))
        events = Request.objects.filter(request_type='6').count()
        events = float((events * 100) / allrequsts)
        events = float(("%0.2f" % events))
        if request.method == "POST":
            date = request.POST.get('date', None)
            dateTwo = request.POST.get('dateTwo', None)
            maintenanceComputer = Request.objects.filter(date_request__range=[date, dateTwo], request_type='1').count()
            softwareConfiguration = Request.objects.filter(date_request__range=[date, dateTwo],
                                                           request_type='2').count()
            softwareInstallation = Request.objects.filter(date_request__range=[date, dateTwo], request_type='3').count()
            computerConsulting = Request.objects.filter(date_request__range=[date, dateTwo], request_type='4').count()
            audioCount = Request.objects.filter(date_request__range=[date, dateTwo], request_type='5').count()
            eventsGeneral = Request.objects.filter(date_request__range=[date, dateTwo], request_type='6').count()
            allrequsts = float(Request.objects.filter(date_request__range=[date, dateTwo]).count())
            if allrequsts != 0:
                maintenance = Request.objects.filter(date_request__range=[date, dateTwo], request_type='1').count()
                maintenance = float((maintenance * 100) / allrequsts)
                maintenance = float(("%0.2f" % maintenance))
                configuration = Request.objects.filter(date_request__range=[date, dateTwo], request_type='2').count()
                configuration = float((configuration * 100) / allrequsts)
                configuration = float(("%0.2f" % configuration))
                installation = Request.objects.filter(date_request__range=[date, dateTwo], request_type='3').count()
                installation = float((installation * 100) / allrequsts)
                installation = float(("%0.2f" % installation))
                consulting = Request.objects.filter(date_request__range=[date, dateTwo], request_type='4').count()
                consulting = float((consulting * 100) / allrequsts)
                consulting = float(("%0.2f" % consulting))
                audio = Request.objects.filter(date_request__range=[date, dateTwo], request_type='5').count()
                audio = float((audio * 100) / allrequsts)
                audio = float(("%0.2f" % audio))
                events = Request.objects.filter(date_request__range=[date, dateTwo], request_type='6').count()
                events = float((events * 100) / allrequsts)
                events = float(("%0.2f" % events))
            else:
                maintenance = 0
                configuration = 0
                installation = 0
                consulting = 0
                audio = 0
                events = 0
                messages.error(request, 'There is not any request!')
    return render(request, 'request_type_dashboard.html', {
        'requests': requests,
        'maintenanceComputer': maintenanceComputer,
        'softwareConfiguration': softwareConfiguration,
        'softwareInstallation': softwareInstallation,
        'computerConsulting': computerConsulting,
        'audioCount': audioCount,
        'eventsGeneral': eventsGeneral,
        'allrequsts': allrequsts,
        'maintenance': maintenance,
        'configuration': configuration,
        'installation': installation,
        'consulting': consulting,
        'audio': audio,
        'events': events})


@login_required()
@permission_required('ordermanager.add_poll')
def department_dashboard(request):
    requests = Request.objects.filter(~Q(status='3'), ~Q(status='4'), user=request.user)
    principalNumber = Request.objects.filter(user__profile__department='1').count()
    administrationNumber = Request.objects.filter(user__profile__department='2').count()
    linkingNumber = Request.objects.filter(user__profile__department='3').count()
    planningNumber = Request.objects.filter(user__profile__department='4').count()
    academicanNumber = Request.objects.filter(user__profile__department='5').count()
    allrequsts = float(Request.objects.all().count())
    if allrequsts == 0:
        principal = 0
        administration = 0
        linking = 0
        planning = 0
        academican = 0
        messages.error(request, 'There is not any request!')
    else:
        principal = Request.objects.filter(user__profile__department='1').count()
        principal = float((principal * 100) / allrequsts)
        principal = float(("%0.2f" % principal))
        administration = Request.objects.filter(user__profile__department='2').count()
        administration = float((administration * 100) / allrequsts)
        administration = float(("%0.2f" % administration))
        linking = Request.objects.filter(user__profile__department='3').count()
        linking = float((linking * 100) / allrequsts)
        linking = float(("%0.2f" % linking))
        planning = Request.objects.filter(user__profile__department='4').count()
        planning = float((planning * 100) / allrequsts)
        planning = float(("%0.2f" % planning))
        academican = Request.objects.filter(user__profile__department='5').count()
        academican = float((academican * 100) / allrequsts)
        academican = float(("%0.2f" % academican))
        if request.method == "POST":
            date = request.POST.get('date', None)
            dateTwo = request.POST.get('dateTwo', None)
            principalNumber = Request.objects.filter(date_request__range=[date, dateTwo],
                                                     user__profile__department='1').count()
            administrationNumber = Request.objects.filter(date_request__range=[date, dateTwo],
                                                          user__profile__department='2').count()
            linkingNumber = Request.objects.filter(date_request__range=[date, dateTwo],
                                                   user__profile__department='3').count()
            planningNumber = Request.objects.filter(date_request__range=[date, dateTwo],
                                                    user__profile__department='4').count()
            academicanNumber = Request.objects.filter(date_request__range=[date, dateTwo],
                                                      user__profile__department='5').count()
            allrequsts = float(Request.objects.filter(date_request__range=[date, dateTwo]).count())
            if allrequsts != 0:
                principal = Request.objects.filter(date_request__range=[date, dateTwo],
                                                   user__profile__department='1').count()
                principal = float((principal * 100) / allrequsts)
                principal = float(("%0.2f" % principal))
                administration = Request.objects.filter(date_request__range=[date, dateTwo],
                                                        user__profile__department='2').count()
                administration = float((administration * 100) / allrequsts)
                administration = float(("%0.2f" % administration))
                linking = Request.objects.filter(date_request__range=[date, dateTwo],
                                                 user__profile__department='3').count()
                linking = float((linking * 100) / allrequsts)
                linking = float(("%0.2f" % linking))
                planning = Request.objects.filter(date_request__range=[date, dateTwo],
                                                  user__profile__department='4').count()
                planning = float((planning * 100) / allrequsts)
                planning = float(("%0.2f" % planning))
                academican = Request.objects.filter(date_request__range=[date, dateTwo],
                                                    user__profile__department='5').count()
                academican = float((academican * 100) / allrequsts)
                academican = float(("%0.2f" % academican))
            else:
                principal = 0
                administration = 0
                linking = 0
                planning = 0
                academican = 0
                messages.error(request, 'There is not any request!')
    return render(request, 'department_dashboard.html', {
        'requests': requests,
        'principalNumber': principalNumber,
        'administrationNumber': administrationNumber,
        'linkingNumber': linkingNumber,
        'planningNumber': planningNumber,
        'academicanNumber': academicanNumber,
        'allrequsts': allrequsts,
        'principal': principal,
        'administration': administration,
        'linking': linking,
        'planning': planning,
        'academican': academican})


@login_required()
@permission_required('ordermanager.add_request')
def orderPending(request):
    requests = Request.objects.filter(~Q(status='3'), ~Q(status='4'), user=request.user)
    principal_requests = Request.objects.filter(~Q(status='2'), ~Q(status='3'),
                                                ~Q(status='4'), user__profile__department='1')
    admin_requests = Request.objects.filter(~Q(status='2'), ~Q(status='3'), ~Q(status='4'), ~Q(status='5'),
                                            ~Q(user__profile__department='1')).order_by('user__groups')
    pause_requests = Request.objects.filter(~Q(status='1'), ~Q(status='2'), ~Q(status='3'), ~Q(status='4')).order_by(
        'user__groups')
    maintenances = Preventive_Maintenance.objects.filter(~Q(status='2'), ~Q(status='3'), ~Q(status='4'), ~Q(status='5'))
    maintenances_pause = Preventive_Maintenance.objects.filter(~Q(status='1'), ~Q(status='2'), ~Q(status='3'),
                                                               ~Q(status='4'))
    return render(request, 'orderPending.html', {'requests': requests, 'principal_requests': principal_requests,
                                                 'admin_requests': admin_requests, 'pause_requests': pause_requests,
                                                 'maintenances': maintenances,
                                                 'maintenances_pause': maintenances_pause})


@login_required()
@permission_required('ordermanager.add_request')
def orderSupport(request, pk):
    requests = Request.objects.filter(~Q(status='3'), ~Q(status='4'), user=request.user)
    principal_request = get_object_or_404(Request, pk=pk)
    if request.method == "GET":
        principal_request.status = '2'
        principal_request.technical = request.user
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
    return render(request, 'orderSupport.html', {'requests': requests, 'principal_request': principal_request})


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
    return render(request, 'poll.html', {'requests': requests, 'poll': poll})


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
@permission_required('ordermanager.add_request')
def orderCancel(request, pk):
    principal_request = get_object_or_404(Request, pk=pk)
    if request.method == "POST":
        principal_request.status = '3'
        principal_request.technical = request.user
        principal_request.date_cancel = datetime.now()
        principal_request.save()
        messages.error(request, 'The order was Canceled successfully!')
        return redirect('ordermanager:orderPending')
    return render(request, 'orderCancel.html', {'principal_request': principal_request})


@login_required()
@permission_required('ordermanager.add_request')
def orderPause(request, pk):
    principal_request = get_object_or_404(Request, pk=pk)
    if request.method == "POST":
        principal_request.status = '5'
        principal_request.technical = request.user
        principal_request.date_pause = datetime.now()
        principal_request.save()
        messages.info(request, 'The order is on Pause!')
        return redirect('ordermanager:orderPending')
    return render(request, 'order_pause.html', {'principal_request': principal_request})


@login_required()
@permission_required('ordermanager.add_poll')
def reports(request):
    principal_requests = Request.objects.all()
    if request.method == "POST":
        date = request.POST.get('date', None)
        dateTwo = request.POST.get('dateTwo', None)
        principal_requests = Request.objects.filter(date_request__range=[date, dateTwo])
    return render(request, 'reports.html', {'principal_requests': principal_requests})


@login_required()
@permission_required('ordermanager.add_request')
def CreateMaintenance(request):
    requests = Request.objects.filter(~Q(status='3'), ~Q(status='4'), user=request.user)
    equipments = Equipment.objects.filter(responsible=request.user)
    if request.method == "POST":
        comments = request.POST.get('comments', None)
        req = Preventive_Maintenance()
        req.user = request.user
        req.status = '1'
        req.comments = comments
        req.save()
        for equipment in equipments:
            equipmentMaintenance = Equipment_Maintenance()
            equipmentMaintenance.preventive_maintenance_id = req
            equipmentMaintenance.equipment_id = equipment
            equipmentMaintenance.save()
        messages.success(request, 'Your order was created successfully!')
        return redirect('ordermanager:principal')
    return render(request, 'create_order_maintenance.html', {'requests': requests, 'equipments': equipments})


@login_required()
@permission_required('ordermanager.add_request')
def OrderObservations(request):
    requests = Request.objects.filter(~Q(status='3'), ~Q(status='4'), user=request.user)
    orders = Request.objects.all()
    maintenances = Preventive_Maintenance.objects.all()
    return render(request, 'order_observations.html',
                  {'requests': requests, 'orders': orders, 'maintenances': maintenances})


@login_required()
def orderShow(request, pk):
    requests = Request.objects.filter(~Q(status='3'), ~Q(status='4'), user=request.user)
    principal_request = get_object_or_404(Request, pk=pk)
    return render(request, 'order_show.html', {'requests': requests, 'principal_request': principal_request})


@login_required()
@permission_required('ordermanager.add_request')
def MaintenanceSupport(request, pk):
    requests = Request.objects.filter(~Q(status='3'), ~Q(status='4'), user=request.user)
    principal_request = get_object_or_404(Preventive_Maintenance, pk=pk)
    equipments = Equipment_Maintenance.objects.filter(preventive_maintenance_id=principal_request)
    if request.method == "GET":
        principal_request.status = '2'
        principal_request.technical = request.user
        principal_request.date_onprocess = datetime.now()
        principal_request.save()
    elif request.method == "POST":
        observations = request.POST.get('observations', None)
        principal_request.status = '4'
        principal_request.observations = observations
        principal_request.date_done = datetime.now()
        messages.success(request, 'The Maintenance is done!')
        principal_request.save()
        return redirect('ordermanager:orderPending')
    return render(request, 'maintenance_support.html',
                  {'requests': requests, 'principal_request': principal_request, 'equipments': equipments})


@login_required()
@permission_required('ordermanager.add_request')
def MaintenanceCancel(request, pk):
    principal_request = get_object_or_404(Preventive_Maintenance, pk=pk)
    if request.method == "POST":
        principal_request.status = '3'
        principal_request.technical = request.user
        principal_request.date_cancel = datetime.now()
        principal_request.save()
        messages.error(request, 'The maintenance was Canceled successfully!')
        return redirect('ordermanager:orderPending')
    return render(request, 'maintenance_cancel.html', {'principal_request': principal_request})


@login_required()
@permission_required('ordermanager.add_request')
def MaintenancePause(request, pk):
    principal_request = get_object_or_404(Preventive_Maintenance, pk=pk)
    if request.method == "POST":
        principal_request.status = '5'
        principal_request.technical = request.user
        principal_request.date_pause = datetime.now()
        principal_request.save()
        messages.info(request, 'The maintenance is on Pause!')
        return redirect('ordermanager:orderPending')
    return render(request, 'maintenance_pause.html', {'principal_request': principal_request})


def MaintenanceShow(request, pk):
    requests = Request.objects.filter(~Q(status='3'), ~Q(status='4'), user=request.user)
    principal_request = get_object_or_404(Preventive_Maintenance, pk=pk)
    equipments = Equipment_Maintenance.objects.filter(preventive_maintenance_id=principal_request)
    return render(request, 'maintenance_show.html', {'requests': requests, 'principal_request': principal_request,
                                                     'equipments': equipments})


def error_404_view(request, exception):
    data = {"name": "ThePythonDjango.com"}
    return render(request, '404_not_found.html', data)


@login_required()
@permission_required('ordermanager.add_poll')
def Poll_satisfaction(request):
    requests = Request.objects.filter(~Q(status='3'), ~Q(status='4'), user=request.user)
    if request.method == "POST":
        date = request.POST.get('date', None)
        dateTwo = request.POST.get('dateTwo', None)
        polls = Poll.objects.filter(date_request__range=[date, dateTwo], status='2')
        polls_total = polls.count()
    else:
        polls = Poll.objects.filter(status='2')
        polls_total = polls.count()

    verySatisfied = 0
    satisfied = 0
    Unsatisfied = 0
    veryUnsatisfied = 0

    uno_verySatisfied = 0
    dos_verySatisfied = 0
    tres_verySatisfied = 0
    cuatro_verySatisfied = 0
    cinco_verySatisfied = 0

    uno_satisfied = 0
    dos_satisfied = 0
    tres_satisfied = 0
    cuatro_satisfied = 0
    cinco_satisfied = 0

    uno_Unsatisfied = 0
    dos_Unsatisfied = 0
    tres_Unsatisfied = 0
    cuatro_Unsatisfied = 0
    cinco_Unsatisfied = 0

    uno_veryUnsatisfied = 0
    dos_veryUnsatisfied = 0
    tres_veryUnsatisfied = 0
    cuatro_veryUnsatisfied = 0
    cinco_veryUnsatisfied = 0

    for poll in polls:
        if poll.answer == '1':
            uno_verySatisfied += 1
        elif poll.answer == '2':
            uno_satisfied += 1
        elif poll.answer == '3':
            uno_Unsatisfied += 1
        elif poll.answer == '4':
            uno_veryUnsatisfied += 1

        if poll.answerTwo == '1':
            dos_verySatisfied += 1
        elif poll.answerTwo == '2':
            dos_satisfied += 1
        elif poll.answerTwo == '3':
            dos_Unsatisfied += 1
        elif poll.answerTwo == '4':
            dos_veryUnsatisfied += 1

        if poll.answerThree == '1':
            tres_verySatisfied += 1
        elif poll.answerThree == '2':
            tres_satisfied += 1
        elif poll.answerThree == '3':
            tres_Unsatisfied += 1
        elif poll.answerThree == '4':
            tres_veryUnsatisfied += 1

        if poll.answerFour == '1':
            cuatro_verySatisfied += 1
        elif poll.answerFour == '2':
            cuatro_satisfied += 1
        elif poll.answerFour == '3':
            cuatro_Unsatisfied += 1
        elif poll.answerFour == '4':
            cuatro_veryUnsatisfied += 1

        if poll.answerFive == '1':
            cinco_verySatisfied += 1
        elif poll.answerFive == '2':
            cinco_satisfied += 1
        elif poll.answerFive == '3':
            cinco_Unsatisfied += 1
        elif poll.answerFive == '4':
            cinco_veryUnsatisfied += 1
    if polls_total == 0:
        verySatisfied = 0
        satisfied = 0
        Unsatisfied = 0
        veryUnsatisfied = 0

        uno_verySatisfied = 0
        dos_verySatisfied = 0
        tres_verySatisfied = 0
        cuatro_verySatisfied = 0
        cinco_verySatisfied = 0

        cinco_satisfied = 0
        uno_satisfied = 0
        dos_satisfied = 0
        tres_satisfied = 0
        cuatro_satisfied = 0
        cinco_satisfied = 0

        uno_Unsatisfied = 0
        dos_Unsatisfied = 0
        tres_Unsatisfied = 0
        cuatro_Unsatisfied = 0
        cinco_Unsatisfied = 0

        uno_veryUnsatisfied = 0
        dos_veryUnsatisfied = 0
        tres_veryUnsatisfied = 0
        cuatro_veryUnsatisfied = 0
        cinco_veryUnsatisfied = 0
        messages.error(request, 'There is not any poll!')
    else:
        verySatisfied = uno_verySatisfied + dos_verySatisfied + tres_verySatisfied + cuatro_verySatisfied + cinco_verySatisfied
        verySatisfied = float(((verySatisfied * 100) / polls_total) / 5)
        verySatisfied = float(("%0.2f" % verySatisfied))

        satisfied = uno_satisfied + dos_satisfied + tres_satisfied + cuatro_satisfied + cinco_satisfied
        satisfied = float(((satisfied * 100) / polls_total) / 5)
        satisfied = float(("%0.2f" % satisfied))

        Unsatisfied = uno_Unsatisfied + dos_Unsatisfied + tres_Unsatisfied + cuatro_Unsatisfied + cinco_Unsatisfied
        Unsatisfied = float(((Unsatisfied * 100) / polls_total) / 5)
        Unsatisfied = float(("%0.2f" % Unsatisfied))

        veryUnsatisfied = uno_veryUnsatisfied + dos_veryUnsatisfied + tres_veryUnsatisfied + cuatro_veryUnsatisfied + cinco_veryUnsatisfied
        veryUnsatisfied = float(((veryUnsatisfied * 100) / polls_total) / 5)
        veryUnsatisfied = float(("%0.2f" % veryUnsatisfied))

        # obtenner el valor de la pregunta uno y todos sus porcentajes
        uno_verySatisfied = float((uno_verySatisfied * 100) / polls_total)
        uno_verySatisfied = float(("%0.2f" % uno_verySatisfied))

        uno_satisfied = float((uno_satisfied * 100) / polls_total)
        uno_satisfied = float(("%0.2f" % uno_satisfied))

        uno_Unsatisfied = float((uno_Unsatisfied * 100) / polls_total)
        uno_Unsatisfied = float(("%0.2f" % uno_Unsatisfied))

        uno_veryUnsatisfied = float((uno_veryUnsatisfied * 100) / polls_total)
        uno_veryUnsatisfied = float(("%0.2f" % uno_veryUnsatisfied))
        # obtenner el valor de la pregunta dos y todos sus porcentajes
        dos_verySatisfied = float((dos_verySatisfied * 100) / polls_total)
        dos_verySatisfied = float(("%0.2f" % dos_verySatisfied))

        dos_satisfied = float((dos_satisfied * 100) / polls_total)
        dos_satisfied = float(("%0.2f" % dos_satisfied))

        dos_Unsatisfied = float((uno_Unsatisfied * 100) / polls_total)
        dos_Unsatisfied = float(("%0.2f" % uno_Unsatisfied))

        dos_veryUnsatisfied = float((dos_veryUnsatisfied * 100) / polls_total)
        dos_veryUnsatisfied = float(("%0.2f" % dos_veryUnsatisfied))
        # obtenner el valor de la pregunta tres y todos sus porcentajes
        tres_verySatisfied = float((tres_verySatisfied * 100) / polls_total)
        tres_verySatisfied = float(("%0.2f" % tres_verySatisfied))

        tres_satisfied = float((tres_satisfied * 100) / polls_total)
        tres_satisfied = float(("%0.2f" % tres_satisfied))

        tres_Unsatisfied = float((tres_Unsatisfied * 100) / polls_total)
        tres_Unsatisfied = float(("%0.2f" % tres_Unsatisfied))

        tres_veryUnsatisfied = float((tres_veryUnsatisfied * 100) / polls_total)
        tres_veryUnsatisfied = float(("%0.2f" % tres_veryUnsatisfied))
        # obtenner el valor de la pregunta cuatro y todos sus porcentajes
        cuatro_verySatisfied = float((cuatro_verySatisfied * 100) / polls_total)
        cuatro_verySatisfied = float(("%0.2f" % cuatro_verySatisfied))

        cuatro_satisfied = float((cuatro_satisfied * 100) / polls_total)
        cuatro_satisfied = float(("%0.2f" % cuatro_satisfied))

        cuatro_Unsatisfied = float((cuatro_Unsatisfied * 100) / polls_total)
        cuatro_Unsatisfied = float(("%0.2f" % cuatro_Unsatisfied))

        cuatro_veryUnsatisfied = float((cuatro_veryUnsatisfied * 100) / polls_total)
        cuatro_veryUnsatisfied = float(("%0.2f" % cuatro_veryUnsatisfied))
        # obtenner el valor de la pregunta cinco y todos sus porcentajes
        cinco_verySatisfied = float((cinco_verySatisfied * 100) / polls_total)
        cinco_verySatisfied = float(("%0.2f" % cinco_verySatisfied))

        cinco_satisfied = float((cinco_satisfied * 100) / polls_total)
        cinco_satisfied = float(("%0.2f" % cinco_satisfied))

        cinco_Unsatisfied = float((cinco_Unsatisfied * 100) / polls_total)
        cinco_Unsatisfied = float(("%0.2f" % cinco_Unsatisfied))

        cinco_veryUnsatisfied = float((cinco_veryUnsatisfied * 100) / polls_total)
        cinco_veryUnsatisfied = float(("%0.2f" % cinco_veryUnsatisfied))

    return render(request, 'poll_satisfaction.html', {
        'requests': requests,
        'verySatisfied': verySatisfied,
        'satisfied': satisfied,
        'Unsatisfied': Unsatisfied,
        'veryUnsatisfied': veryUnsatisfied,
        'uno_verySatisfied': uno_verySatisfied,
        'dos_verySatisfied': dos_verySatisfied,
        'tres_verySatisfied': tres_verySatisfied,
        'cuatro_verySatisfied': cuatro_verySatisfied,
        'cinco_verySatisfied': cinco_verySatisfied,
        'uno_satisfied': uno_satisfied,
        'dos_satisfied': dos_satisfied,
        'tres_satisfied': tres_satisfied,
        'cuatro_satisfied': cuatro_satisfied,
        'cinco_satisfied': cinco_satisfied,
        'uno_Unsatisfied': uno_Unsatisfied,
        'dos_Unsatisfied': dos_Unsatisfied,
        'tres_Unsatisfied': tres_Unsatisfied,
        'cuatro_Unsatisfied': cuatro_Unsatisfied,
        'cinco_Unsatisfied': cinco_Unsatisfied,
        'uno_veryUnsatisfied': uno_veryUnsatisfied,
        'dos_veryUnsatisfied': dos_veryUnsatisfied,
        'tres_veryUnsatisfied': tres_veryUnsatisfied,
        'cuatro_veryUnsatisfied': cuatro_veryUnsatisfied,
        'cinco_veryUnsatisfied': cinco_veryUnsatisfied
    })

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from os import path

from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver


def unique_file_path(instance, filename):
    base, ext = path.splitext(filename)
    newname = "%s%s" % (instance.name, ext)
    return path.join('equipment_img', newname)


# Create your models here.
class Equipment(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    location = models.CharField(max_length=200, null=False, blank=False)
    responsible = models.ForeignKey(
        User, null=False, blank=False, related_name='equipment_user_set', on_delete=models.PROTECT
    )
    image = models.ImageField(upload_to=unique_file_path, null=True, blank=False)
    inventory_type = models.CharField(
        max_length=1, blank=False, default='1', choices=(
            ('1', 'Computer equipment'),
            ('2', 'Audio'),
            ('3', 'Video'),
            ('4', 'Cabling')
        )
    )

    def __str__(self):
        return 'Equipment: {0} '.format(self.name)


class Request(models.Model):
    user = models.ForeignKey(
        User, null=False, blank=False, related_name='request_user_set', on_delete=models.PROTECT
    )
    technical = models.ForeignKey(
        User, null=True, blank=True, related_name='request_technical_set', on_delete=models.PROTECT
    )
    request_type = models.CharField(
        max_length=1, blank=False, default='1', choices=(
            ('1', 'Maintenance of computer equipment'),
            ('2', 'Configuration in general'),
            ('3', 'Software installation'),
            ('4', 'Computer consulting'),
            ('5', 'Audio and Events'),
            ('6', 'Problems in general'),
            ('7', 'Problems in Laboratories'),
        )
    )
    equipment_id = models.ForeignKey(
        Equipment, null=True, blank=True, related_name='equipment_set', on_delete=models.PROTECT
    )
    status = models.CharField(
        max_length=1, blank=False, default='1', choices=(
            ('1', 'Pennding'),
            ('2', 'on process'),
            ('3', 'Canceled'),
            ('4', 'Done'),
            ('5', 'Pause')
        )
    )
    comments = models.CharField(max_length=200, null=True, blank=False)
    observations = models.CharField(max_length=200, null=True, blank=False)
    date_request = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    date_onprocess = models.DateTimeField(null=True, blank=True)
    date_done = models.DateTimeField(null=True, blank=True)
    date_cancel = models.DateTimeField(null=True, blank=True)
    date_pause = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return 'Request N: {0} Status: {1} Request type: {2}'.format(self.id, self.get_status_display(),
                                                                     self.get_request_type_display())


class Poll(models.Model):
    question = models.CharField(
        max_length=1, blank=False, default='1', choices=(
            ('1', 'Was it easy to request the service?'),
        )
    )
    answer = models.CharField(
        max_length=1, blank=False, default='1', choices=(
            ('1', 'Very satisfied'),
            ('2', 'Satisfied'),
            ('3', 'Unsatisfied'),
            ('4', 'Very Unsatisfied'),
        )
    )
    questionTwo = models.CharField(
        max_length=1, blank=False, default='1', choices=(
            ('1', 'What was the quality of the service?'),
        )
    )
    answerTwo = models.CharField(
        max_length=1, blank=False, default='1', choices=(
            ('1', 'Very satisfied'),
            ('2', 'Satisfied'),
            ('3', 'Unsatisfied'),
            ('4', 'Very Unsatisfied'),
        )
    )
    questionThree = models.CharField(
        max_length=1, blank=False, default='1', choices=(
            ('1', 'How do you feel about the behavior of the technician?'),
        )
    )
    answerThree = models.CharField(
        max_length=1, blank=False, default='1', choices=(
            ('1', 'Very satisfied'),
            ('2', 'Satisfied'),
            ('3', 'Unsatisfied'),
            ('4', 'Very Unsatisfied'),
        )
    )
    questionFour = models.CharField(
        max_length=1, blank=False, default='1', choices=(
            ('1', 'How do you feel about the service the technician performed?'),
        )
    )
    answerFour = models.CharField(
        max_length=1, blank=False, default='1', choices=(
            ('1', 'Very satisfied'),
            ('2', 'Satisfied'),
            ('3', 'Unsatisfied'),
            ('4', 'Very Unsatisfied'),
        )
    )
    questionFive = models.CharField(
        max_length=1, blank=False, default='1', choices=(
            ('1', 'What is your level of satisfaction?'),
        )
    )
    answerFive = models.CharField(
        max_length=1, blank=False, default='1', choices=(
            ('1', 'Very satisfied'),
            ('2', 'Satisfied'),
            ('3', 'Unsatisfied'),
            ('4', 'Very Unsatisfied'),
        )
    )
    request_id = models.ForeignKey(
        Request, null=False, blank=True, related_name='request_set', on_delete=models.PROTECT
    )
    date_request = models.DateTimeField(null=True, blank=False, auto_now_add=True)

    status = models.CharField(
        max_length=1, blank=False, default='1', choices=(
            ('1', 'Pennding'),
            ('2', 'Done'),
        )
    )

    def __str__(self):
        return 'Poll of the {0} '.format(self.request_id)


class Activity(models.Model):
    tittle = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    date_request = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    date_event = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return 'Tittle: {0} '.format(self.tittle)


class Comment(models.Model):
    comment = models.CharField(max_length=200, null=False, blank=False)
    user = models.ForeignKey(
        User, null=False, blank=False, related_name='comment_user_set', on_delete=models.PROTECT
    )
    date_request = models.DateTimeField(null=True, blank=False, auto_now_add=True)

    def __str__(self):
        return 'Comment by: {0} '.format(self.user.get_full_name)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    department = models.CharField(
        max_length=1, blank=False, default='5', choices=(
            ('1', 'Principal'),
            ('2', 'Administration and finance'),
            ('3', 'Linking'),
            ('4', 'Planning and evaluation'),
            ('5', 'Academician'),
        )
    )
    building = models.CharField(
        max_length=1, blank=False, default='1', choices=(
            ('1', 'Teaching 1'),
            ('2', 'Teaching 2'),
            ('3', 'Heavy Laboratory'),
            ('4', 'Library'),
            ('5', 'Other'),
        )
    )

    def __str__(self):  # __unicode__ for Python 2

        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Preventive_Maintenance(models.Model):
    user = models.ForeignKey(
        User, null=False, blank=False, related_name='Maintenance_user_set', on_delete=models.PROTECT
    )
    technical = models.ForeignKey(
        User, null=True, blank=True, related_name='Maintenance_technical_set', on_delete=models.PROTECT
    )
    request_type = models.CharField(
        max_length=1, blank=False, default='1', choices=(
            ('1', 'Preventive Maintenance'),
            ('2', 'Corrective Maintenance')
        )
    )
    status = models.CharField(
        max_length=1, blank=False, default='1', choices=(
            ('1', 'Pennding'),
            ('2', 'on process'),
            ('3', 'Canceled'),
            ('4', 'Done'),
            ('5', 'Pause')
        )
    )
    comments = models.CharField(max_length=200, null=True, blank=False)
    observations = models.CharField(max_length=200, null=True, blank=False)
    date_request = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    date_onprocess = models.DateTimeField(null=True, blank=True)
    date_done = models.DateTimeField(null=True, blank=True)
    date_cancel = models.DateTimeField(null=True, blank=True)
    date_pause = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return 'Maintenance N: {0} Status: {1} Request type: {2}'.format(self.id, self.get_status_display(),
                                                                     self.get_request_type_display())


class Equipment_Maintenance(models.Model):
    equipment_id = models.ForeignKey(
        Equipment, null=True, blank=True, related_name='maintenance_equipment_set', on_delete=models.PROTECT
    )
    preventive_maintenance_id = models.ForeignKey(
        Preventive_Maintenance, null=True, blank=True, related_name='preventive_maintenance_set', on_delete=models.PROTECT
    )
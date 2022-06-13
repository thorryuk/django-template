from os import truncate
from typing import DefaultDict
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.base import Model, ModelBase
from django.db.models.expressions import F
from django.db.models.fields.related import ForeignKey
from django.utils.functional import keep_lazy_text
from django.utils.timezone import now


class UserExtend(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='admin_user', on_delete=models.DO_NOTHING)
    profile_pict_url = models.CharField(max_length=255, null=False)
    is_suspended = models.IntegerField(null=False, choices=((0, 'Not Suspended'), (1, 'Suspended')))
    sex = models.CharField(max_length=6, blank=True, choices=(('male', 'Male'),
                                                              ('female', 'Female')))
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=25, blank=True, null=True)
    create_date = models.DateField()
    create_by = models.CharField(max_length=50, blank=True, null=True)
    email_signature = models.CharField(max_length=255, blank=True, null=True)
    is_activated = models.IntegerField(null=False, default=0, choices=((0, 'Not Activated'),
                                                                       (1, 'Activated')))
    activation_expired_date = models.DateField(blank=True, null=True)
    activation_key = models.CharField(max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(blank=False, default=False)

    def __str__(self):
        return '%s' % self.user


class UserArea(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True,
                               related_name='child')
    parent_alias = models.CharField(max_length=10, blank=True)
    type = models.CharField(max_length=15, choices=(('city', 'City'), ('province', 'Province'),
                                                    ('country', 'Country')))
    alias = models.CharField(max_length=10, blank=True)
    loc_lat = models.CharField(max_length=30, blank=True)
    loc_lon = models.CharField(max_length=30, blank=True)
    continent_alias = models.CharField(max_length=10, blank=True)
    continent_detail = models.CharField(max_length=30, blank=True)


class RoleGroup(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100, null=True, blank=True)
    create_date = models.DateField(null=True, blank=True)
    create_by = models.CharField(max_length=255, null=True, blank=True)
    modified_date = models.DateField(null=True, blank=True)
    modified_by = models.CharField(max_length=255, null=True, blank=True)


class RoleUser(models.Model):
    role_group = models.ForeignKey(RoleGroup, on_delete=models.DO_NOTHING)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    create_date = models.DateField()
    create_by = models.CharField(max_length=300, null=True, blank=True)
    modify_date = models.DateField(null=True, blank=True)
    modified_by = models.CharField(max_length=300, null=True, blank=True)


class Menu(models.Model):
    name = models.CharField(max_length=50)
    parent_menu = models.ForeignKey('self', related_name='parent', blank=True, null=True, on_delete=models.DO_NOTHING)
    link = models.CharField(max_length=400, null=True, blank=True)
    is_left_menu = models.BooleanField(null=False, blank=False, default=False)
    alias_name = models.CharField(max_length=30, null=True, blank=True)
    icon = models.CharField(max_length=200, null=True, blank=True)
    is_tree = models.BooleanField(default=False)
    order = models.IntegerField(null=True, blank=True)


class RoleMenu(models.Model):
    menu = models.ForeignKey(Menu, null=True, blank=True, on_delete=models.DO_NOTHING)
    role_group = models.ForeignKey(RoleGroup , on_delete=models.DO_NOTHING)

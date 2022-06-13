# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2022-04-29 00:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_menu_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextend',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='admin_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2022-03-16 16:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='order',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

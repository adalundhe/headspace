# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-08 00:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('symptom_manager', '0004_symptom_location'),
    ]

    operations = [
        migrations.RenameField(
            model_name='symptom',
            old_name='type',
            new_name='type_of',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-22 19:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminmailer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='body',
            field=models.TextField(verbose_name='Meldung'),
        ),
    ]

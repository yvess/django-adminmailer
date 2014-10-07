# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function  # python3
from __future__ import unicode_literals, division  # python3
from django.db import models
from django.utils.timezone import now
from django.conf import settings


class Message(models.Model):
    created = models.DateTimeField(
        auto_now_add=True, editable=False, default=now)
    modified = models.DateTimeField(
        auto_now=True, editable=False, default=now)
    subject = models.CharField('Betreff', max_length=200)
    body = models.TextField('Meldung', max_length=4)
    test_email = models.EmailField('Test-Empfänger', blank=True)
    recipient_list = models.ForeignKey(
        settings.ADMINMAILER['recipient_list'], null=True,
        verbose_name='Versender Liste'
    )

    was_sended = models.BooleanField(
        "Versand gestartet", default=False, editable=False)
    total_sended = models.IntegerField(
        "Anzahl Empfänger", editable=False, null=True)
    recipients = models.TextField(
        "Empfänger", editable=False, blank=True)
    date_sended = models.DateTimeField(
        "Versanddatum", editable=False, null=True)

    class Meta:
        verbose_name = 'Meldung'
        verbose_name_plural = 'Meldungen'

    def __unicode__(self):
        return self.subject

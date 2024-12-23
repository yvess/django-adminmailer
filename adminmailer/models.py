from django.db import models
from django.utils.timezone import now
from django.conf import settings


class Message(models.Model):
    created = models.DateTimeField(
        auto_now_add=True, editable=False)
    modified = models.DateTimeField(
        auto_now=True, editable=False)
    subject = models.CharField('Betreff', max_length=200)
    body = models.TextField('Meldung')
    test_email = models.EmailField('Test-Empfänger', blank=True)
    recipient_list = models.ForeignKey(
        settings.ADMINMAILER['recipient_list'], null=True, blank=True,
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

    def __str__(self):
        return self.subject

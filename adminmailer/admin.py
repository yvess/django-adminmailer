
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from adminmailer.models import Message


class MessageAdmin(admin.ModelAdmin):
    readonly_fields = (
        'was_sended', 'date_sended', 'total_sended', 'recipients')
    fieldsets = (
        ('Meldung', {
         'fields': ('subject', 'body', 'test_email', 'recipient_list')
         }),
        ('Versandinfos', {
         'fields': ('was_sended', 'date_sended', 'total_sended', 'recipients')
         }),
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(MessageAdmin, self).get_fieldsets(request, obj)
        recipients = settings.ADMINMAILER['recipients']
        if '.' in recipients:
            fields = list(self.fieldsets[0][1]['fields'])
            try:
                fields.remove('recipient_list')
                self.fieldsets[0][1]['fields'] = fields
            except ValueError:
                pass
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.was_sended:
                return (
                    self.readonly_fields +
                    ('subject', 'body', 'recipient_list', 'test_email')
                )
        return self.readonly_fields

    def response_change(self, request, obj):
        if "_send_test" in request.POST:
            redirect_url = reverse(
                'adminmailer_send_test', args=[obj.id],
                current_app=self.admin_site.name)
            return HttpResponseRedirect(redirect_url)
        elif "_send_all" in request.POST:
            redirect_url = reverse(
                'adminmailer_send_all', args=[obj.id],
                current_app=self.admin_site.name)
            return HttpResponseRedirect(redirect_url)
        else:
            res = super(MessageAdmin, self).response_change(request, obj)
            return res

admin.site.register(Message, MessageAdmin)

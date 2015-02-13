# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Message'
        db.create_table('adminmailer_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('body', self.gf('django.db.models.fields.TextField')(max_length=4)),
            ('test_email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('recipient_list', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'], null=True, blank=True)),
            ('was_sended', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('total_sended', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('recipients', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_sended', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('adminmailer', ['Message'])


    def backwards(self, orm):
        # Deleting model 'Message'
        db.delete_table('adminmailer_message')


    models = {
        'adminmailer.message': {
            'Meta': {'object_name': 'Message'},
            'body': ('django.db.models.fields.TextField', [], {'max_length': '4'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'date_sended': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'recipient_list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Group']", 'null': 'True', 'blank': 'True'}),
            'recipients': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'test_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'total_sended': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'was_sended': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['adminmailer']

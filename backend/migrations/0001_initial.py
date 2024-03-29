# Generated by Django 3.2 on 2022-09-09 07:48

import backend.utils
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fact',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_id', models.CharField(blank=True, default='', max_length=100)),
                ('namespace', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('namespace_item_id', models.CharField(blank=True, default='', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('entity', models.CharField(max_length=100)),
                ('property_data', models.JSONField(default=backend.utils.default_property_data)),
                ('value_data', models.JSONField(default=backend.utils.default_value_data)),
                ('data_type', models.CharField(blank=True, default='Item', max_length=100)),
                ('qualifiers', models.JSONField(default=dict)),
                ('references', models.JSONField(default=backend.utils.default_references)),
                ('shown_to_editors', models.IntegerField(default=0)),
                ('confirmed_at', models.DateTimeField(auto_now=True)),
                ('evidence_highlight', models.JSONField(default=backend.utils.default_evidence_highlight)),
                ('validated_by', models.CharField(blank=True, default='', max_length=100)),
                ('feedback', models.JSONField(default=backend.utils.default_feedback)),
            ],
        ),
    ]

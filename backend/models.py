import uuid
from django.db import models
from backend.utils import (
    default_data_value,
    default_evidence_highlight,
    default_feedback,
    default_meta_information,
    default_references,
)


class Fact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=100, blank=True, default="")
    namespace = models.CharField(max_length=200, unique=True, blank=True, null=True)
    namespace_item_id = models.CharField(max_length=100, blank=True, default="")
    candidate_created_at = models.DateTimeField(auto_now_add=True)
    wikidata_entity = models.URLField(blank=True, default="")
    wikidata_property = models.CharField(max_length=100, blank=True, default="")
    data_value = models.JSONField(default=default_data_value)
    data_type = models.CharField(max_length=100, blank=True, default="")
    qualifiers = models.JSONField(default=dict)
    references = models.JSONField(default=default_references)
    shown_to_editors = models.IntegerField(default=0)
    confirmed_at = models.DateTimeField(auto_now=True)
    evidence_highlight = models.JSONField(default=default_evidence_highlight)
    validated_by = models.CharField(max_length=100, blank=True, default="")
    meta_information = models.JSONField(default=default_meta_information)
    feedback = models.JSONField(default=default_feedback)

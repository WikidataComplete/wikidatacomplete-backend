import uuid
from django.db import models


class Fact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=100, blank=True, default="")
    namespace = models.CharField(max_length=200, unique=True, blank=True, null=True)
    namespace_item_id = models.CharField(max_length=100, blank=True, default="")
    candidate_created_at = models.DateTimeField(auto_now_add=True)
    wikidata_entity = models.URLField(blank=True, default="")
    wikidata_property = models.CharField(max_length=100, blank=True, default="")
    data_value = models.JSONField(default=list)
    data_type = models.CharField(max_length=100, blank=True, default="")
    qualifiers = models.JSONField(default=dict)
    references = models.JSONField(default=list)
    shown_to_editors = models.IntegerField(default=0)
    confirmed_at = models.DateTimeField(auto_now=True)
    evidence_highlight = models.JSONField(default=dict)
    validated_by = models.CharField(max_length=100, blank=True, default="")
    meta_information = models.JSONField(default=dict)
    feedback = models.JSONField(default=dict)

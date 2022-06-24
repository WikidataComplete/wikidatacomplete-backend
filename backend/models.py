import uuid
from django.db import models


class Fact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=30, blank=True, default="")
    namespace = models.CharField(max_length=100, unique=True, null=True, default=None)
    namespace_item_id = models.CharField(max_length=30, blank=True, default="")
    candidate_created_at = models.DateTimeField(auto_now_add=True)
    wikidata_entity = models.URLField(blank=True, default="")
    wikidata_property = models.CharField(max_length=30, blank=True, default="")
    data_value = models.CharField(max_length=100, blank=True, default="")
    data_type = models.CharField(max_length=30, blank=True, default="")
    qualifiers = models.JSONField(null=True)
    references = models.JSONField(null=True)
    shown_to_editors = models.IntegerField(default=0)
    confirmed_at = models.DateTimeField(auto_now=True)
    evidence_highlight = models.JSONField(null=True)
    editor_feedback = models.BooleanField(null=True)
    validated_by = models.CharField(max_length=30, blank=True, default="")

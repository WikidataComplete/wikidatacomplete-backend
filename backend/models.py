import uuid
from django.db import models
from backend.utils import (
    default_property_data,
    default_value_data,
    default_references,
    default_evidence_highlight,
    default_feedback,
)


class Fact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=100, blank=True, default="")
    namespace = models.CharField(max_length=200, unique=True, blank=True, null=True)
    namespace_item_id = models.CharField(max_length=100, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    entity = models.CharField(max_length=100)
    property_data = models.JSONField(default=default_property_data)
    value_data = models.JSONField(default=default_value_data)
    data_type = models.CharField(max_length=100, blank=True, default="Item")
    qualifiers = models.JSONField(default=dict)
    references = models.JSONField(default=default_references)
    shown_to_editors = models.IntegerField(default=0)
    confirmed_at = models.DateTimeField(auto_now=True)
    evidence_highlight = models.JSONField(
        null=True, blank=True, default=default_evidence_highlight
    )
    validated_by = models.CharField(max_length=100, blank=True, default="")
    feedback = models.JSONField(default=default_feedback)

    class Meta:
        unique_together = ("entity", "property_data", "value_data")

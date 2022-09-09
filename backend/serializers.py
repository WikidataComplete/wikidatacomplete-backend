from rest_framework import serializers
from backend.models import Fact
from drf_yasg import openapi


class PropertyDataJSONField(serializers.JSONField):
    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "properties": {
                "property": openapi.Schema(type=openapi.TYPE_STRING),
                "value": openapi.Schema(type=openapi.TYPE_STRING),
            },
            "required": ["property", "value"],
        }


class ValueDataJSONField(serializers.JSONField):
    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "properties": {
                "entity": openapi.Schema(type=openapi.TYPE_STRING),
                "value": openapi.Schema(type=openapi.TYPE_STRING),
            },
            "required": ["entity", "value"],
        }


class ReferencesJSONField(serializers.JSONField):
    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_ARRAY,
            "items": openapi.Items(
                type=openapi.TYPE_OBJECT,
                properties={
                    "property": openapi.Schema(type=openapi.TYPE_STRING),
                    "value": openapi.Schema(type=openapi.TYPE_STRING),
                    "type": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
            "required": ["property", "value", "type"],
        }


class EvidenceHighlightJSONField(serializers.JSONField):
    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "properties": {
                "start_index": openapi.Schema(type=openapi.TYPE_INTEGER),
                "end_index": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        }


class FactListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fact
        fields = (
            "id",
            "user_id",
            "namespace",
            "namespace_item_id",
            "created_at",
            "entity",
            "property_data",
            "value_data",
            "data_type",
            "qualifiers",
            "references",
            "shown_to_editors",
            "confirmed_at",
            "evidence_highlight",
            "validated_by",
            "feedback",
        )
        read_only_fields = (
            "id",
            "user_id",
            "namespace",
            "namespace_item_id",
            "created_at",
            "qualifiers",
            "shown_to_editors",
            "confirmed_at",
            "validated_by",
            "feedback",
            "data_type",
        )

    property_data = PropertyDataJSONField()
    value_data = ValueDataJSONField()
    references = ReferencesJSONField()
    evidence_highlight = EvidenceHighlightJSONField(allow_null=True, required=False)

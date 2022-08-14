from dataclasses import field
from rest_framework import serializers
from backend.models import Fact
from drf_yasg import openapi


class DataValueJSONField(serializers.JSONField):
    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_ARRAY,
            "items": openapi.Items(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "object": openapi.Schema(type=openapi.TYPE_STRING),
                    "objectLabel": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
            "required": ["id", "object", "objectLabel"],
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
                    "name": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
            "required": ["property", "value", "type"],
        }


class EvidenceHighlightJSONField(serializers.JSONField):
    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "properties": {
                "startIdx": openapi.Schema(type=openapi.TYPE_INTEGER),
                "endIdx": openapi.Schema(type=openapi.TYPE_INTEGER),
                "text": openapi.Schema(type=openapi.TYPE_STRING),
            },
            "required": ["startIdx", "endIdx", "text"],
        }


class MetaInformationJSONField(serializers.JSONField):
    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "properties": {
                "question": openapi.Schema(type=openapi.TYPE_STRING),
            },
            "required": ["question"],
        }


class FactListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fact
        fields = (
            "id",
            "user_id",
            "namespace",
            "namespace_item_id",
            "candidate_created_at",
            "wikidata_entity",
            "wikidata_property",
            "data_value",
            "data_type",
            "qualifiers",
            "references",
            "shown_to_editors",
            "confirmed_at",
            "evidence_highlight",
            "validated_by",
            "meta_information",
            "feedback",
        )
        read_only_fields = (
            "id",
            "user_id",
            "namespace",
            "namespace_item_id",
            "candidate_created_at",
            "qualifiers",
            "shown_to_editors",
            "confirmed_at",
            "validated_by",
            "feedback",
        )

    data_value = DataValueJSONField()
    references = ReferencesJSONField()
    evidence_highlight = EvidenceHighlightJSONField()
    meta_information = MetaInformationJSONField()

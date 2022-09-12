from rest_framework import serializers
from backend.models import Fact
from drf_yasg import openapi


class EntityCharField(serializers.CharField):
    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_STRING,
            "title": "Wikidata Page's QId. Eg: Q1025718",
        }


class PropertyDataJSONField(serializers.JSONField):
    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "properties": {
                "property": openapi.Schema(
                    title="Wikidata Property. Eg: P641", type=openapi.TYPE_STRING
                ),
                "value": openapi.Schema(
                    title="Value of Property. Eg: Sport", type=openapi.TYPE_STRING
                ),
            },
            "required": ["property", "value"],
        }


class ValueDataJSONField(serializers.JSONField):
    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "properties": {
                "entity": openapi.Schema(
                    title="Wikidata Entity's QId. Eg: Q2746", type=openapi.TYPE_STRING
                ),
                "value": openapi.Schema(
                    title="Value of Entity. Eg: association football",
                    type=openapi.TYPE_STRING,
                ),
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
                    "property": openapi.Schema(
                        title="Wikidata Property. Eg: P813", type=openapi.TYPE_STRING
                    ),
                    "value": openapi.Schema(
                        title="Value of Property. Eg: retrieved",
                        type=openapi.TYPE_STRING,
                    ),
                    "type": openapi.Schema(
                        title="data type of Property. Eg: string",
                        type=openapi.TYPE_STRING,
                    ),
                },
            ),
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

    entity = EntityCharField(max_length=100)
    property_data = PropertyDataJSONField(
        help_text="Data for Property of Wikidata Statement."
    )
    value_data = ValueDataJSONField(help_text="Data for Value of Wikidata Statement.")
    references = ReferencesJSONField(
        help_text="Data for References of Wikidata Statement."
    )
    evidence_highlight = EvidenceHighlightJSONField(
        allow_null=True,
        required=False,
        help_text="Only applicable when references have P143.",
    )

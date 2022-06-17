from rest_framework import serializers
from backend.models import Fact


class FactListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fact
        fields = "__all__"

from rest_framework import serializers
from .models import WeightEntry


class WeightEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model  = WeightEntry
        fields = ['id', 'weight', 'date', 'logged_at']
        read_only_fields = ['logged_at']
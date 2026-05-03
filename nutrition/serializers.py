from rest_framework import serializers
from .models import Meal, MacroTarget


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Meal
        fields = '__all__'
        read_only_fields = ['user', 'created_at']


class MacroTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model  = MacroTarget
        fields = ['calorie_goal', 'protein', 'carbs', 'fats']
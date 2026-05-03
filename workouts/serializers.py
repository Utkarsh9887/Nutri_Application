from rest_framework import serializers
from .models import Exercise, WorkoutTemplate, WorkoutLog


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Exercise
        fields = ['id', 'name', 'muscle_group', 'equipment',
                  'experience_level', 'instructions', 'recommended_sets', 'tips']


class WorkoutTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = WorkoutTemplate
        fields = ['id', 'name', 'exercises']


class WorkoutLogSerializer(serializers.ModelSerializer):
    class Meta:
        model  = WorkoutLog
        fields = ['id', 'name', 'sets', 'reps', 'weight', 'difficulty', 'date', 'logged_at']
        read_only_fields = ['logged_at']
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model  = UserProfile
        fields = [
            'display_name', 'bio', 'gender',
            'date_of_birth', 'height_cm',
            'goal', 'activity_level', 'updated_at'
        ]
        read_only_fields = ['updated_at']


class UserSerializer(serializers.ModelSerializer):
    """
    Combines the Django User fields with the UserProfile fields
    into one flat response so the frontend only needs one call.
    """
    profile = ProfileSerializer()

    class Meta:
        model  = User
        fields = ['id', 'username', 'email', 'profile']
        read_only_fields = ['id', 'username']
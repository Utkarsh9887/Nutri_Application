from rest_framework import serializers
from .models import ProgressPhoto


class ProgressPhotoSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model  = ProgressPhoto
        fields = ['id', 'caption', 'date', 'uploaded_at', 'image_url']
        read_only_fields = ['uploaded_at', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
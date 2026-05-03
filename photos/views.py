from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from .models import ProgressPhoto
from .serializers import ProgressPhotoSerializer


# ── LIST PHOTOS ────────────────────────────────────────────────────────────────
# GET /api/media/photos/
# Returns all photos for the logged-in user, newest first.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_photos(request):
    photos = ProgressPhoto.objects.filter(user=request.user)
    serializer = ProgressPhotoSerializer(photos, many=True, context={'request': request})
    return Response(serializer.data)


# ── UPLOAD PHOTO ───────────────────────────────────────────────────────────────
# POST /api/media/photos/
# Multipart form: { image: <file>, caption: "...", date: "YYYY-MM-DD" }

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_photo(request):
    image   = request.FILES.get('image')
    caption = request.data.get('caption', '')
    date    = request.data.get('date')

    if not image:
        return Response({'error': 'No image file provided.'}, status=400)
    if not date:
        from django.utils.timezone import now
        date = str(now().date())

    # Validate file type
    allowed = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
    if image.content_type not in allowed:
        return Response({'error': 'Only JPEG, PNG, WebP and GIF images are allowed.'}, status=400)

    # Validate file size — max 5MB
    if image.size > 5 * 1024 * 1024:
        return Response({'error': 'Image must be under 5MB.'}, status=400)

    photo = ProgressPhoto.objects.create(
        user    = request.user,
        image   = image,
        caption = caption,
        date    = date,
    )
    return Response(
        ProgressPhotoSerializer(photo, context={'request': request}).data,
        status=201
    )


# ── DELETE PHOTO ───────────────────────────────────────────────────────────────
# DELETE /api/media/photos/<id>/
# Also removes the image file from disk.

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_photo(request, photo_id):
    try:
        photo = ProgressPhoto.objects.get(id=photo_id, user=request.user)
        # Delete file from disk before removing the DB row
        if photo.image:
            photo.image.delete(save=False)
        photo.delete()
        return Response({'success': True})
    except ProgressPhoto.DoesNotExist:
        return Response({'error': 'Photo not found.'}, status=404)
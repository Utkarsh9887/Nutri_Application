from django.urls import path
from .views import list_photos, upload_photo, delete_photo

urlpatterns = [
    path('photos/',              list_photos,  name='list-photos'),   # GET
    path('photos/upload/',       upload_photo, name='upload-photo'),  # POST (multipart)
    path('photos/<int:photo_id>/', delete_photo, name='delete-photo'), # DELETE
]
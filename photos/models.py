from django.db import models
from django.contrib.auth.models import User
import os


def photo_upload_path(instance, filename):
    """Store photos under media/photos/<user_id>/<filename>"""
    ext  = filename.rsplit('.', 1)[-1].lower()
    name = filename.rsplit('.', 1)[0]
    safe = "".join(c for c in name if c.isalnum() or c in ('-', '_'))[:40]
    return f"photos/{instance.user.id}/{safe}.{ext}"


class ProgressPhoto(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    image   = models.ImageField(upload_to=photo_upload_path)
    caption = models.CharField(max_length=200, blank=True)
    date    = models.DateField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-uploaded_at']

    def __str__(self):
        return f"{self.user.username} photo — {self.date}"
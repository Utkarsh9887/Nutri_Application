from django.db import models
from django.contrib.auth.models import User


class Friendship(models.Model):
    """
    A directional follow — from_user follows to_user.
    To check mutual friendship query both directions.
    unique_together prevents duplicate follow rows.
    """
    from_user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    to_user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['from_user', 'to_user']]

    def __str__(self):
        return f"{self.from_user.username} → {self.to_user.username}"
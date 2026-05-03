from django.db import models
from django.contrib.auth.models import User


class WeightEntry(models.Model):
    """
    One weight measurement per user per day.
    The unique_together constraint prevents duplicate entries for the same date.
    """
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weight_entries')
    weight     = models.FloatField()          # kg
    date       = models.DateField()
    logged_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']
        unique_together = [['user', 'date']]  # one entry per day per user

    def __str__(self):
        return f"{self.user.username} — {self.weight}kg on {self.date}"
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    GOAL_CHOICES = [
        ('lose',     'Lose Weight'),
        ('maintain', 'Maintain Weight'),
        ('gain',     'Gain Muscle'),
    ]
    GENDER_CHOICES = [
        ('male',   'Male'),
        ('female', 'Female'),
        ('other',  'Other'),
    ]
    ACTIVITY_CHOICES = [
        ('sedentary',      'Sedentary'),
        ('lightly_active', 'Lightly Active'),
        ('active',         'Active'),
        ('very_active',    'Very Active'),
    ]

    user           = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name   = models.CharField(max_length=80, blank=True)
    bio            = models.TextField(blank=True)
    gender         = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    date_of_birth  = models.DateField(null=True, blank=True)
    height_cm      = models.FloatField(null=True, blank=True)   # for BMI
    goal           = models.CharField(max_length=10, choices=GOAL_CHOICES, blank=True)
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_CHOICES, blank=True)
    updated_at     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile({self.user.username})"


# Auto-create a blank profile whenever a new User is saved
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)